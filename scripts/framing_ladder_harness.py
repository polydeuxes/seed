#!/usr/bin/env python3
"""Form material in which a byte grouping recurs rather than being declared.

The other ladders vary a coordinate within a framing. This one varies material
so that the framing itself recurs, because a specimen does not
carry one.

Raw bytes are raw bytes. That two of them are one sample, that the second
holds the high half, that the grouping starts at offset zero -- these are
coordinates the harness knows. A `.pcm` suffix and a `--period 800` argument
are the harness talking about its material, not the material.

**What the material carries instead.** Partition the bytes by offset under a
candidate stride. Each offset has an exact set of byte values measured at it,
and those sets are measurable without classifying them:

```text
  amplitude 100, stride 2   |support(2,0)| = 201    |support(2,1)| = 2
  amplitude 100, stride 3   144, 145, 172
  amplitude 100, stride 4   159, 2, 157, 2
  amplitude 8000, stride 2  198, 64
```

`201 != 2` is the measurement. What it is *about* -- that one offset holds a
high half, that the values at it are sign extension, that a stride of 2 is a
sample -- is not measured here and is not asserted here.

**The rule that would select a framing from this is unread.** Support
sizes differ at every stride and every amplitude above, so inequality alone
selects nothing. An earlier revision used a fourfold ratio, which chose stride
2 for no reason the material supplies; that threshold is withdrawn rather than
replaced by a different one.

**Phase is which source byte is treated as offset 0 of this partition.** Not
where a group begins: nothing here establishes that a group exists. Read from
byte zero the two classes at stride 2 are 201 values and 2; read from byte one
they are 2 and 201, and the sets trade places exactly.

The material's byte boundary is exact -- an occurrence begins at its first
byte and ends at its last. That boundary is not an internal one. A partition
starting at byte zero starts where the material does, which is a property of
the partition and not evidence that anything inside the material is bounded
there too.

What a rule would have to distinguish, once warranted:

```text
  candidate stride     its offsets' supports stand in some exact relation
  primitive candidate  a candidate stride no proper divisor of which is one
  partition phase      which source byte is offset 0 of the partition
  grouping             that adjacent positions representation a unit
  group boundary       where such a unit would begin and end
```

The second is what would separate stride 2 from stride 4, which agrees with it
because it is two of them. None is established.

The harness may still testify to how it supplied a specimen. That testimony
is attributed, and is not what makes the framing usable.

Usage:

    framing_ladder_harness.py --out-dir rungs/
    framing_ladder_harness.py --out-dir rungs/ --amplitudes 8000,2000,500,100,20
"""

from __future__ import annotations

import argparse
import math
import struct
from pathlib import Path

PERIOD_SAMPLES = 800


def block(amplitude: int) -> bytes:
    return b"".join(
        struct.pack("<h", int(amplitude * math.sin(2.0 * math.pi * i / PERIOD_SAMPLES)))
        for i in range(PERIOD_SAMPLES)
    )


def position_diversity(raw: bytes, width: int, phase: int = 0) -> dict[int, int]:
    """How many distinct byte values each offset carries under this stride."""

    return {
        offset: len(support)
        for offset, support in position_support(raw, width, phase).items()
    }


def position_support(
    raw: bytes, stride: int, phase: int = 0
) -> dict[int, frozenset[int]]:
    """The exact set of byte values at each offset, under a stride and a phase.

    A partition begins somewhere. Reading from byte zero is a fixed coordinate, and
    the same material read from byte one yields the same classes in reversed places, so
    positional recurrence at some stride does not say where a group starts.
    """

    body = raw[phase:]
    return {
        offset: frozenset(body[i] for i in range(offset, len(body), stride))
        for offset in range(stride)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--amplitudes", default="8000,2000,500,100,20")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    print(f"  {'specimen':26}{'bytes':>7}   support sizes by offset, per stride")
    for amplitude in (int(v) for v in args.amplitudes.split(",")):
        raw = block(amplitude)
        path = args.out_dir / f"F-amplitude{amplitude}.pcm"
        path.write_bytes(raw)
        measured = "   ".join(
            f"{stride}:{list(position_diversity(raw, stride).values())}"
            for stride in (2, 3, 4)
        )
        print(f"  {path.name:26}{len(raw):>7}   {measured}")
    print("\n  No stride is selected. Support sizes differ under every stride,")
    print("  so the rule that would choose one is unread.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
