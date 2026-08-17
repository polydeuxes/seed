#!/usr/bin/env python3
"""Render audio material where one measurable coordinate changes at a time.

The harness knows how it constructed each specimen. Seed receives only the
material. Nothing here names what the difference between two specimens means.

Every coordinate is held fixed except the one a ladder varies:

```text
  A   occurrence count      one, two, three occurrences at 60 Hz
  B   frequency             one occurrence at 1 Hz, 60 Hz, 120 Hz
```

Sample rate, amplitude, channel count, sample width, and the duration of each
occurrence are identical across every specimen either ladder renders. A
difference between two of them is the coordinate its ladder varies, and
nothing else.

**Samples are written, not encoded.** The visual ladder found that H.264
perturbs exact pixel equality, so two frames differing only by compression
compare unequal. Uncompressed PCM has no such step: identical construction
gives identical bytes, and a Compare over these specimens can be exact
without a tolerance nothing established.

Sequential occurrences and simultaneous components are different material and
are not mixed here. Repeating an occurrence three times is ladder A. Sounding
three frequencies at once is a different candidate relation and gets its own
ladder when there is a reason to build one.

Usage:

    audio_ladder.py --out-dir rungs/
    audio_ladder.py --out-dir rungs/ --frequencies 1,60,120 --counts 1,2,3
"""

from __future__ import annotations

import argparse
import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 48000
SAMPLE_WIDTH = 2
CHANNELS = 1
AMPLITUDE = 8000
OCCURRENCE_SECONDS = 0.25
SILENCE_SECONDS = 0.25
BASE_FREQUENCY = 60.0


def occurrence_material(frequency: float) -> bytes:
    """One occurrence: exact samples, no encoder between them and the file."""

    count = int(SAMPLE_RATE * OCCURRENCE_SECONDS)
    return b"".join(
        struct.pack(
            "<h",
            int(AMPLITUDE * math.sin(2.0 * math.pi * frequency * index / SAMPLE_RATE)),
        )
        for index in range(count)
    )


def _silence() -> bytes:
    return b"\x00\x00" * int(SAMPLE_RATE * SILENCE_SECONDS)


def write_wave(path: Path, frames: bytes) -> None:
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(CHANNELS)
        handle.setsampwidth(SAMPLE_WIDTH)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(frames)


def count_ladder(out_dir: Path, counts: list[int]) -> list[Path]:
    """Occurrence count varies. Frequency, and everything else, does not."""

    written = []
    single = occurrence_material(BASE_FREQUENCY)
    gap = _silence()
    for count in counts:
        frames = gap.join([single] * count)
        path = out_dir / f"A-{count}x{BASE_FREQUENCY:g}hz.wav"
        write_wave(path, frames)
        written.append(path)
    return written


def frequency_ladder(out_dir: Path, frequencies: list[float]) -> list[Path]:
    """Frequency varies. Occurrence count, and everything else, does not."""

    written = []
    for frequency in frequencies:
        path = out_dir / f"B-1x{frequency:g}hz.wav"
        write_wave(path, occurrence_material(frequency))
        written.append(path)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--counts", default="1,2,3")
    parser.add_argument("--frequencies", default="1,60,120")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    counts = [int(value) for value in args.counts.split(",")]
    frequencies = [float(value) for value in args.frequencies.split(",")]

    for path in count_ladder(args.out_dir, counts) + frequency_ladder(
        args.out_dir, frequencies
    ):
        print(f"{path.name:22} {path.stat().st_size:8} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
