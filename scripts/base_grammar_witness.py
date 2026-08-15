#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import material_admission

GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed" / "grammar.json"


def relations() -> dict[str, dict]:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["relations"]


def endpoints(declared: dict[str, dict]) -> list[str]:
    return sorted({end for spec in declared.values() for end in (spec["from"], spec["to"])})


def compositions(declared: dict[str, dict]) -> list[tuple[str, str]]:
    """Ordered relation pairs where the first ends where the second begins."""

    return [
        (first, second)
        for first, second in itertools.product(sorted(declared), repeat=2)
        if declared[first]["to"] == declared[second]["from"]
    ]


def links(declared: dict[str, dict]) -> list[tuple[str, str]]:
    """Ordered endpoint pairs some relation runs between."""

    return sorted({(spec["from"], spec["to"]) for spec in declared.values()})


def shared_requirements(declared: dict[str, dict]) -> bool:
    """Whether every relation states the same requirements."""

    return len({tuple(spec["requires"]) for spec in declared.values()}) == 1


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    declared = relations()
    ends = endpoints(declared)

    print(f"  {len(declared)} relations over {len(ends)} endpoints")
    print(f"  every relation states the same requirements: {shared_requirements(declared)}")
    print(
        f"  linked endpoint pairs: {len(links(declared))} of {len(ends) ** 2}"
        f"   compositions: {len(compositions(declared))} of {len(declared) ** 2}"
    )
    for first, second in compositions(declared):
        print(f"    {first} then {second}, meeting at {declared[first]['to']}")

    joined = {end for pair in links(declared) for end in pair}
    dangling = [
        name
        for name, spec in declared.items()
        if not any(other["from"] == spec["to"] for other in declared.values())
    ]
    print(f"  relations without a following relation: {dangling}")

    by_composition = material_admission.admit(
        material_admission.one_admission(sorted(declared)),
        lambda a, b: declared[a]["to"] == declared[b]["from"],
    )
    by_link = material_admission.admit(
        material_admission.one_admission(ends),
        lambda x, y: any(
            spec["from"] == x and spec["to"] == y for spec in declared.values()
        ),
    )
    print(
        "\n  relation Admission counts under composition: "
        f"{material_admission.admission_counts(by_composition)}"
    )
    print(
        "  endpoint Admission counts under linkage: "
        f"{material_admission.admission_counts(by_link)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
