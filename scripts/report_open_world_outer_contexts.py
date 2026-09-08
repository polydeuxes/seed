"""Render exact population relations from the frozen outer-context artifact."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path


INPUT = Path("/tmp/seed_open_world_outer_contexts_blind.json")
OUTPUT = Path("/tmp/seed_open_world_outer_context_pressure.json")


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


def _digest(value: object) -> str:
    material = value if isinstance(value, bytes) else _canonical(value)
    return sha256(material).hexdigest()


def _decode(materials: dict, reference: str) -> str:
    return bytes.fromhex(materials[reference]["utf8_hex"]).decode("utf-8")


def _render(value: str) -> str:
    return value.encode("unicode_escape").decode("ascii")


def _population_relation(comparison: dict) -> str:
    first_only = comparison["first_only_outer_context_population"]["count"]
    second_only = comparison["second_only_outer_context_population"]["count"]
    if first_only == 0 and second_only == 0:
        return "equal"
    if first_only == 0:
        return "first proper subset of second"
    if second_only == 0:
        return "second proper subset of first"
    return "partial overlap"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()

    observation = json.loads(arguments.input.read_text(encoding="utf-8"))
    materials = observation["materials"]
    branch_index = {
        branch["branch_reference"]: branch
        for source in observation["sources"]
        for frame in source["frames"]
        for branch in frame["branches"]
    }
    comparisons = [
        comparison
        for source in observation["sources"]
        for frame in source["frames"]
        for comparison in frame["branch_comparisons"]
    ]

    relation_counts = Counter(_population_relation(value) for value in comparisons)
    rendered_comparisons = []
    shared_context_support: dict[str, dict] = {}
    shared_context_comparisons: dict[str, set[str]] = defaultdict(set)
    for comparison in comparisons:
        first = branch_index[comparison["first_branch_reference"]]
        second = branch_index[comparison["second_branch_reference"]]
        relation = _population_relation(comparison)
        rendered_comparisons.append(
            {
                "comparison_reference": comparison["comparison_reference"],
                "comparison_boundary": comparison["comparison_boundary"],
                "first_branch_reference": comparison["first_branch_reference"],
                "second_branch_reference": comparison["second_branch_reference"],
                "first_internal_material": comparison["first_internal_material"],
                "second_internal_material": comparison["second_internal_material"],
                "first_context_population_count": first[
                    "context_population_count"
                ],
                "second_context_population_count": second[
                    "context_population_count"
                ],
                "shared_context_count": len(comparison["shared_outer_contexts"]),
                "shared_nonempty_context_count": len(
                    comparison["shared_nonempty_outer_context_references"]
                ),
                "first_only_context_count": comparison[
                    "first_only_outer_context_population"
                ]["count"],
                "second_only_context_count": comparison[
                    "second_only_outer_context_population"
                ]["count"],
                "exact_population_relation": relation,
            }
        )
        for context in comparison["shared_outer_contexts"]:
            if not (context["left_scalar_count"] or context["right_scalar_count"]):
                continue
            reference = context["context_reference"]
            definition = {
                key: value
                for key, value in context.items()
                if key not in {"first_support_populations", "second_support_populations"}
            }
            if reference in shared_context_support and shared_context_support[
                reference
            ] != definition:
                raise AssertionError("one outer-context reference has two definitions")
            shared_context_support[reference] = definition
            shared_context_comparisons[reference].add(
                comparison["comparison_reference"]
            )

    recurrent_shared_contexts = [
        {
            **shared_context_support[reference],
            "comparison_count": len(comparison_references),
            "comparison_references": sorted(comparison_references),
        }
        for reference, comparison_references in sorted(
            shared_context_comparisons.items()
        )
        if len(comparison_references) > 1
    ]

    same_material = []
    for comparison in observation[
        "same_internal_material_across_distinct_frames"
    ]:
        first = branch_index[comparison["first_branch_reference"]]
        second = branch_index[comparison["second_branch_reference"]]
        same_material.append(
            {
                "comparison_reference": comparison["comparison_reference"],
                "internal_material": comparison["first_internal_material"],
                "first_branch_reference": comparison["first_branch_reference"],
                "second_branch_reference": comparison["second_branch_reference"],
                "first_context_population_count": first[
                    "context_population_count"
                ],
                "second_context_population_count": second[
                    "context_population_count"
                ],
                "shared_context_count": len(comparison["shared_outer_contexts"]),
                "shared_nonempty_context_count": len(
                    comparison["shared_nonempty_outer_context_references"]
                ),
                "first_only_context_count": comparison[
                    "first_only_outer_context_population"
                ]["count"],
                "second_only_context_count": comparison[
                    "second_only_outer_context_population"
                ]["count"],
                "exact_population_relation": _population_relation(comparison),
            }
        )

    finding = {
        "outer_context_artifact_sha256": _digest(arguments.input.read_bytes()),
        "comparison_count": len(comparisons),
        "population_relation_counts": dict(sorted(relation_counts.items())),
        "comparisons": rendered_comparisons,
        "recurrent_shared_outer_contexts": recurrent_shared_contexts,
        "same_internal_material_across_distinct_frames": same_material,
        "nested_exact_occupancy_count": len(
            observation["nested_frame_occupancies"]
        ),
        "nested_exact_occupancy_sources": sorted(
            {
                value["source"] for value in observation["nested_frame_occupancies"]
            }
        ),
        "independently_varying_position_counts": sorted(
            {
                frame["independently_varying_position_count"]
                for source in observation["sources"]
                for frame in source["frames"]
            }
        ),
    }
    encoded = _canonical(finding)
    arguments.output.write_bytes(encoded)

    print(f"comparisons: {finding['comparison_count']}")
    print(f"population relations: {finding['population_relation_counts']}")
    print("most recurrent shared nonempty contexts:")
    for context in sorted(
        recurrent_shared_contexts,
        key=lambda value: (-value["comparison_count"], value["context_reference"]),
    )[:12]:
        print(
            f"  {context['comparison_count']:2}  "
            f"({_render(_decode(materials, context['left_material']))!r}, "
            f"{_render(_decode(materials, context['right_material']))!r})"
        )
    print("same exact internal material across distinct frames:")
    for comparison in same_material:
        print(
            f"  {_render(_decode(materials, comparison['internal_material']))!r}  "
            f"contexts={comparison['first_context_population_count']}/"
            f"{comparison['second_context_population_count']} "
            f"shared={comparison['shared_context_count']} "
            f"only={comparison['first_only_context_count']}/"
            f"{comparison['second_only_context_count']}"
        )
    print(f"artifact: {arguments.output}")
    print(f"artifact bytes: {len(encoded)}")
    print(f"findings sha256: {_digest(encoded)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
