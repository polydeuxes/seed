"""Write one exact Representation result to an external boundary."""

from __future__ import annotations

from typing import Any, BinaryIO


EXACT_MATERIAL_WRITE_BOUNDARY_RULE = "write exact material"


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


def _require_exact_writable_boundary(output_stream: BinaryIO) -> None:
    if not callable(getattr(output_stream, "write", None)) and not callable(
        getattr(output_stream, "sendall", None)
    ):
        raise TypeError("egress requires one writable boundary")


def operator_emission_boundary(
    output_stream: BinaryIO,
    *,
    boundary_identity: str,
    locality_identity: str,
    boundary_rule: str,
) -> tuple[BinaryIO, str, str, str]:
    """Bind one host output boundary to its exact operator coordinates."""

    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("egress requires one exact boundary identity")
    if type(locality_identity) is not str or not locality_identity:
        raise TypeError("egress requires one exact operator Locality identity")
    if type(boundary_rule) is not str or not boundary_rule:
        raise TypeError("egress requires one exact destination boundary rule")
    _require_exact_writable_boundary(output_stream)
    return (output_stream, boundary_identity, locality_identity, boundary_rule)


def read_operator_emission_boundary(
    boundary: Any,
) -> tuple[BinaryIO, str, str, str]:
    """Refuse an inferred or mutable output-boundary carrier."""

    if (
        type(boundary) is not tuple
        or len(boundary) != 4
        or type(boundary[1]) is not str
        or not boundary[1]
        or type(boundary[2]) is not str
        or not boundary[2]
        or type(boundary[3]) is not str
        or not boundary[3]
    ):
        raise TypeError("egress requires one exact operator boundary")
    _require_exact_writable_boundary(boundary[0])
    return boundary


def emit_exact_material(output_stream: BinaryIO, exact_material: bytes) -> int:
    """Obtain one exact write acceptance without inferring later delivery."""
    _require_exact_writable_boundary(output_stream)
    write = getattr(output_stream, "write", None)
    sendall = getattr(output_stream, "sendall", None)
    if type(exact_material) is not bytes:
        raise TypeError("egress requires exact material bytes")
    if callable(sendall):
        try:
            reported = sendall(exact_material)
        except Exception as error:
            raise ExactMaterialEgressFailure(
                "egress boundary raised before reporting exact completion",
                reported_count=None,
                error=error,
            ) from error
        if reported is not None:
            raise ExactMaterialEgressFailure(
                "egress boundary did not preserve exact material",
                reported_count=reported if type(reported) is int else None,
                error=None,
            )
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
    return written
