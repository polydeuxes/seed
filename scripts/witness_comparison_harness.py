#!/usr/bin/env python3
"""Compare what witnesses made of the same material, and climb that.

Each decoding witness yields one material Locality over the same 256 bytes, so
their results are comparable without translation. One material Locality
refines another where every exact material tuple of the first is contained by one exact material tuple of the
second.

That relation is a witness in its own right, and the same climb rides it. Its
material is the previous climb's results:

```text
  bytes               -> material Localities
  material Localities -> material Localities
  material Localities -> material Localities
```

Nothing is translated at any step. The second climb's material is the first
climb's outputs, and the third's are the second's.

What one machine's codecs yield:

```text
  103 witnesses, 46 distinct material Localities
    1 material Locality everything refines, held by 50 witnesses
   38 material Localities nothing refines
   71 comparable pairs of 1035 -- 7%
```

**Witnesses do not converge.** 93% of pairs are incomparable: neither cuts the
material more finely than the other, they cut it differently. There is one
trivial floor and thirty-eight maximal material Localities above it, not a chain
toward some finest result.
"""

from __future__ import annotations

import argparse
import collections

import refinement_climb as rc
from decoder_witness_harness import accepts, material_locality, decoding_witnesses

MaterialLocality = frozenset


def final_material_locality(codec: str) -> MaterialLocality:
    """Where this witness's own climb came to rest."""

    read = material_locality(codec, 4)
    localities = rc.climb(
        [tuple(material) for material in read.values()],
        lambda first, second: accepts(codec, (first, second)),
    )
    return frozenset(frozenset(material) for material in localities[-1])


def material_localities() -> dict[MaterialLocality, list[str]]:
    """Each distinct resting material Locality and its witnesses."""

    grouped: dict[MaterialLocality, list[str]] = collections.defaultdict(list)
    for name in decoding_witnesses():
        try:
            grouped[final_material_locality(name)].append(name)
        except Exception:
            continue
    return dict(grouped)


def refines(finer: MaterialLocality, coarser: MaterialLocality) -> bool:
    """Whether every exact material tuple of one is contained by one tuple of the other."""

    return all(any(part <= whole for whole in coarser) for part in finer)


def order(found: dict[MaterialLocality, list[str]]) -> dict[str, int]:
    """How the refinement relation arranges them."""

    keys = list(found)
    above = collections.Counter()
    below = collections.Counter()
    for i, first in enumerate(keys):
        for j, second in enumerate(keys):
            if i != j and refines(first, second):
                below[i] += 1
                above[j] += 1
    comparable = sum(
        1
        for i in range(len(keys))
        for j in range(i + 1, len(keys))
        if refines(keys[i], keys[j]) or refines(keys[j], keys[i])
    )
    return {
        "material_localities": len(keys),
        "finest": sum(1 for i in range(len(keys)) if above[i] == 0),
        "coarsest": sum(1 for i in range(len(keys)) if below[i] == 0),
        "comparable": comparable,
        "pairs": len(keys) * (len(keys) - 1) // 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    found = material_localities()
    counted = order(found)
    witnesses = sum(len(names) for names in found.values())

    print(f"  {witnesses} witnesses -> {counted['material_localities']} distinct material Localities")
    print(f"  material Localities nothing refines:  {counted['finest']}")
    print(f"  material Localities refining nothing: {counted['coarsest']}")
    print(
        f"  comparable pairs: {counted['comparable']} of {counted['pairs']}"
        f"  ({counted['comparable'] / counted['pairs'] * 100:.0f}%)"
    )

    keys = sorted(found, key=len)
    localities = rc.climb(rc.by(len, keys), refines)
    print(
        "\n  material Localities under refinement: "
        f"{len(localities)}"
    )
    print(
        f"  counts {rc.heights(localities)[:6]} ... {rc.heights(localities)[-1]}"
    )
    print(f"  left unseparated: {len(rc.unseparated(localities))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
