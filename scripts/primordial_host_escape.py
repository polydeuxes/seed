"""Primordial process-host escape at the exact stdin byte boundary."""

from __future__ import annotations

from typing import BinaryIO


_ESCAPE_FRAMES = (b"/", b"/\n", b"/\r\n")


class _PrimordialHostInput:
    def __init__(self, input_stream: BinaryIO) -> None:
        self._input_stream = input_stream
        self._escaped = False

    def readline(self) -> bytes:
        if self._escaped:
            return b""
        material = self._input_stream.readline()
        if type(material) is bytes and material in _ESCAPE_FRAMES:
            self._escaped = True
            return b""
        return material


def primordial_host_input(input_stream: BinaryIO) -> _PrimordialHostInput:
    """Expose one exact slash line to the hosted process as EOF."""
    return _PrimordialHostInput(input_stream)
