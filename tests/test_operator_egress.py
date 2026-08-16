from __future__ import annotations

from io import BytesIO

import pytest

from seed_runtime.operator_egress import emit_exact_material


def test_egress_writes_exact_bytes_without_decoding():
    output = BytesIO()
    material = b"\x00\xff\x80hello"

    assert emit_exact_material(output, material) == len(material)
    assert output.getvalue() == material


def test_egress_refuses_non_bytes():
    with pytest.raises(TypeError, match="exact material bytes"):
        emit_exact_material(BytesIO(), "hello")


def test_egress_refuses_a_short_write():
    class ShortBoundary:
        def write(self, material):
            return len(material) - 1

    with pytest.raises(ValueError, match="did not preserve"):
        emit_exact_material(ShortBoundary(), b"hello")
