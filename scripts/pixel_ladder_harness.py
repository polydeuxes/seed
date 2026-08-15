#!/usr/bin/env python3
"""Form pixel material where one measurable coordinate differs at a time.

The harness knows how it supplied each specimen. Seed receives only the
material. Nothing here names what a difference between two specimens means.

**Raw channel bytes, no container and no encoder.** PNG is lossless, which
escapes the H.264 problem of two frames differing only by compression, but it
is still an encoding: the bytes are compressed PNG, not the values. A specimen
here is exactly its channel bytes.

```text
  P   one pixel, three values      000000, 808080, ffffff
  C   one channel varies           00 00 00, 01 00 00 ... ff 00 00
                                   then the second, then the third
```

Ladder P is the floor: three bytes, differing in all three. Ladder C moves one
channel and holds the other two, once per channel, so each channel is a
coordinate addressable on its own before any two are crossed.

The pixel dimensions do not vary here. One pixel is the whole specimen, so a
difference between two specimens is a value, not a pixel dimension.

Three distinct coordinates are not the space they span. Ladder C represents
256 specimens per channel, 768 in all; the crossed space is 256 x 256 x 256,
16,777,216 combinations. Read each coordinate alone is what makes the
crossed space addressable without enumerating every specimen.

**A specimen does not carry its own framing.** Three bytes are three bytes.
That the first is one channel, that the three together are one pixel, and that
a channel is a whole byte, are all coordinates this harness knows and no
specimen states. See `framing_ladder_harness.py`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

CHANNELS = ("r", "g", "b")


def pixel_ladder(out_dir: Path, values: list[int]) -> list[Path]:
    """One pixel whose three channels carry one value each."""

    written = []
    for value in values:
        path = out_dir / f"P-{value:02x}{value:02x}{value:02x}.rgb"
        path.write_bytes(bytes((value, value, value)))
        written.append(path)
    return written


def channel_ladder(out_dir: Path, step: int) -> list[Path]:
    """One channel varies across its whole range. The other two hold at zero."""

    written = []
    for position, channel in enumerate(CHANNELS):
        for value in list(range(0, 256, step)) + ([255] if 255 % step else []):
            sample = [0, 0, 0]
            sample[position] = value
            path = out_dir / f"C-{channel}-{value:02x}.rgb"
            path.write_bytes(bytes(sample))
            written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--values", default="0,128,255")
    parser.add_argument(
        "--step",
        type=int,
        default=85,
        help="channel-ladder stride; 1 represents every value of every channel",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    values = [int(value) for value in args.values.split(",")]

    pixels = pixel_ladder(args.out_dir, values)
    channels = channel_ladder(args.out_dir, args.step)
    for path in pixels:
        print(f"{path.name:20} {path.read_bytes().hex(' ')}")
    print(f"\n{len(channels)} channel specimens at step {args.step}")
    print(f"every specimen is {len(pixels[0].read_bytes())} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
