from __future__ import annotations

from dataclasses import dataclass
import math
import struct
import subprocess


@dataclass(frozen=True, slots=True)
class SuppliedMaterial:
    testimony: str
    exact_material: bytes


def _run(invocation: tuple[str, ...], exact_material: bytes) -> bytes:
    completed = subprocess.run(
        invocation,
        input=exact_material,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def _periodic_material(period: int) -> bytes:
    return b"".join(
        struct.pack(
            "<h",
            int(8000 * math.sin(2.0 * math.pi * position / period)),
        )
        for position in range(period)
    )


def _audio_material() -> tuple[SuppliedMaterial, ...]:
    first = _periodic_material(800)
    second = _periodic_material(400)
    mp3 = _run(
        (
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-f",
            "s16le",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-i",
            "pipe:0",
            "-map_metadata",
            "-1",
            "-f",
            "mp3",
            "pipe:1",
        ),
        first * 4,
    )
    ogg = _run(
        (
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-f",
            "s16le",
            "-ar",
            "48000",
            "-ac",
            "1",
            "-i",
            "pipe:0",
            "-map_metadata",
            "-1",
            "-c:a",
            "libopus",
            "-f",
            "ogg",
            "pipe:1",
        ),
        second * 8,
    )
    return (
        SuppliedMaterial("pcm-a", first),
        SuppliedMaterial("pcm-a-again", first),
        SuppliedMaterial("pcm-b", second),
        SuppliedMaterial("mp3", mp3),
        SuppliedMaterial("ogg-opus", ogg),
    )


def _photo_material() -> tuple[SuppliedMaterial, ...]:
    first = bytes(
        (
            0,
            0,
            0,
            255,
            0,
            0,
            0,
            255,
            0,
            0,
            0,
            255,
        )
    )
    second = bytes(
        (
            255,
            255,
            255,
            128,
            128,
            128,
            64,
            64,
            64,
            0,
            0,
            0,
        )
    )

    def encoded(exact_material: bytes, implementation: str) -> bytes:
        return _run(
            (
                "ffmpeg",
                "-nostdin",
                "-v",
                "error",
                "-f",
                "rawvideo",
                "-pixel_format",
                "rgb24",
                "-video_size",
                "2x2",
                "-i",
                "pipe:0",
                "-frames:v",
                "1",
                "-map_metadata",
                "-1",
                "-f",
                "image2pipe",
                "-c:v",
                implementation,
                "pipe:1",
            ),
            exact_material,
        )

    return (
        SuppliedMaterial("raw-rgb-a", first),
        SuppliedMaterial("raw-rgb-b", second),
        SuppliedMaterial("png", encoded(first, "png")),
        SuppliedMaterial("jpeg", encoded(second, "mjpeg")),
    )


def supplied_media_material() -> tuple[SuppliedMaterial, ...]:
    return _audio_material() + _photo_material()
