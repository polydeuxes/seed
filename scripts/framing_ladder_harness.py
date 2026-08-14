#!/usr/bin/env python3
"""Render material in which a byte grouping is recoverable rather than declared.

The other ladders vary a coordinate within a framing. This one varies material
so that the framing itself becomes recoverable, because a specimen does not
carry one.

Raw bytes are raw bytes. That two of them are one sample, that the second
holds the high half, that the grouping starts at offset zero -- these are
coordinates the harness knows. A `.pcm` suffix and a `--period 800` argument
are the harness talking about its material, not the material.

**What the material can carry instead.** Under the true grouping, byte
positions do not behave alike. Given samples whose magnitudes stay small, the
high byte carries only sign extension while the low byte varies freely:

```text
  amplitude 100, grouped by 2   position 0: 201 distinct values
                                position 1:   2
  amplitude 100, grouped by 3   position 0: 144   1: 145   2: 172
```

Width 3 is flat, so it explains nothing. Width 2 is the smallest width whose
positions differ markedly, and width 4 agrees with it because it is two of
them. The grouping is then a finding about the material rather than a fact
supplied with it.

An amplitude near the sample width's range hides this -- at 8000 the high byte
takes 64 values and the asymmetry is much weaker. So the ladder renders a
descent, and the recovery gets easier as it goes.

The harness may still testify to how it constructed a specimen. That testimony
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


def position_diversity(raw: bytes, width: int) -> dict[int, int]:
    """Distinct byte values at each position, under a candidate grouping."""

    return {
        offset: len({raw[i] for i in range(offset, len(raw), width)})
        for offset in range(width)
    }


def recovered_width(raw: bytes, widths: tuple[int, ...] = (1, 2, 3, 4, 6, 8)) -> int | None:
    """The smallest candidate width whose positions differ markedly.

    A width whose positions all carry a similar spread of values explains
    nothing about the material. Returns nothing where no candidate does.
    """

    for width in widths:
        if width == 1:
            continue
        spread = position_diversity(raw, width)
        if min(spread.values()) * 4 <= max(spread.values()):
            return width
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--amplitudes", default="8000,2000,500,100,20")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    print(f"  {'specimen':28}{'bytes':>8}{'recovered width':>17}  positions under it")
    for amplitude in (int(v) for v in args.amplitudes.split(",")):
        raw = block(amplitude)
        path = args.out_dir / f"F-amplitude{amplitude}.pcm"
        path.write_bytes(raw)
        width = recovered_width(raw)
        spread = position_diversity(raw, width) if width else {}
        print(f"  {path.name:28}{len(raw):>8}{str(width):>17}  {spread}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
