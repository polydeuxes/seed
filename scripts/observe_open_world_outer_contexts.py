"""Measure outer-context consequences of frozen internal frame substitutions.

The observer reads only the frozen variable-extent and relation artifacts plus
the exact source windows they address.  It performs no counterfactual source
rewrite.  Two internal materials are compared only when the source already
placed them in distinct branches of one recurrent frame.

Usage:
    .venv/bin/python scripts/observe_open_world_outer_contexts.py
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import time

from observe_open_world_apertures import CORPUS, _window


VARIABLE_INPUT = Path("/tmp/seed_open_world_variable_extents_blind.json")
RELATION_INPUT = Path("/tmp/seed_open_world_variable_extent_relations.json")
OUTPUT = Path("/tmp/seed_open_world_outer_contexts_blind.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _material_reference(
    materials: dict[str, dict[str, object]],
    references_by_value: dict[str, str],
    value: str,
) -> str:
    existing_reference = references_by_value.get(value)
    if existing_reference is not None:
        return existing_reference
    encoded = value.encode("utf-8")
    reference = _digest(encoded)
    record = {
        "scalar_count": len(value),
        "byte_count": len(encoded),
        "utf8_hex": encoded.hex(),
    }
    if reference in materials and materials[reference] != record:
        raise AssertionError("material digest collision")
    materials[reference] = record
    references_by_value[value] = reference
    return reference


def _branch_reference(source_name: str, frame_number: int, branch_number: int, branch: dict) -> str:
    return _digest(
        {
            "source": source_name,
            "frame": frame_number,
            "branch": branch_number,
            "identity": branch["identity"],
        }
    )


def _context_population_and_families(
    *,
    text: str,
    branch: dict,
    materials: dict[str, dict[str, object]],
    references_by_value: dict[str, str],
) -> tuple[dict[str, dict], list[dict]]:
    contexts: dict[str, dict] = {}
    families = []
    seen = set()
    for family in branch["nodes"]:
        minimum_left, maximum_left = family["left_extension_range"]
        minimum_right, maximum_right = family["right_extension_range"]
        anchors = tuple(
            (
                start + minimum_left,
                end - minimum_right,
                origin,
            )
            for start, end, origin in family["minimum_source_scalar_ranges"]
        )
        support_reference = _digest(anchors)
        first_start, first_end, _first_origin = anchors[0]
        families.append(
            {
                "context_family_reference": family["identity"],
                "support_reference": support_reference,
                "source_occurrence_count": len(anchors),
                "left_extension_range": [minimum_left, maximum_left],
                "right_extension_range": [minimum_right, maximum_right],
                "minimum_left_material": _material_reference(
                    materials,
                    references_by_value,
                    text[first_start - minimum_left : first_start],
                ),
                "maximal_left_material": _material_reference(
                    materials,
                    references_by_value,
                    text[first_start - maximum_left : first_start],
                ),
                "minimum_right_material": _material_reference(
                    materials,
                    references_by_value,
                    text[first_end : first_end + minimum_right],
                ),
                "maximal_right_material": _material_reference(
                    materials,
                    references_by_value,
                    text[first_end : first_end + maximum_right],
                ),
                "parent_references": family["parent_references"],
                "child_references": family["child_references"],
            }
        )
        for left_extension in range(minimum_left, maximum_left + 1):
            for right_extension in range(minimum_right, maximum_right + 1):
                coordinate = (left_extension, right_extension, support_reference)
                if coordinate in seen:
                    continue
                seen.add(coordinate)
                left_material = text[
                    first_start - left_extension : first_start
                ]
                right_material = text[
                    first_end : first_end + right_extension
                ]
                left_reference = _material_reference(
                    materials, references_by_value, left_material
                )
                right_reference = _material_reference(
                    materials, references_by_value, right_material
                )
                context_reference = _digest(
                    {
                        "left_material": left_reference,
                        "right_material": right_reference,
                    }
                )
                finding = contexts.setdefault(
                    context_reference,
                    {
                        "context_reference": context_reference,
                        "left_material": left_reference,
                        "right_material": right_reference,
                        "left_scalar_count": left_extension,
                        "right_scalar_count": right_extension,
                        "is_nonempty_outer_context": bool(
                            left_extension or right_extension
                        ),
                        "support_populations": [],
                        "_support_references": set(),
                    },
                )
                if support_reference not in finding["_support_references"]:
                    finding["_support_references"].add(support_reference)
                    finding["support_populations"].append(
                        {
                            "support_reference": support_reference,
                            "source_occurrence_count": len(anchors),
                        }
                    )
    for finding in contexts.values():
        del finding["_support_references"]
    return contexts, families


def _comparison(
    first: dict,
    second: dict,
    *,
    comparison_boundary: str,
) -> dict:
    first_contexts = set(first["contexts"])
    second_contexts = set(second["contexts"])
    shared = first_contexts & second_contexts
    first_only = first_contexts - second_contexts
    second_only = second_contexts - first_contexts

    def nonempty(branch: dict, references: set[str]) -> list[str]:
        return sorted(
            reference
            for reference in references
            if branch["contexts"][reference]["is_nonempty_outer_context"]
        )

    for reference in shared:
        first_context = first["contexts"][reference]
        second_context = second["contexts"][reference]
        for coordinate in (
            "left_material",
            "right_material",
            "left_scalar_count",
            "right_scalar_count",
            "is_nonempty_outer_context",
        ):
            if first_context[coordinate] != second_context[coordinate]:
                raise AssertionError(
                    "one outer-context reference has two exact coordinate values"
                )

    shared_findings = [
        {
            "context_reference": reference,
            "left_material": first["contexts"][reference]["left_material"],
            "right_material": first["contexts"][reference]["right_material"],
            "left_scalar_count": first["contexts"][reference][
                "left_scalar_count"
            ],
            "right_scalar_count": first["contexts"][reference][
                "right_scalar_count"
            ],
            "first_support_populations": first["contexts"][reference][
                "support_populations"
            ],
            "second_support_populations": second["contexts"][reference][
                "support_populations"
            ],
        }
        for reference in sorted(shared)
    ]

    return {
        "comparison_reference": _digest(
            {
                "boundary": comparison_boundary,
                "first": first["branch_reference"],
                "second": second["branch_reference"],
            }
        ),
        "comparison_boundary": comparison_boundary,
        "first_branch_reference": first["branch_reference"],
        "second_branch_reference": second["branch_reference"],
        "first_internal_material": first["occupant_material"],
        "second_internal_material": second["occupant_material"],
        "shared_outer_contexts": shared_findings,
        "first_only_outer_context_population": {
            "operation": "first branch context population minus shared references",
            "count": len(first_only),
        },
        "second_only_outer_context_population": {
            "operation": "second branch context population minus shared references",
            "count": len(second_only),
        },
        "shared_nonempty_outer_context_references": nonempty(first, shared),
        "first_only_nonempty_outer_context_count": len(nonempty(first, first_only)),
        "second_only_nonempty_outer_context_count": len(
            nonempty(second, second_only)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variable-input", type=Path, default=VARIABLE_INPUT)
    parser.add_argument("--relation-input", type=Path, default=RELATION_INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--source", action="append", default=[])
    arguments = parser.parse_args()

    begun = time.perf_counter()
    variable = json.loads(arguments.variable_input.read_text(encoding="utf-8"))
    relations = json.loads(arguments.relation_input.read_text(encoding="utf-8"))
    materials: dict[str, dict[str, object]] = {}
    references_by_value: dict[str, str] = {}
    sources = []
    branch_index = {}
    material_branches: dict[str, list[dict]] = defaultdict(list)

    for source in variable["sources"]:
        if arguments.source and source["source"] not in arguments.source:
            continue
        source_begun = time.perf_counter()
        exact_bytes, _line_starts = _window(
            CORPUS.parent / source["source"], source["first_line"]
        )
        if _digest(exact_bytes) != source["material_sha256"]:
            raise ValueError("outer-context source differs from frozen source")
        text = exact_bytes.decode("utf-8")
        frames = []
        for frame in source["frames"]:
            branches = []
            for branch_number, branch in enumerate(frame["branches"], start=1):
                branch_begun = time.perf_counter()
                reference = _branch_reference(
                    source["source"], frame["frame_number"], branch_number, branch
                )
                occupant = source["materials"][branch["occupant_material"]]
                occupant_value = bytes.fromhex(occupant["utf8_hex"]).decode("utf-8")
                occupant_reference = _material_reference(
                    materials, references_by_value, occupant_value
                )
                contexts, context_families = _context_population_and_families(
                    text=text,
                    branch=branch,
                    materials=materials,
                    references_by_value=references_by_value,
                )
                branch_record = {
                    "branch_reference": reference,
                    "source": source["source"],
                    "frame_number": frame["frame_number"],
                    "branch_number": branch_number,
                    "occupant_material": occupant_reference,
                    "initial_occurrence_count": branch["initial_occurrence_count"],
                    "contexts": contexts,
                    "context_families": context_families,
                }
                branches.append(branch_record)
                branch_index[reference] = branch_record
                material_branches[occupant_reference].append(branch_record)
                print(
                    f"  frame={frame['frame_number']:3} branch={branch_number:3} "
                    f"contexts={len(branch_record['contexts']):7} "
                    f"{time.perf_counter() - branch_begun:.3f}s",
                    flush=True,
                )

            comparisons = []
            for first_position, first in enumerate(branches):
                for second in branches[first_position + 1 :]:
                    comparisons.append(
                        _comparison(
                            first,
                            second,
                            comparison_boundary=(
                                f"{source['source']}#frame-{frame['frame_number']}"
                            ),
                        )
                    )
            frames.append(
                {
                    "frame_number": frame["frame_number"],
                    "independently_varying_position_count": 1,
                    "branches": [
                        {
                            **{
                                key: value
                                for key, value in branch.items()
                                if key != "contexts"
                            },
                            "context_population_count": len(branch["contexts"]),
                        }
                        for branch in branches
                    ],
                    "branch_comparisons": comparisons,
                }
            )
        sources.append(
            {
                "source": source["source"],
                "first_line": source["first_line"],
                "line_count": source["line_count"],
                "material_sha256": source["material_sha256"],
                "frames": frames,
            }
        )
        print(
            f"{source['source']:48} frames={len(frames):3} "
            f"{time.perf_counter() - source_begun:.3f}s",
            flush=True,
        )

    repeated_material_comparisons = []
    for material_reference, branches in sorted(material_branches.items()):
        distinct_frame_boundaries = {
            (branch["source"], branch["frame_number"]) for branch in branches
        }
        if len(distinct_frame_boundaries) < 2:
            continue
        for first_position, first in enumerate(branches):
            for second in branches[first_position + 1 :]:
                if (first["source"], first["frame_number"]) == (
                    second["source"],
                    second["frame_number"],
                ):
                    continue
                repeated_material_comparisons.append(
                    _comparison(
                        first,
                        second,
                        comparison_boundary=(
                            "same exact internal material across distinct frames"
                        ),
                    )
                )

    nested_occupancies = []
    for occupancy in relations[
        "exact_extent_occupies_other_frame_position"
    ]:
        inner = branch_index.get(occupancy["extent_branch_reference"])
        outer = branch_index.get(occupancy["occupant_branch_reference"])
        if arguments.source and inner is None and outer is None:
            continue
        if inner is None or outer is None:
            raise ValueError("frozen occupancy does not resolve to exact branches")
        nested_occupancies.append(
            {
                **occupancy,
                "inner_frame_independently_varying_position_count": 1,
                "outer_frame_independently_varying_position_count": 1,
                "inner_outer_context_population_is_carried_by": inner[
                    "branch_reference"
                ],
                "outer_outer_context_population_is_carried_by": outer[
                    "branch_reference"
                ],
            }
        )

    finding = {
        "variable_extent_artifact_sha256": _digest(
            arguments.variable_input.read_bytes()
        ),
        "variable_extent_relation_artifact_sha256": _digest(
            arguments.relation_input.read_bytes()
        ),
        "operation": (
            "exact outer-context population comparison across naturally occurring "
            "internal frame branches"
        ),
        "materials": materials,
        "sources": sources,
        "same_internal_material_across_distinct_frames": (
            repeated_material_comparisons
        ),
        "nested_frame_occupancies": nested_occupancies,
        "known_loss": None,
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)

    frame_comparisons = [
        comparison
        for source in sources
        for frame in source["frames"]
        for comparison in frame["branch_comparisons"]
    ]
    print(f"\ninternal branch comparisons: {len(frame_comparisons)}")
    print(
        "comparisons sharing nonempty outer context: "
        f"{sum(bool(value['shared_nonempty_outer_context_references']) for value in frame_comparisons)}"
    )
    print(
        "same-material cross-frame comparisons: "
        f"{len(repeated_material_comparisons)}"
    )
    print(f"nested exact occupancies: {len(nested_occupancies)}")
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    print(f"complete wall seconds: {time.perf_counter() - begun:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
