"""Byte-boundary representation evidence for one operator-ingress occurrence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO, TextIO


class OperatorIngressRepresentationError(ValueError):
    """An operator-ingress representation or metadata is malformed."""


@dataclass(frozen=True)
class CapturedOperatorMaterial:
    """Material observed at the smallest stdin boundary available to the caller."""

    exact_bytes: bytes
    eof: bool
    delimiter_hex: str | None
    capture_boundary: str
    byte_material_origin: str
    known_loss: tuple[str, ...]

    def __post_init__(self) -> None:
        invalid_type = (
            type(self.exact_bytes) is not bytes
            or type(self.eof) is not bool
            or (self.delimiter_hex is not None and type(self.delimiter_hex) is not str)
            or type(self.capture_boundary) is not str
            or type(self.byte_material_origin) is not str
            or type(self.known_loss) is not tuple
        )
        if invalid_type:
            raise OperatorIngressRepresentationError(
                "malformed captured operator material"
            )
        if not self.capture_boundary or not self.byte_material_origin:
            raise OperatorIngressRepresentationError(
                "malformed captured operator material"
            )
        if any(type(item) is not str for item in self.known_loss):
            raise OperatorIngressRepresentationError(
                "malformed captured operator material"
            )
        expected_delimiter = (
            "0d0a"
            if self.exact_bytes.endswith(b"\r\n")
            else "0a" if self.exact_bytes.endswith(b"\n") else None
        )
        if self.eof is not (self.exact_bytes == b""):
            raise OperatorIngressRepresentationError(
                "malformed captured operator material"
            )
        if self.delimiter_hex != expected_delimiter:
            raise OperatorIngressRepresentationError(
                "malformed captured operator material"
            )

def capture_stdin_material(input_stream: TextIO | BinaryIO) -> CapturedOperatorMaterial:
    """Read one framed occurrence from a byte stream.

    A live wrapped stream is accepted only when it exposes its underlying
    ``buffer``. No represented material is reconstructed here.
    Programmatic callers therefore supply a binary stream such as
    :class:`io.BytesIO`.
    """
    binary = getattr(input_stream, "buffer", None)
    if binary is not None:
        material = binary.readline()
        boundary = "stdin.buffer.readline"
        byte_material_origin = "direct_boundary_observation"
        loss = (
            "transport bytes before the stdin byte-stream boundary are not observable",
        )
    else:
        material = input_stream.readline()
        boundary = "binary-stream.readline (bytes observed directly)"
        byte_material_origin = "direct_boundary_observation"
        loss = (
            "transport bytes before the supplied binary-stream boundary are not observable",
        )
    if type(material) is not bytes:
        raise OperatorIngressRepresentationError(
            "operator ingress requires a binary stream"
        )
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
        byte_material_origin=byte_material_origin,
        known_loss=loss,
    )
