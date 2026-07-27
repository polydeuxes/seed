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


def pesc_dimensions(
    capture: CapturedOperatorMaterial, examination: RepresentationExamination
):
    """Project the four canonical PESC dimensions as separate evidence records."""
    common = {
        "source_provenance": capture.capture_boundary,
        "scope_locality": "this captured stdin occurrence only",
        "known_loss": list(capture.known_loss),
        "unknowns_conflicts": [
            "true source-relative encoding Unknown",
            "pre-boundary transport representation Unknown",
            "no representation conflict evidence observed",
        ],
    }
    return {
        "P_projection_representation": {
            **common,
            "observed_evidence": {
                "exact_bytes_hex": capture.exact_bytes.hex(),
                "byte_count": len(capture.exact_bytes),
                "delimiter_hex": capture.delimiter_hex,
                "eof": capture.eof,
                "decoder_mechanism": examination.mechanism,
                "decoder_succeeded": examination.succeeded,
                "decoder_failure": examination.failure,
            },
            "producer_responsibility": "capture exact bytes at the available stdin boundary and invoke the testified decoder strictly",
            "supports": "the retained byte representation and the observed decoder invocation outcome",
            "does_not_follow": "original transport bytes, unique or correct encoding, meaning, grammar, intent, or constitutional truth",
        },
        "E_equivalence": {
            **common,
            "observed_evidence": "byte identity is exact byte-for-byte identity; admitted text, when present, is the strict decoder result",
            "producer_responsibility": "preserve bytes and represented text separately without normalization or replacement",
            "supports": "exact equality comparisons within this occurrence under the declared representations",
            "does_not_follow": "semantic, Unicode-normalized, source-relative, or cross-codec equivalence",
        },
        "S_scope": {
            **common,
            "observed_evidence": {
                "capture_boundary": capture.capture_boundary,
                "delimiter_present": capture.delimiter_hex is not None,
                "eof": capture.eof,
            },
            "producer_responsibility": "bound findings to this workspace/session/interaction occurrence lineage",
            "supports": "only the material returned by this one readline occurrence",
            "does_not_follow": "terminal, transport, session, stream, workspace, or corpus completeness",
        },
        "C_consumer_contract": {
            **common,
            "observed_evidence": "the communication bootstrap accepts only a successful strict text decoding; EOF and decoder failure stop",
            "producer_responsibility": "admit text only for the existing one-attempt communication bootstrap",
            "supports": "purpose-local text admission when strict decoding succeeds",
            "does_not_follow": "applicability to meaning, English, common grammar, interpretation, Demand, acquisition, BOGE, or cluster standing",
        },
    }
