#!/usr/bin/env python3
"""Form frames that differ from each other in one stated way at a time.

Material whose differences are known before Seed reads it. Each rung adds one
thing to the rung below, so a comparison between two of them has a expected
answer a caller can check its finding against.

```text
  1  one colour                     the frame's area, 1 distinct value
  2  a smaller box inside it        the box's exact area leaves the ground
  3  one letter inside the box      ink appears where box was
  4  five letters inside the box    more ink, and not five times the one
```

Frame size and box size vary separately, so a comparison that reports only
"the ground shrank" cannot tell which of the two moved. Ground area is the
frame's area less the box's, and both are declared here.

Rung 4 is not rung 3 five times over. Letters carry different amounts of ink,
and antialiasing puts colours in the frame that neither the ground nor the ink
was given. Both are measurable, and neither was declared.

This script represents the material under the operator's authority in a
subprocess. What occurs afterwards is a file, and it enters through the
material path like any other body.

Usage:

    visual_ladder_harness.py --out-dir rungs/
    visual_ladder_harness.py --out-dir rungs/ --text hello --seconds 2
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

# Supplied descriptions, not Seed grammar. A specimen carries pixel values
# and pixel dimensions; `ground`, `box` and `ink` are how this harness built them.
GROUND = "red"
BOX = "black"
INK = "white"

# Below objects: one frame, one value, nothing else moving. Written as PNG
# rather than H.264, because the encoder perturbs exact pixel equality and
# these exist for exact comparison.
VALUES = ("0x000000", "0x808080", "0xffffff")


def value_ladder(out_dir: Path, size: str, values: tuple[str, ...]) -> list[Path]:
    """Pixel value varies. Pixel dimensions and encoding do not."""

    written = []
    for value in values:
        out = out_dir / f"V-{value}.png"
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-y",
             "-f", "lavfi", "-i", f"color=c={value}:s={size}:d=1",
             "-frames:v", "1", str(out)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            raise SystemExit(
                f"{value} failed: " + result.stderr.decode("utf-8", "replace")[-400:]
            )
        written.append(out)
    return written
def _draw_box(frame: str, box: str) -> str:
    """A box of this exact area, centred, whatever the frame around it is."""

    width, height = (int(value) for value in box.split("x"))
    return (
        f"drawbox=x=(iw-{width})/2:y=(ih-{height})/2"
        f":w={width}:h={height}:color={BOX}:t=fill"
    )


def _draw_text(text: str) -> str:
    return (
        f"drawtext=text='{text}':fontcolor={INK}:fontsize=64"
        ":x=(w-tw)/2:y=(h-th)/2"
    )


def rungs(text: str, frame: str, box: str) -> list[tuple[str, str]]:
    """Each rung's name and the filter that separates it from the one below."""

    drawn = _draw_box(frame, box)
    return [
        (f"{frame}_ground", ""),
        (f"{frame}_box{box}", drawn),
        (f"{frame}_box{box}_one", f"{drawn},{_draw_text(text[0])}"),
        (f"{frame}_box{box}_all", f"{drawn},{_draw_text(text)}"),
    ]


def emit_visual_material(name: str, filters: str, out_dir: Path, size: str, seconds: float) -> Path:
    out = out_dir / f"{name}.mp4"
    command = [
        "ffmpeg", "-v", "error", "-y",
        "-f", "lavfi", "-i", f"color=c={GROUND}:s={size}:d={seconds}",
    ]
    if filters:
        command += ["-vf", filters]
    command += ["-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise SystemExit(
            f"{name} failed: " + result.stderr.decode("utf-8", "replace")[-400:]
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--text", default="hello")
    parser.add_argument("--sizes", default="320x240,640x480")
    parser.add_argument("--boxes", default="200x120,100x60")
    parser.add_argument("--seconds", type=float, default=1.0)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for out in value_ladder(args.out_dir, args.sizes.split(",")[0], VALUES):
        print(f"{out.name:26} {out.stat().st_size:7} bytes")
    seen: set[str] = set()
    for frame in args.sizes.split(","):
        for box in args.boxes.split(","):
            for name, filters in rungs(args.text, frame, box):
                if name in seen:
                    continue
                seen.add(name)
                out = emit_visual_material(name, filters, args.out_dir, frame, args.seconds)
                print(f"{name:26} {out.stat().st_size:7} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
