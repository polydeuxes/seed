#!/usr/bin/env python3
"""Form speech material from supplied writing outside Seed.

Companion to `system_material_harness.py`, and the same line runs through it:
this script performs the synthesis, under the operator's authority, in a
subprocess. Seed neither invokes it nor speaks. What occurs afterwards is a
file, and it enters through the material path like any other body.

The supplied speech is not a read of the writing. A voice, a speaking rate, and a
sample rate are choices this script made, and none of them is carried by the
text they were applied to. Two renderings of one sentence are two materials
whose only addressable relation is that a caller declared the same source text
for both.

Usage:

    speech_material_harness.py --text hello --out hello.wav
    speech_material_harness.py --file chapter.txt --out chapter.wav --subtitles chapter.srt
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

DEFAULT_VOICE = "en_US-lessac-medium"
VOICE_DIR = Path.home() / ".local" / "share" / "piper-voices"


def emit_speech_material(text: str, out: Path, *, voice: str) -> None:
    """Write one spoken result from this exact material."""

    model = voice if voice.endswith(".onnx") else str(VOICE_DIR / f"{voice}.onnx")
    if not Path(model).exists():
        raise SystemExit(
            f"no voice at {model}. Fetch one with:\n"
            f"  python -m piper.download_voices {voice}\n"
            f"and move the .onnx and .onnx.json into {VOICE_DIR}"
        )
    piper = Path(sys.executable).with_name("piper")
    result = subprocess.run(
        [
            str(piper) if piper.exists() else "piper",
            "-m",
            model,
            "-f",
            str(out),
        ],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode != 0 or not out.exists():
        raise SystemExit(
            f"synthesis failed ({result.returncode}): "
            + result.stderr.decode("utf-8", "replace")[-400:]
        )


def duration_seconds(path: Path) -> float:
    """How long the supplied material runs, read from the file itself."""

    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return float(probe.stdout.decode().strip())


def write_subtitles(text: str, seconds: float, out: Path) -> None:
    """One cue spanning the whole supplied material.

    The cue spans the audio's exact time boundary. Nothing here knows where
    within the supplied material any word falls, and a cue per sentence would
    assert timings no measurement supplied.
    """

    milliseconds = int(seconds * 1000)
    out.write_text(
        "1\n00:00:00,000 --> "
        f"00:00:{milliseconds // 1000:02d},{milliseconds % 1000:03d}\n"
        f"{text}\n",
        encoding="utf-8",
    )


def write_video(audio: Path, subtitles: Path, out: Path, seconds: float) -> None:
    """A still frame carrying the subtitles for the audio's full duration."""

    result = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y",
            "-f", "lavfi", "-i", f"color=c=0x1a1a2e:s=640x360:d={seconds}",
            "-i", str(audio),
            "-vf",
            f"subtitles={subtitles}:force_style='FontSize=48,PrimaryColour=&H00FFFFFF&'",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
            str(out),
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise SystemExit(
            "video failed: " + result.stderr.decode("utf-8", "replace")[-400:]
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--file", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--subtitles", type=Path)
    parser.add_argument("--video", type=Path)
    args = parser.parse_args()

    text = args.text if args.text is not None else args.file.read_text(encoding="utf-8")
    emit_speech_material(text, args.out, voice=args.voice)
    seconds = duration_seconds(args.out)

    subtitles = args.subtitles
    if args.video is not None and subtitles is None:
        subtitles = args.out.with_suffix(".srt")
    if subtitles is not None:
        write_subtitles(text, seconds, subtitles)
    if args.video is not None:
        write_video(args.out, subtitles, args.video, seconds)

    print(f"audio       {args.out}  {args.out.stat().st_size} bytes  {seconds:.3f}s")
    print(f"voice       {args.voice}  rate {args.rate}")
    if subtitles is not None:
        print(f"subtitles   {subtitles}")
    if args.video is not None:
        print(f"video       {args.video}  {args.video.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
