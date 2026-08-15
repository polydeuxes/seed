"""The live operator boundary accepts only directly observed byte streams."""

from __future__ import annotations

from io import BytesIO, StringIO

import pytest

from seed_runtime.operator_ingress_representation import (
    OperatorIngressRepresentationError,
    capture_stdin_material,
)


class _DeclaredBytes(BytesIO):
    encoding = "a declaration the byte boundary does not consult"


def test_binary_capture_preserves_every_byte_without_text_conversion():
    captured = capture_stdin_material(BytesIO(b"\xff\x00\x80\n"))

    assert captured.exact_bytes == b"\xff\x00\x80\n"
    assert captured.byte_material_origin == "direct_boundary_observation"
    assert captured.delimiter_hex == "0a"


def test_stream_encoding_metadata_does_not_change_observed_bytes():
    captured = capture_stdin_material(_DeclaredBytes(b"\xff\n"))

    assert captured.exact_bytes == b"\xff\n"
    assert not hasattr(captured, "stream_encoding_metadata")


def test_programmatic_text_stream_is_refused_at_the_boundary():
    with pytest.raises(
        OperatorIngressRepresentationError, match="requires a binary stream"
    ):
        capture_stdin_material(StringIO("material\n"))


def test_eof_and_delimiters_are_derived_from_exact_bytes():
    assert capture_stdin_material(BytesIO()).eof is True
    assert capture_stdin_material(BytesIO(b"a\r\n")).delimiter_hex == "0d0a"
    assert capture_stdin_material(BytesIO(b"a")).delimiter_hex is None
