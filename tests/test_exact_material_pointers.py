from __future__ import annotations

import base64
import hashlib

import pytest

from seed_runtime.exact_material_pointers import (
    ENCODING_VERSION,
    ExactMaterialPointerError,
    ExactMaterialPointers,
    LiteralPart,
    ReferencePart,
    form_exact_material_pointers,
    reconstruct_exact_bytes,
)


def test_repeated_exact_material_is_represented_by_backward_references():
    material = b"through through through "

    encoded = form_exact_material_pointers(material)

    assert reconstruct_exact_bytes(encoded) == material
    assert any(isinstance(part, ReferencePart) for part in encoded.parts)
    assert encoded.byte_count == len(material)
    assert encoded.sha256 == hashlib.sha256(material).hexdigest()


def test_a_reference_may_reuse_bytes_that_an_earlier_reference_reconstructed():
    material = b"abcdabcdabcd"
    encoded = ExactMaterialPointers(
        byte_count=len(material),
        sha256=hashlib.sha256(material).hexdigest(),
        parts=(
            LiteralPart(b"abcd"),
            ReferencePart(start=0, length=4),
            # These bytes were themselves produced by the preceding reference.
            ReferencePart(start=4, length=4),
        ),
    )

    assert reconstruct_exact_bytes(encoded) == material


def test_references_do_not_depend_on_word_or_token_boundaries():
    material = b"got through the door; through the wall"

    encoded = form_exact_material_pointers(material)

    assert reconstruct_exact_bytes(encoded) == material
    references = [part for part in encoded.parts if isinstance(part, ReferencePart)]
    assert references
    assert max(part.length for part in references) >= len(b"through the ")


def test_arbitrary_bytes_round_trip_without_text_interpretation():
    material = bytes(range(256)) + bytes(range(256))

    encoded = form_exact_material_pointers(material)
    recovered = ExactMaterialPointers.from_json_dict(encoded.to_json_dict())

    assert reconstruct_exact_bytes(recovered) == material
    assert any(isinstance(part, ReferencePart) for part in recovered.parts)


def test_empty_material_is_exactly_representable():
    encoded = form_exact_material_pointers(b"")

    assert encoded.parts == ()
    assert encoded.byte_count == 0
    assert reconstruct_exact_bytes(encoded) == b""


def test_serialized_literal_is_exact_bytes_not_decoded_text():
    encoded = ExactMaterialPointers(
        byte_count=3,
        sha256=hashlib.sha256(b"\x00\xffA").hexdigest(),
        parts=(LiteralPart(b"\x00\xffA"),),
    )

    carried = encoded.to_json_dict()

    assert carried["version"] == ENCODING_VERSION
    assert base64.b64decode(carried["parts"][0]["bytes_b64"]) == b"\x00\xffA"
    assert ExactMaterialPointers.from_json_dict(carried) == encoded


def test_forward_or_partially_forward_reference_is_refused():
    digest = hashlib.sha256(b"abcdabcd").hexdigest()

    with pytest.raises(ExactMaterialPointerError, match="already reconstructed"):
        ExactMaterialPointers(
            byte_count=8,
            sha256=digest,
            parts=(LiteralPart(b"abcd"), ReferencePart(start=2, length=4)),
        )


def test_byte_count_and_commitment_are_verified_against_reconstruction():
    digest = hashlib.sha256(b"abc").hexdigest()

    with pytest.raises(ExactMaterialPointerError, match="byte_count"):
        ExactMaterialPointers(
            byte_count=4,
            sha256=digest,
            parts=(LiteralPart(b"abc"),),
        )

    with pytest.raises(ExactMaterialPointerError, match="sha256"):
        ExactMaterialPointers(
            byte_count=3,
            sha256="0" * 64,
            parts=(LiteralPart(b"abc"),),
        )


def test_malformed_serialized_parts_are_refused():
    honest = form_exact_material_pointers(b"abcdef").to_json_dict()

    malformed = dict(honest)
    malformed["parts"] = [{"kind": "literal", "bytes_b64": "not base64!"}]
    with pytest.raises(ExactMaterialPointerError, match="base64"):
        ExactMaterialPointers.from_json_dict(malformed)

    malformed = dict(honest)
    malformed["parts"] = [{"kind": "reference", "start": True, "length": 4}]
    with pytest.raises(ExactMaterialPointerError, match="reference start"):
        ExactMaterialPointers.from_json_dict(malformed)

    malformed = dict(honest)
    malformed["parts"] = [{"kind": "word", "value": "through"}]
    with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
        ExactMaterialPointers.from_json_dict(malformed)


def test_encoder_parameters_are_exactly_bounded():
    with pytest.raises(ExactMaterialPointerError, match="exact bytes"):
        form_exact_material_pointers(bytearray(b"abc"))
    for bad in (True, 1, 1.5, "4"):
        with pytest.raises(ExactMaterialPointerError, match="minimum_reference_length"):
            form_exact_material_pointers(b"abc", minimum_reference_length=bad)
    for bad in (True, 0, -1, 1.5, "64"):
        with pytest.raises(ExactMaterialPointerError, match="candidate_limit"):
            form_exact_material_pointers(b"abc", candidate_limit=bad)
