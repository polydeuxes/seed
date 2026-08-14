#!/usr/bin/env python3
"""The three structural edges at the Book's base, as a witness about themselves.

`grammar.json` declares three edges. Asked what separates them, their stated
requirements do not: all three require exact_relation, occurrence_witness and
intact_evidence, and nothing else is listed. What differs is where each runs
from and to.

```text
  locality       content         -> occurrence
  participation  subject         -> Act_occurrence
  yield          Act_occurrence  -> result
```

Five endpoints, three edges, so twenty-five ordered endpoint pairs of which
three are linked, and nine ordered edge pairs of which one composes:

```text
  participation ends at Act_occurrence, where yield begins
```

**Locality joins nothing.** It ends at `occurrence`, and no edge begins there.
The Book's prose says Locality is "the exact evidenced relation from content to
the occurrence that carries it", and separately holds `act occurrence` apart
from `recording occurrence`, so an Act occurrence reads as one kind of
occurrence. `grammar.json` states no relation between the two names, so to
anything reading it the graph is disconnected.

**The edges do not separate under composition.** Climbing them by whether one
ends where another begins yields one class: composition says nothing that
tells locality from yield. The endpoints climb to five classes in four rungs.
So the structure such as it is lives in the endpoints, not the edges.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import refinement_climb as rc

GRAMMAR = Path(__file__).resolve().parents[1] / "book_of_seed" / "grammar.json"


def edges() -> dict[str, dict]:
    return json.loads(GRAMMAR.read_text(encoding="utf-8"))["structural_edges"]


def endpoints(declared: dict[str, dict]) -> list[str]:
    return sorted({end for spec in declared.values() for end in (spec["from"], spec["to"])})


def compositions(declared: dict[str, dict]) -> list[tuple[str, str]]:
    """Ordered edge pairs where the first ends where the second begins."""

    return [
        (first, second)
        for first, second in itertools.product(sorted(declared), repeat=2)
        if declared[first]["to"] == declared[second]["from"]
    ]


def links(declared: dict[str, dict]) -> list[tuple[str, str]]:
    """Ordered endpoint pairs some edge runs between."""

    return sorted({(spec["from"], spec["to"]) for spec in declared.values()})


def shared_requirements(declared: dict[str, dict]) -> bool:
    """Whether every edge states the same requirements."""

    return len({tuple(spec["requires"]) for spec in declared.values()}) == 1


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    declared = edges()
    ends = endpoints(declared)

    print(f"  {len(declared)} edges over {len(ends)} endpoints")
    print(f"  every edge states the same requirements: {shared_requirements(declared)}")
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
    print(f"  edges no other edge follows: {dangling}")

    by_composition = rc.climb(
        rc.one_class(sorted(declared)),
        lambda a, b: declared[a]["to"] == declared[b]["from"],
    )
    by_link = rc.climb(
        rc.one_class(ends),
        lambda x, y: any(
            spec["from"] == x and spec["to"] == y for spec in declared.values()
        ),
    )
    print(f"\n  edges climbed under composition: {rc.heights(by_composition)}")
    print(f"  endpoints climbed under linkage:  {rc.heights(by_link)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
