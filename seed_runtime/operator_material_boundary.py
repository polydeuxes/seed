"""Exact operator material at one byte-stream boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO, TextIO


class OperatorMaterialBoundaryError(ValueError):
    """Operator material or its byte-stream boundary is malformed."""


@dataclass(frozen=True)
class OperatorBoundaryMaterial:
    """Material observed at the smallest stdin boundary available to the caller."""

    exact_bytes: bytes
    eof: bool
    delimiter_hex: str | None
    material_boundary: str
    known_loss: tuple[str, ...]

    def __post_init__(self) -> None:
        invalid_type = (
            type(self.exact_bytes) is not bytes
            or type(self.eof) is not bool
            or (self.delimiter_hex is not None and type(self.delimiter_hex) is not str)
            or type(self.material_boundary) is not str
            or type(self.known_loss) is not tuple
        )
        if invalid_type:
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )
        if not self.material_boundary:
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )
        if any(type(item) is not str for item in self.known_loss):
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )
        expected_delimiter = (
            "0d0a"
            if self.exact_bytes.endswith(b"\r\n")
            else "0a" if self.exact_bytes.endswith(b"\n") else None
        )
        if self.eof is not (self.exact_bytes == b""):
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )
        if self.delimiter_hex != expected_delimiter:
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )

def operator_boundary_material(input_stream: TextIO | BinaryIO) -> OperatorBoundaryMaterial:
    """Read one framed occurrence from a byte stream.

    A live wrapped stream is accepted only when it exposes its underlying
    ``buffer``. No represented material is read here.
    Programmatic callers therefore supply a binary stream such as
    :class:`io.BytesIO`.
    """
    binary = getattr(input_stream, "buffer", None)
    if binary is not None:
        material = binary.readline()
        boundary = "stdin.buffer.readline"
        loss = (
            "transport bytes before the stdin byte-stream boundary are not observable",
        )
    else:
        material = input_stream.readline()
        boundary = "binary-stream.readline (bytes observed directly)"
        loss = (
            "transport bytes before the supplied binary-stream boundary are not observable",
        )
    if type(material) is not bytes:
        raise OperatorMaterialBoundaryError("operator material requires a binary stream")
    delimiter = (
        "0d0a"
        if material.endswith(b"\r\n")
        else "0a" if material.endswith(b"\n") else None
    )
    return OperatorBoundaryMaterial(
        exact_bytes=material,
        eof=material == b"",
        delimiter_hex=delimiter,
        material_boundary=boundary,
        known_loss=loss,
    )
