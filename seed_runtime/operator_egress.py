"""Write one exact Representation result to an external boundary."""

from __future__ import annotations

from typing import Any, BinaryIO


class ExactMaterialEgressFailure(Exception):
    """One invoked egress boundary did not report exact completion."""

    def __init__(
        self,
        message: str,
        *,
        reported_count: int | None,
        error: Exception | None,
    ) -> None:
        super().__init__(message)
        self.reported_count = reported_count
        self.error = error


def operator_emission_boundary(
    output_stream: BinaryIO,
    *,
    boundary_identity: str,
    locality_identity: str,
) -> tuple[BinaryIO, str, str]:
    """Bind one host output boundary to its exact operator coordinates."""

    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("egress requires one exact boundary identity")
    if type(locality_identity) is not str or not locality_identity:
        raise TypeError("egress requires one exact operator Locality identity")
    return (output_stream, boundary_identity, locality_identity)


def read_operator_emission_boundary(
    boundary: Any,
) -> tuple[BinaryIO, str, str]:
    """Refuse an inferred or mutable output-boundary carrier."""

    if (
        type(boundary) is not tuple
        or len(boundary) != 3
        or type(boundary[1]) is not str
        or not boundary[1]
        or type(boundary[2]) is not str
        or not boundary[2]
    ):
        raise TypeError("egress requires one exact operator boundary")
    return boundary


def emit_exact_material(output_stream: BinaryIO, exact_material: bytes) -> int:
    """Write exact material without decoding or selecting a display species."""
    write = getattr(output_stream, "write", None)
    sendall = getattr(output_stream, "sendall", None)
    if write is None and sendall is None:
        raise TypeError("egress requires one writable boundary")
    if type(exact_material) is not bytes:
        raise TypeError("egress requires exact material bytes")
    if sendall is not None:
        try:
            sendall(exact_material)
        except Exception as error:
            raise ExactMaterialEgressFailure(
                "egress boundary raised before reporting exact completion",
                reported_count=None,
                error=error,
            ) from error
        written = len(exact_material)
    else:
        try:
            written = write(exact_material)
        except Exception as error:
            raise ExactMaterialEgressFailure(
                "egress boundary raised before reporting exact completion",
                reported_count=None,
                error=error,
            ) from error
    if type(written) is not int or written != len(exact_material):
        raise ExactMaterialEgressFailure(
            "egress boundary did not preserve exact material",
            reported_count=written if type(written) is int else None,
            error=None,
        )
    flush = getattr(output_stream, "flush", None)
    if flush is not None:
        try:
            flush()
        except Exception as error:
            raise ExactMaterialEgressFailure(
                "egress boundary raised after reporting the exact material count",
                reported_count=written,
                error=error,
            ) from error
    return written
