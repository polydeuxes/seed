#!/usr/bin/env python3
"""Read the Book's own distinction statements as a witness about its terms.

Every chapter carries lines of the form `X != Y`. Asked about two terms, this
answers whether the Book holds them apart. That is testimony about the Book,
not about whatever the terms name.

The same refinement the codec witnesses ride applies here without change: the
subjects are terms rather than bytes, and the witness is a corpus rather than
a decoder.

Usage:

    book_grammar_witness.py
    book_grammar_witness.py --chapters
"""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path

import refinement_climb

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
                        match.group(1).lower().strip(),
                        match.group(2).lower().strip(),
                    )
                )
    return found


def held_apart() -> dict[str, set[str]]:
    """For each term, the terms the Book states it is not."""

    apart: dict[str, set[str]] = collections.defaultdict(set)
    for _, _, first, second in statements():
        apart[first].add(second)
        apart[second].add(first)
    return dict(apart)


def witness(apart: dict[str, set[str]]):
    """Whether the Book holds these two terms apart."""

    def answer(first: str, second: str) -> bool:
        return second in apart.get(first, ())

    return answer


def restated() -> dict[tuple[str, str], list[str]]:
    """Distinctions the Book states more than once, and where."""

    seen: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for chapter, number, first, second in statements():
        seen[(first, second)].append(f"{chapter}:{number}")
    return {pair: at for pair, at in seen.items() if len(at) > 1}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapters", action="store_true")
    args = parser.parse_args()

    said = statements()
    apart = held_apart()
    print(f"  {len(said)} statements, {len(apart)} terms")

    if args.chapters:
        counts = collections.Counter(chapter for chapter, _, _, _ in said)
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

    first = refinement_climb.by(lambda term: len(apart[term]), apart)
    rungs = refinement_climb.climb(first, witness(apart))
    print(f"\n  climb: {refinement_climb.heights(rungs)}")
    left = refinement_climb.unseparated(rungs)
    print(f"  {sum(len(c) for c in left)} terms in {len(left)} classes it never separated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
