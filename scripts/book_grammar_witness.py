#!/usr/bin/env python3
"""Compare exact Book distinction statements."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import material_admission

CHAPTERS = Path(__file__).resolve().parents[1] / "book_of_seed" / "chapters"
STATEMENT = re.compile(r"\s*-\s*(.+?)\s*!=\s*(.+?)\s*$")


def statements() -> list[tuple[str, int, str, str]]:
    """Each distinction the Book states, with where it states it."""

    found = []
    for path in sorted(CHAPTERS.glob("*.md")):
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            match = STATEMENT.match(line)
            if match:
                found.append(
                    (
                        path.name[:2],
                        number,
                        match[1].lower().strip(),
                        match[2].lower().strip(),
                    )
                )
    return found


def held_apart() -> dict[str, set[str]]:
    """For each term, the terms the Book states it is not."""

    apart: dict[str, set[str]] = {}
    for _, _, first, second in statements():
        apart.setdefault(first, set()).add(second)
        apart.setdefault(second, set()).add(first)
    return apart


def implementation_function(apart: dict[str, set[str]]):
    """Whether the Book holds these two terms apart."""

    def result(first: str, second: str) -> bool:
        return second in apart.get(first, ())

    return result


def restated() -> dict[tuple[str, str], list[str]]:
    """Distinctions the Book states more than once, and where."""

    seen: dict[tuple[str, str], list[str]] = {}
    for chapter, number, first, second in statements():
        seen.setdefault((first, second), []).append(f"{chapter}:{number}")
    return {pair: at for pair, at in seen.items() if len(at) > 1}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapters", action="store_true")
    args = parser.parse_args()

    said = statements()
    apart = held_apart()
    print(f"  {len(said)} statements, {len(apart)} terms")

    if args.chapters:
        counts: dict[str, int] = {}
        for chapter, _, _, _ in said:
            counts[chapter] = counts.get(chapter, 0) + 1
        for chapter, many in sorted(counts.items()):
            print(f"    {chapter}  {many}")
        return 0

    both_ways = [
        (first, second)
        for _, _, first, second in said
        if first in apart.get(second, ()) and (second, first) in {
            (a, b) for _, _, a, b in said
        }
    ]
    print(f"  stated in both directions: {len(both_ways)}")
    print(f"  stated more than once: {len(restated())}")
    for pair, at in restated().items():
        print(f"    {pair[0][:34]} != {pair[1][:28]}   at {', '.join(at)}")

    first = material_admission.admission_by(lambda term: len(apart[term]), apart)
    admissions = material_admission.admit(first, implementation_function(apart))
    print(f"\n  Admission counts: {material_admission.admission_counts(admissions)}")
    left = material_admission.not_distinguished(admissions)
    print(f"  {sum(len(c) for c in left)} terms in {len(left)} material tuples it never separated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
