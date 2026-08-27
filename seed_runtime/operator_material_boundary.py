"""Exact operator material at one byte-stream boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO, TextIO


class OperatorMaterialBoundaryError(ValueError):
    """Operator material or its byte-stream boundary is malformed."""


@dataclass(frozen=True)
class OperatorBoundaryMaterial:
    """Exact material at the smallest stdin boundary available to the caller."""

    exact_bytes: bytes
    eof: bool
    material_boundary: str

    def __post_init__(self) -> None:
        invalid_type = (
            type(self.exact_bytes) is not bytes
            or type(self.eof) is not bool
            or type(self.material_boundary) is not str
        )
        if invalid_type:
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )
        if not self.material_boundary:
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )
        if self.eof is not (self.exact_bytes == b""):
            raise OperatorMaterialBoundaryError(
                "malformed operator boundary material"
            )


def _operator_material_source(
    input_stream: TextIO | BinaryIO,
) -> tuple[BinaryIO, str]:
    binary = getattr(input_stream, "buffer", None)
    if binary is not None:
        return binary, "stdin.buffer.readline"
    return input_stream, "binary-stream.readline (exact bytes)"


def operator_material_source_boundary(input_stream: TextIO | BinaryIO) -> str:
    """Return the exact boundary address without reading from it."""

    _source, boundary = _operator_material_source(input_stream)
    return boundary


def operator_boundary_material(input_stream: TextIO | BinaryIO) -> OperatorBoundaryMaterial:
    """Read one framed occurrence from a byte stream.

    A live wrapped stream is accepted only when it carries its underlying
    ``buffer``. No represented material is read here.
    Programmatic callers therefore supply a binary stream such as
    :class:`io.BytesIO`.
    """
    source, boundary = _operator_material_source(input_stream)
    material = source.readline()
    if type(material) is not bytes:
        raise OperatorMaterialBoundaryError("operator material requires a binary stream")
    return OperatorBoundaryMaterial(
        exact_bytes=material,
        eof=material == b"",
        material_boundary=boundary,
    )
