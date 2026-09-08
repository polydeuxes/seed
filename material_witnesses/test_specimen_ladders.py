"""Keep operator-authored specimen coordinates exact and independently variable."""

from __future__ import annotations

import wave

from material_witnesses.audio_ladder import (
    CHANNELS as AUDIO_CHANNEL_COUNT,
    SAMPLE_RATE,
    SAMPLE_WIDTH,
    count_ladder,
    frequency_ladder,
)
from material_witnesses.pixel_ladder import (
    CHANNELS as PIXEL_CHANNELS,
    channel_ladder,
    pixel_ladder,
)
from material_witnesses.visual_ladder import rungs


def test_pixel_specimens_preserve_exact_channel_positions(tmp_path):
    pixels = pixel_ladder(tmp_path, [0, 128, 255])
    channels = channel_ladder(tmp_path, 255)

    assert tuple(path.read_bytes() for path in pixels) == (
        b"\x00\x00\x00",
        b"\x80\x80\x80",
        b"\xff\xff\xff",
    )
    assert len(channels) == 2 * len(PIXEL_CHANNELS)
    assert {
        path.read_bytes()
        for path in channels
        if path.read_bytes() != b"\x00\x00\x00"
    } == {b"\xff\x00\x00", b"\x00\xff\x00", b"\x00\x00\xff"}


def test_audio_specimens_preserve_exact_container_coordinates(tmp_path):
    count_paths = count_ladder(tmp_path, [1, 2])
    frequency_paths = frequency_ladder(tmp_path, [60.0, 120.0])

    for path in (*count_paths, *frequency_paths):
        with wave.open(str(path), "rb") as material:
            assert material.getframerate() == SAMPLE_RATE
            assert material.getsampwidth() == SAMPLE_WIDTH
            assert material.getnchannels() == AUDIO_CHANNEL_COUNT
    assert count_paths[0].read_bytes() != count_paths[1].read_bytes()
    assert frequency_paths[0].read_bytes() != frequency_paths[1].read_bytes()


def test_visual_specimens_keep_each_authored_rung_distinct():
    found = rungs("hello", "320x240", "200x120")

    assert len(found) == 4
    assert len({name for name, _ in found}) == len(found)
    assert found[0][1] == ""
    assert found[1][1] in found[2][1]
    assert found[1][1] in found[3][1]
    assert found[2][1] != found[3][1]
