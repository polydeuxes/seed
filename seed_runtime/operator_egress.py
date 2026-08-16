"""Write one exact Representation result to an external boundary."""

from __future__ import annotations

from typing import BinaryIO


def emit_exact_material(output_stream: BinaryIO, exact_material: bytes) -> int:
    """Write exact material without decoding or selecting a display species."""
    write = getattr(output_stream, "write", None)
    sendall = getattr(output_stream, "sendall", None)
    if write is None and sendall is None:
        raise TypeError("egress requires one writable boundary")
    if type(exact_material) is not bytes:
        raise TypeError("egress requires exact material bytes")
    if sendall is not None:
        sendall(exact_material)
        written = len(exact_material)
    else:
        written = write(exact_material)
    if written is None:
        written = len(exact_material)
    if type(written) is not int or written != len(exact_material):
        raise ValueError("egress boundary did not preserve exact material")
    flush = getattr(output_stream, "flush", None)
    if flush is not None:
        flush()
    return written
