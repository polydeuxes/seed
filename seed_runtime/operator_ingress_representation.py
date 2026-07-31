"""Byte-boundary representation evidence for one operator-ingress occurrence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO, TextIO


class OperatorIngressRepresentationError(ValueError):
    """An operator-ingress representation artifact or metadata is malformed."""


@dataclass(frozen=True)
class CapturedOperatorMaterial:
    """Material observed at the smallest stdin boundary available to the caller."""

    exact_bytes: bytes
    eof: bool
    delimiter_hex: str | None
    capture_boundary: str
    byte_material_origin: str
    encoding_testimony: str | None
    known_loss: tuple[str, ...]

    def __post_init__(self) -> None:
        invalid_type = (
            type(self.exact_bytes) is not bytes
            or type(self.eof) is not bool
            or (self.delimiter_hex is not None and type(self.delimiter_hex) is not str)
            or type(self.capture_boundary) is not str
            or type(self.byte_material_origin) is not str
            or (
                self.encoding_testimony is not None
                and type(self.encoding_testimony) is not str
            )
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
        if self.encoding_testimony == "" or any(
            type(item) is not str for item in self.known_loss
        ):
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


@dataclass(frozen=True)
class RepresentationExamination:
    """One bounded decoder invocation and its evidence, not an encoding verdict."""

    mechanism: str
    mechanism_selection: str
    outcome: str
    represented_text: str | None
    failure: str | None

    def __post_init__(self) -> None:
        if (
            type(self.mechanism) is not str
            or type(self.mechanism_selection) is not str
            or type(self.outcome) is not str
            or (
                self.represented_text is not None
                and type(self.represented_text) is not str
            )
            or (self.failure is not None and type(self.failure) is not str)
            or not self.mechanism
            or not self.mechanism_selection
        ):
            raise OperatorIngressRepresentationError(
                "malformed representation examination"
            )
        if self.outcome == "decoded":
            coherent = type(self.represented_text) is str and self.failure is None
        elif self.outcome in {"decoder_unavailable", "bytes_rejected"}:
            coherent = (
                self.represented_text is None
                and type(self.failure) is str
                and bool(self.failure)
            )
        else:
            coherent = False
        if not coherent:
            raise OperatorIngressRepresentationError(
                "malformed representation examination"
            )

    @property
    def succeeded(self) -> bool:
        return self.outcome == "decoded"


def capture_stdin_material(input_stream: TextIO | BinaryIO) -> CapturedOperatorMaterial:
    """Read one framed occurrence without passing production stdin through TextIO."""
    binary = getattr(input_stream, "buffer", None)
    if binary is not None:
        material = binary.readline()
        testimony = _encoding_testimony(input_stream)
        boundary = "stdin.buffer.readline"
        byte_material_origin = "direct_boundary_observation"
        loss = (
            "transport bytes before the stdin byte-stream boundary are not observable",
        )
    else:
        value = input_stream.readline()
        testimony = _encoding_testimony(input_stream)
        if isinstance(value, bytes):
            material = value
            boundary = "binary-stream.readline (bytes observed directly)"
            byte_material_origin = "direct_boundary_observation"
            loss = (
                "transport bytes before the supplied binary-stream boundary are not observable",
            )
        else:
            # Compatibility for programmatic text streams.  This adapter is honest
            # about the earlier framing/decoding rather than calling recreated bytes
            # original transport material.
            adapter_encoding = testimony or "utf-8"
            material = value.encode(adapter_encoding, errors="strict")
            boundary = "text-stream adapter after prior decoding"
            byte_material_origin = "text_reencoding_after_prior_decoding"
            loss = (
                "original transport bytes and prior decoder behavior are unavailable",
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
        encoding_testimony=testimony,
        known_loss=loss,
    )


def _encoding_testimony(input_stream: TextIO | BinaryIO) -> str | None:
    raw_testimony = getattr(input_stream, "encoding", None)
    if raw_testimony is None:
        return None
    if type(raw_testimony) is not str:
        raise OperatorIngressRepresentationError("malformed stream encoding metadata")
    return raw_testimony or None


def examine_text_representation(
    capture: CapturedOperatorMaterial,
) -> RepresentationExamination:
    """Strictly invoke the selected decoder when material exists."""
    if capture.eof:
        raise OperatorIngressRepresentationError(
            "cannot examine EOF as operator-ingress material"
        )
    mechanism = capture.encoding_testimony or "utf-8"
    selection = (
        "stream_encoding_testimony"
        if capture.encoding_testimony is not None
        else "implementation_utf8_fallback"
    )
    try:
        represented = capture.exact_bytes.decode(mechanism, errors="strict")
    except LookupError as exc:
        return RepresentationExamination(
            mechanism,
            selection,
            "decoder_unavailable",
            None,
            f"{type(exc).__name__}: {exc}",
        )
    except UnicodeDecodeError as exc:
        return RepresentationExamination(
            mechanism,
            selection,
            "bytes_rejected",
            None,
            f"{type(exc).__name__}: {exc}",
        )
    return RepresentationExamination(mechanism, selection, "decoded", represented, None)
