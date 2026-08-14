"""What a text stream's declared encoding does to the material it carries.

A text stream hands over characters it already decoded. Re-encoding them is a
reconstruction of bytes nobody observed, and the stream's declared encoding is
the only evidence of what those bytes were. Where that encoding cannot
represent what the stream itself decoded, it is not the encoding the material
arrived in, and the reconstruction says so rather than failing.
"""

from __future__ import annotations

import io

from seed_runtime.operator_ingress_representation import capture_stdin_material

DECLARED = "text_reencoding_after_prior_decoding"
OUTSIDE = "text_reencoding_outside_declared_encoding"


class _Declared(io.StringIO):
    """A text stream that declares an encoding, as a terminal's stdin does."""

    def __init__(self, value: str, encoding: str) -> None:
        super().__init__(value)
        self._encoding = encoding

    @property
    def encoding(self) -> str:
        return self._encoding


def test_material_the_declared_encoding_can_represent_uses_it():
    captured = capture_stdin_material(_Declared("café\n", "latin-1"))

    assert captured.byte_material_origin == DECLARED
    assert captured.exact_bytes == "café\n".encode("latin-1")
    assert len(captured.exact_bytes) == 5


def test_one_typed_line_is_different_material_under_a_different_declaration():
    """The declared encoding is part of what the recorded bytes are."""

    latin = capture_stdin_material(_Declared("café\n", "latin-1"))
    utf8 = capture_stdin_material(_Declared("café\n", "utf-8"))

    assert latin.exact_bytes != utf8.exact_bytes
    assert len(latin.exact_bytes) == 5
    assert len(utf8.exact_bytes) == 6
    assert latin.byte_material_origin == utf8.byte_material_origin == DECLARED


def test_material_the_declared_encoding_cannot_represent_is_still_captured():
    """An encoding that cannot represent what its own stream decoded is refused,
    not the material."""

    captured = capture_stdin_material(_Declared("猫坐在垫子上\n", "ascii"))

    assert captured.exact_bytes == "猫坐在垫子上\n".encode("utf-8")
    assert captured.byte_material_origin == OUTSIDE


def test_falling_outside_the_declared_encoding_is_recorded_as_known_loss():
    captured = capture_stdin_material(_Declared("café\n", "ascii"))

    named = [entry for entry in captured.known_loss if "ascii" in entry]
    assert named, captured.known_loss
    assert "UTF-8" in named[0]
    assert captured.stream_encoding_metadata == "ascii"


def test_representable_material_records_no_encoding_loss():
    """The extra known_loss entry appears only where the declaration failed."""

    captured = capture_stdin_material(_Declared("plain\n", "ascii"))

    assert captured.byte_material_origin == DECLARED
    assert not [entry for entry in captured.known_loss if "cannot represent" in entry]


def test_the_two_origins_are_distinguishable_for_one_line_of_material():
    """A reader can tell which reconstruction produced these bytes."""

    inside = capture_stdin_material(_Declared("café\n", "utf-8"))
    outside = capture_stdin_material(_Declared("café\n", "ascii"))

    assert inside.exact_bytes == outside.exact_bytes
    assert inside.byte_material_origin != outside.byte_material_origin
