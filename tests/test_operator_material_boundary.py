"""The live operator boundary accepts only exact byte streams."""

from __future__ import annotations

from io import BytesIO, StringIO

import pytest


from seed_runtime.operator_material_boundary import (
    OperatorMaterialBoundaryError,
    operator_boundary_material,
    operator_material_source_boundary,
)


class _DeclaredBytes(BytesIO):
    encoding = "a declaration the byte boundary does not consult"


class _ReadCountingBytes(BytesIO):
    def __init__(self, material: bytes):
        super().__init__(material)
        self.read_count = 0

    def readline(self, *args, **kwargs):
        self.read_count += 1
        return super().readline(*args, **kwargs)


def test_source_boundary_is_addressed_before_material_is_read():
    stream = _ReadCountingBytes(b"material\n")

    source_boundary = operator_material_source_boundary(stream)

    assert stream.read_count == 0
    material = operator_boundary_material(stream)
    assert stream.read_count == 1
    assert material.material_boundary == source_boundary


def test_binary_boundary_preserves_every_byte_without_text_conversion():
    material = operator_boundary_material(BytesIO(b"\xff\x00\x80\n"))

    assert material.exact_bytes == b"\xff\x00\x80\n"


def test_stream_encoding_metadata_does_not_change_exact_bytes():
    material = operator_boundary_material(_DeclaredBytes(b"\xff\n"))

    assert material.exact_bytes == b"\xff\n"
    assert not hasattr(material, "stream_encoding_metadata")


def test_programmatic_text_stream_is_refused_at_the_boundary():
    with pytest.raises(
        OperatorMaterialBoundaryError, match="requires a binary stream"
    ):
        operator_boundary_material(StringIO("material\n"))


def test_eof_is_derived_from_exact_bytes():
    assert operator_boundary_material(BytesIO()).eof is True
    assert operator_boundary_material(BytesIO(b"a\r\n")).exact_bytes == b"a\r\n"
    assert operator_boundary_material(BytesIO(b"a")).exact_bytes == b"a"
