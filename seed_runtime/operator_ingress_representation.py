"""Byte-boundary representation evidence for one operator-ingress occurrence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO, TextIO


@dataclass(frozen=True)
class CapturedOperatorMaterial:
    """Material observed at the smallest stdin boundary available to the caller."""

    exact_bytes: bytes
    eof: bool
    delimiter_hex: str | None
    capture_boundary: str
    original_transport_bytes: bool
    encoding_testimony: str | None
    known_loss: tuple[str, ...]


@dataclass(frozen=True)
class RepresentationExamination:
    """One bounded decoder invocation and its evidence, not an encoding verdict."""

    mechanism: str
    succeeded: bool
    represented_text: str | None
    failure: str | None


def capture_stdin_material(input_stream: TextIO | BinaryIO) -> CapturedOperatorMaterial:
    """Read one framed occurrence without passing production stdin through TextIO."""
    binary = getattr(input_stream, "buffer", None)
    if binary is not None:
        material = binary.readline()
        testimony = getattr(input_stream, "encoding", None)
        boundary = "stdin.buffer.readline"
        original_transport_bytes = True
        loss = (
            "transport bytes before the stdin byte-stream boundary are not observable",
        )
    else:
        value = input_stream.readline()
        testimony = getattr(input_stream, "encoding", None) or "utf-8"
        # Compatibility for programmatic text streams.  This adapter is honest
        # about the earlier framing/decoding rather than calling recreated bytes
        # original transport material.
        material = value.encode(testimony, errors="strict")
        boundary = "text-stream adapter after prior decoding"
        original_transport_bytes = False
        loss = ("original transport bytes and prior decoder behavior are unavailable",)
    delimiter = (
        "0d0a"
        if material.endswith(b"\r\n")
        else "0a" if material.endswith(b"\n") else None
    )
    return CapturedOperatorMaterial(
        exact_bytes=material,
        eof=material == b"",
        delimiter_hex=delimiter,
        capture_boundary=boundary,
        original_transport_bytes=original_transport_bytes,
        encoding_testimony=testimony,
        known_loss=loss,
    )


def examine_text_representation(
    capture: CapturedOperatorMaterial,
) -> RepresentationExamination:
    """Invoke only the stdin transport's testified decoder, strictly."""
    mechanism = capture.encoding_testimony or "utf-8"
    if capture.eof:
        return RepresentationExamination(
            mechanism, False, None, "EOF has no material to decode"
        )
    try:
        represented = capture.exact_bytes.decode(mechanism, errors="strict")
    except (UnicodeDecodeError, LookupError) as exc:
        return RepresentationExamination(
            mechanism,
            False,
            None,
            f"{type(exc).__name__}: {exc}",
        )
    return RepresentationExamination(mechanism, True, represented, None)
