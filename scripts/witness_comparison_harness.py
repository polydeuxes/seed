#!/usr/bin/env python3
"""Compare what witnesses made of the same material, and climb that.

Each decoding witness classifies the same 256 bytes, so their results are
comparable without anything being translated between them. One partition
refines another where every class of the first sits inside a class of the
second.

That relation is a witness in its own right, and the same climb rides it. Its
subjects are the previous climb's results:

```text
  bytes      -> classes        one climb per decoding witness
  classes    -> partitions     the results, collected
  partitions -> classes        this climb, over the refinement relation
```

Nothing is translated at any step. The second climb's subjects are the first
climb's outputs, and the third's are the second's.

What one machine's codecs yield:

```text
  103 witnesses, 46 distinct partitions
    1 partition everything refines, held by 50 witnesses
   38 partitions nothing refines
   71 comparable pairs of 1035 -- 7%
```

**Witnesses do not converge.** 93% of pairs are incomparable: neither cuts the
material more finely than the other, they cut it differently. There is one
trivial floor and thirty-eight maximal classifications above it, not a chain
toward some finest answer.
"""

from __future__ import annotations

import argparse
import collections

import refinement_climb as rc
from decoder_witness_harness import accepts, classes, decoding_witnesses

Partition = frozenset


def final_partition(codec: str) -> Partition:
    """Where this witness's own climb came to rest."""

    recovered = classes(codec, 4)
    rungs = rc.climb(
        [tuple(members) for members in recovered.values()],
        lambda first, second: accepts(codec, (first, second)),
    )
    return frozenset(frozenset(members) for members in rungs[-1])


def partitions() -> dict[Partition, list[str]]:
    """Each distinct resting classification, and the witnesses that reached it."""

    grouped: dict[Partition, list[str]] = collections.defaultdict(list)
    for name in decoding_witnesses():
        try:
            grouped[final_partition(name)].append(name)
        except Exception:
            continue
    return dict(grouped)


def refines(finer: Partition, coarser: Partition) -> bool:
    """Whether every class of one sits inside a class of the other."""

    return all(any(part <= whole for whole in coarser) for part in finer)


def order(found: dict[Partition, list[str]]) -> dict[str, int]:
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
        "partitions": len(keys),
        "finest": sum(1 for i in range(len(keys)) if above[i] == 0),
        "coarsest": sum(1 for i in range(len(keys)) if below[i] == 0),
        "comparable": comparable,
        "pairs": len(keys) * (len(keys) - 1) // 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    found = partitions()
    counted = order(found)
    witnesses = sum(len(names) for names in found.values())

    print(f"  {witnesses} witnesses -> {counted['partitions']} distinct partitions")
    print(f"  partitions nothing refines:  {counted['finest']}")
    print(f"  partitions refining nothing: {counted['coarsest']}")
    print(
        f"  comparable pairs: {counted['comparable']} of {counted['pairs']}"
        f"  ({counted['comparable'] / counted['pairs'] * 100:.0f}%)"
    )

    keys = sorted(found, key=len)
    rungs = rc.climb(rc.by(len, keys), refines, limit=64)
    print(f"\n  climbing those partitions under refinement: {len(rungs)} rungs")
    print(f"  heights {rc.heights(rungs)[:6]} ... {rc.heights(rungs)[-1]}")
    print(f"  left unseparated: {len(rc.unseparated(rungs))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
