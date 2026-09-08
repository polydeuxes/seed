"""Report exact recurrence, containment, and composition of variable extents.

The input artifacts were frozen before this report.  This script reads only
those artifacts and the exact source windows they address.  It does not read
the Book, machine grammar, Rosetta material, dictionaries, language labels, or
expected vocabulary.

Usage:
    .venv/bin/python scripts/report_open_world_variable_extents.py
"""

from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_open_world_apertures import CORPUS, _window


INPUT = Path("/tmp/seed_open_world_variable_extents_blind.json")
OUTPUT = Path("/tmp/seed_open_world_variable_extent_relations.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _decode(materials: dict, reference: str) -> str:
    return bytes.fromhex(materials[reference]["utf8_hex"]).decode("utf-8")


def _render(value: str, boundary: int = 100) -> str:
    rendered = value.encode("unicode_escape").decode("ascii")
    if len(rendered) > boundary:
        return rendered[: boundary - 3] + "..."
    return rendered


def _extent_coordinates(branch: dict):
    seen = set()
    for family in branch["nodes"]:
        minimum_left, maximum_left = family["left_extension_range"]
        minimum_right, maximum_right = family["right_extension_range"]
        minimum_ranges = tuple(
            (start, end, origin)
            for start, end, origin in family["minimum_source_scalar_ranges"]
        )
        anchors = tuple(
            (start + minimum_left, end - minimum_right, origin)
            for start, end, origin in minimum_ranges
        )
        support_reference = _digest(anchors)
        for left_extension in range(minimum_left, maximum_left + 1):
            for right_extension in range(minimum_right, maximum_right + 1):
                coordinate = (left_extension, right_extension, support_reference)
                if coordinate in seen:
                    continue
                seen.add(coordinate)
                yield left_extension, right_extension, support_reference, anchors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    observation = json.loads(arguments.input.read_text(encoding="utf-8"))
    begun = time.perf_counter()
    sources = {}
    branches = []
    occupant_ranges_by_source: dict[str, list[dict]] = defaultdict(list)
    extent_families_by_source: dict[str, dict[int, list[dict]]] = defaultdict(
        lambda: defaultdict(list)
    )
    material_support: dict[str, dict[str, object]] = {}
    branch_inputs = []

    for source in observation["sources"]:
        source_begun = time.perf_counter()
        exact_bytes, _line_starts = _window(
            CORPUS.parent / source["source"], source["first_line"]
        )
        if _digest(exact_bytes) != source["material_sha256"]:
            raise ValueError("reported source differs from frozen source")
        text = exact_bytes.decode("utf-8")
        sources[source["source"]] = text
        for frame in source["frames"]:
            for branch_number, branch in enumerate(frame["branches"], start=1):
                branch_reference = _digest(
                    {
                        "source": source["source"],
                        "frame": frame["frame_number"],
                        "branch": branch_number,
                        "identity": branch["identity"],
                    }
                )
                for start, end, origin in branch["occupant_source_scalar_ranges"]:
                    occupant_ranges_by_source[source["source"]].append(
                        {
                            "branch_reference": branch_reference,
                            "source_scalar_range": [start, end],
                            "source_occurrence_reference": origin,
                        }
                    )

                maximum_scalar_count = 0
                terminal_families = []
                for family in branch["nodes"]:
                    scalar_count = source["materials"][family["maximal_material"]][
                        "scalar_count"
                    ]
                    maximum_scalar_count = max(maximum_scalar_count, scalar_count)
                    if not family["child_references"]:
                        terminal_families.append(
                            {
                                "family_reference": family["identity"],
                                "maximal_material": family["maximal_material"],
                                "maximal_scalar_count": scalar_count,
                                "support_count": len(
                                    family["maximal_source_scalar_ranges"]
                                ),
                                "maximal_source_scalar_ranges": family[
                                    "maximal_source_scalar_ranges"
                                ],
                            }
                        )

                branch_record = {
                    "reference": branch_reference,
                    "source": source["source"],
                    "frame_number": frame["frame_number"],
                    "branch_number": branch_number,
                    "initial_occurrence_count": branch["initial_occurrence_count"],
                    "extent_family_count": len(branch["nodes"]),
                    "addressed_extent_population_count": branch[
                        "addressed_extent_population_count"
                    ],
                    "maximum_scalar_count": maximum_scalar_count,
                    "terminal_families": terminal_families,
                }
                branches.append(branch_record)
                branch_inputs.append((source["source"], text, branch_reference, branch))

                for family in branch["nodes"]:
                    minimum_left, maximum_left = family["left_extension_range"]
                    minimum_right, maximum_right = family["right_extension_range"]
                    support_anchors = tuple(
                        (
                            start + minimum_left,
                            end - minimum_right,
                            origin,
                        )
                        for start, end, origin in family[
                            "minimum_source_scalar_ranges"
                        ]
                    )
                    support_reference = _digest(support_anchors)
                    for start, end, origin in family[
                        "minimum_source_scalar_ranges"
                    ]:
                        anchor_start = start + minimum_left
                        anchor_end = end - minimum_right
                        extent_families_by_source[source["source"]][
                            anchor_start
                        ].append(
                            {
                                "family_reference": family["identity"],
                                "branch_reference": branch_reference,
                                "support_reference": support_reference,
                                "source_occurrence_reference": origin,
                                "anchor_source_scalar_range": [
                                    anchor_start,
                                    anchor_end,
                                ],
                                "left_extension_range": [
                                    minimum_left,
                                    maximum_left,
                                ],
                                "right_extension_range": [
                                    minimum_right,
                                    maximum_right,
                                ],
                            }
                        )

                for left_extension, right_extension, _support_reference, anchors in (
                    _extent_coordinates(branch)
                ):
                    first_start, first_end, _first_origin = anchors[0]
                    material = text[
                        first_start - left_extension : first_end + right_extension
                    ]
                    material_reference = _digest(material.encode("utf-8"))
                    support = material_support.setdefault(
                        material_reference,
                        {
                            "material_utf8_hex": material.encode("utf-8").hex(),
                            "scalar_count": len(material),
                            "sources": set(),
                        },
                    )
                    support["sources"].add(source["source"])
        print(
            f"indexed {source['source']}: "
            f"{time.perf_counter() - source_begun:.3f}s",
            flush=True,
        )

    cross_source_references = {
        reference
        for reference, support in material_support.items()
        if len(support["sources"]) > 1
    }
    cross_source_coordinates: dict[str, dict[str, list[dict]]] = {
        reference: defaultdict(list) for reference in cross_source_references
    }
    for source_name, text, branch_reference, branch in branch_inputs:
        for left_extension, right_extension, support_reference, anchors in (
            _extent_coordinates(branch)
        ):
            first_start, first_end, _first_origin = anchors[0]
            material = text[
                first_start - left_extension : first_end + right_extension
            ]
            material_reference = _digest(material.encode("utf-8"))
            if material_reference not in cross_source_references:
                continue
            ranges = [
                [start - left_extension, end + right_extension, origin]
                for start, end, origin in anchors
            ]
            coordinate_reference = _digest(
                {
                    "branch": branch_reference,
                    "left_extension": left_extension,
                    "right_extension": right_extension,
                    "support": support_reference,
                }
            )
            cross_source_coordinates[material_reference][source_name].append(
                {
                    "coordinate_reference": coordinate_reference,
                    "branch_reference": branch_reference,
                    "left_extension": left_extension,
                    "right_extension": right_extension,
                    "source_scalar_ranges": ranges,
                }
            )

    cross_source_material = []
    for material_reference, support in sorted(material_support.items()):
        if material_reference not in cross_source_references:
            continue
        cross_source_material.append(
            {
                "material_reference": material_reference,
                "material_utf8_hex": support["material_utf8_hex"],
                "scalar_count": support["scalar_count"],
                "source_count": len(support["sources"]),
                "sources": dict(
                    sorted(cross_source_coordinates[material_reference].items())
                ),
            }
        )
    print(
        f"cross-source material projection: {time.perf_counter() - begun:.3f}s",
        flush=True,
    )

    occupancy_relations = []
    containment_relations = []
    occupancy_seen = set()
    containment_seen = set()
    for source_name, occupants in occupant_ranges_by_source.items():
        families_by_start = extent_families_by_source[source_name]
        starts = sorted(families_by_start)
        for occupant in occupants:
            occupant_start, occupant_end = occupant["source_scalar_range"]
            first = bisect_left(starts, occupant_start)
            stop = bisect_right(starts, occupant_end)
            for anchor_start in starts[first:stop]:
                for family in families_by_start[anchor_start]:
                    anchor_start, anchor_end = family[
                        "anchor_source_scalar_range"
                    ]
                    if anchor_end > occupant_end:
                        continue
                    if family["branch_reference"] == occupant["branch_reference"]:
                        continue
                    minimum_left, maximum_left = family["left_extension_range"]
                    minimum_right, maximum_right = family[
                        "right_extension_range"
                    ]
                    contained_maximum_left = min(
                        maximum_left, anchor_start - occupant_start
                    )
                    contained_maximum_right = min(
                        maximum_right, occupant_end - anchor_end
                    )
                    if (
                        contained_maximum_left < minimum_left
                        or contained_maximum_right < minimum_right
                    ):
                        continue
                    relation = {
                        "source": source_name,
                        "extent_family_reference": family["family_reference"],
                        "extent_branch_reference": family["branch_reference"],
                        "occupant_branch_reference": occupant["branch_reference"],
                        "source_occurrence_reference": family[
                            "source_occurrence_reference"
                        ],
                        "contained_left_extension_range": [
                            minimum_left,
                            contained_maximum_left,
                        ],
                        "contained_right_extension_range": [
                            minimum_right,
                            contained_maximum_right,
                        ],
                        "occupant_source_scalar_range": [occupant_start, occupant_end],
                    }
                    exact_left = anchor_start - occupant_start
                    exact_right = occupant_end - anchor_end
                    has_exact_occupancy = (
                        minimum_left <= exact_left <= maximum_left
                        and minimum_right <= exact_right <= maximum_right
                    )
                    if has_exact_occupancy:
                        occupancy = {
                            "source": source_name,
                            "extent_coordinate_reference": _digest(
                                {
                                    "branch": family["branch_reference"],
                                    "left_extension": exact_left,
                                    "right_extension": exact_right,
                                    "support": family["support_reference"],
                                }
                            ),
                            "extent_branch_reference": family[
                                "branch_reference"
                            ],
                            "support_reference": family["support_reference"],
                            "source_occurrence_reference": family[
                                "source_occurrence_reference"
                            ],
                            "occupant_branch_reference": occupant[
                                "branch_reference"
                            ],
                            "occupant_source_scalar_range": [
                                occupant_start,
                                occupant_end,
                            ],
                            "exact_left_extension": exact_left,
                            "exact_right_extension": exact_right,
                        }
                        identity = _digest(occupancy)
                        if identity not in occupancy_seen:
                            occupancy_seen.add(identity)
                            occupancy_relations.append(occupancy)
                    contained_extent_count = (
                        contained_maximum_left - minimum_left + 1
                    ) * (contained_maximum_right - minimum_right + 1)
                    strict_contained_extent_count = contained_extent_count - int(
                        has_exact_occupancy
                    )
                    if strict_contained_extent_count:
                        containment = {
                            **relation,
                            "strict_contained_extent_count": (
                                strict_contained_extent_count
                            ),
                        }
                        identity = _digest(containment)
                        if identity not in containment_seen:
                            containment_seen.add(identity)
                            containment_relations.append(containment)
        print(
            f"joined {source_name}: {time.perf_counter() - begun:.3f}s",
            flush=True,
        )

    finding = {
        "variable_extent_artifact_sha256": _digest(arguments.input.read_bytes()),
        "branch_count": len(branches),
        "extent_family_count": sum(
            branch["extent_family_count"] for branch in branches
        ),
        "addressed_extent_population_count": sum(
            branch["addressed_extent_population_count"] for branch in branches
        ),
        "branches": branches,
        "cross_source_exact_material": cross_source_material,
        "exact_extent_occupies_other_frame_position": occupancy_relations,
        "extent_family_ranges_contained_by_other_frame_position": (
            containment_relations
        ),
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)

    print(f"branches: {finding['branch_count']}")
    print(f"extent families: {finding['extent_family_count']}")
    print(f"addressed exact extents: {finding['addressed_extent_population_count']}")
    print(f"cross-source exact materials: {len(cross_source_material)}")
    print(f"exact frame-position occupancies: {len(occupancy_relations)}")
    print(
        "strict frame-position containment family ranges: "
        f"{len(containment_relations)}"
    )
    print("\nlongest terminal surface per branch:")
    for branch in branches:
        if not branch["terminal_families"]:
            continue
        terminal = max(
            branch["terminal_families"], key=lambda value: value["maximal_scalar_count"]
        )
        source = next(
            value for value in observation["sources"] if value["source"] == branch["source"]
        )
        print(
            f"{branch['source']} F{branch['frame_number']} B{branch['branch_number']} "
            f"occ={branch['initial_occurrence_count']} "
            f"extents={branch['addressed_extent_population_count']} "
            f"terminal={terminal['maximal_scalar_count']} "
            f"{_render(_decode(source['materials'], terminal['maximal_material']))!r}"
        )
    print(f"\nartifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
