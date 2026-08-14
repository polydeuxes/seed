#!/usr/bin/env python3
"""Render sample material where one measurable coordinate changes at a time.

The harness knows how it constructed each specimen. Seed receives only the
material. Nothing here names what a difference between two specimens means.

**Raw samples, no container.** A WAV header carries the sample count in its
RIFF and data length fields, so a ladder varying only the number of samples
changes the header too, and a Compare over whole files sees two coordinates
move. These files are little-endian signed 16-bit samples and nothing else.

**Period length in samples is what a specimen carries.** Frequency is a
relation between that length and a separately declared sample rate --
`sample_rate / period_length` -- and composing it is not this harness's to do.

```text
  A   repetition       one exact 800-sample block, once, twice, three times
  B   period length    one exact block of 48000, 800, 400 samples
```

Ladder A holds the block identical and varies how many times it occurs, with
nothing between the repeats. Ladder B holds the repeat count at one and varies
how long the block is. A specimen in either is a whole number of periods, so
neither ladder moves cycle count and period length together.
"""

from __future__ import annotations

import argparse
import math
import struct
from pathlib import Path

SAMPLE_RATE = 48000
AMPLITUDE = 8000
BASE_PERIOD_SAMPLES = 800


def periodic_block(period_samples: int) -> bytes:
    """Exactly one period, as little-endian signed 16-bit samples."""

    return b"".join(
        struct.pack(
            "<h",
            int(AMPLITUDE * math.sin(2.0 * math.pi * index / period_samples)),
        )
        for index in range(period_samples)
    )


def repetition_ladder(out_dir: Path, counts: list[int]) -> list[Path]:
    """How many times the block occurs varies. The block does not."""

    block = periodic_block(BASE_PERIOD_SAMPLES)
    written = []
    for count in counts:
        path = out_dir / f"A-{count}x{BASE_PERIOD_SAMPLES}samples.pcm"
        path.write_bytes(block * count)
        written.append(path)
    return written


def period_ladder(out_dir: Path, periods: list[int]) -> list[Path]:
    """How long one period is varies. The count of periods does not."""

    written = []
    for period in periods:
        path = out_dir / f"B-1x{period}samples.pcm"
        path.write_bytes(periodic_block(period))
        written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--counts", default="1,2,3")
    parser.add_argument("--periods", default="48000,800,400")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    counts = [int(value) for value in args.counts.split(",")]
    periods = [int(value) for value in args.periods.split(",")]

    for path in repetition_ladder(args.out_dir, counts) + period_ladder(
        args.out_dir, periods
    ):
        print(f"{path.name:28} {path.stat().st_size:8} bytes")
    print(
        f"\nsample rate {SAMPLE_RATE} is declared here, not carried by any specimen."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
