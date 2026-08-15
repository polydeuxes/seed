from __future__ import annotations

import base64
import hashlib

import pytest

from seed_runtime.exact_material_pointers import (
    ExactMaterialReferenceLimits,
    ExactMaterialPointerError,
    ExactMaterialPointers,
    LiteralPart,
    ReferencePart,
    represent_exact_material_pointers,
    read_exact_bytes,
)


def test_repeated_exact_material_is_represented_by_backward_references():
    material = b"through through through "

    encoded = represent_exact_material_pointers(material)

    assert read_exact_bytes(encoded) == material
    assert any(isinstance(part, ReferencePart) for part in encoded.material)
    assert encoded.count == len(material)
    assert encoded.material_identity == hashlib.sha256(material).hexdigest()


def test_a_reference_may_reuse_bytes_that_an_earlier_reference_read():
    material = b"abcdabcdabcd"
    encoded = ExactMaterialPointers(
        reference_limits=ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=64),
        count=len(material),
        material_identity=hashlib.sha256(material).hexdigest(),
        material=(
            LiteralPart(b"abcd"),
            ReferencePart(source_position=0, count=4),
            # These bytes were themselves appended by the preceding reference.
            ReferencePart(source_position=4, count=4),
        ),
    )

    assert read_exact_bytes(encoded) == material


def test_references_do_not_depend_on_word_or_token_boundaries():
    material = b"got through the door; through the wall"

    encoded = represent_exact_material_pointers(material)

    assert read_exact_bytes(encoded) == material
    references = [part for part in encoded.material if isinstance(part, ReferencePart)]
    assert references
    assert max(part.count for part in references) >= len(b"through the ")


def test_arbitrary_bytes_round_trip_without_text_read():
    material = bytes(range(256)) + bytes(range(256))

    encoded = represent_exact_material_pointers(material)
    read = ExactMaterialPointers.from_json_dict(encoded.to_json_dict())

    assert read_exact_bytes(read) == material
    assert any(isinstance(part, ReferencePart) for part in read.material)


def test_empty_material_is_exactly_representable():
    encoded = represent_exact_material_pointers(b"")

    assert encoded.material == ()
    assert encoded.count == 0
    assert read_exact_bytes(encoded) == b""


def test_serialized_literal_is_exact_bytes_not_decoded_text():
    encoded = ExactMaterialPointers(
        reference_limits=ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=64),
        count=3,
        material_identity=hashlib.sha256(b"\x00\xffA").hexdigest(),
        material=(LiteralPart(b"\x00\xffA"),),
    )

    carried = encoded.to_json_dict()

    assert base64.b64decode(carried["material"][0]["representation"]) == b"\x00\xffA"
    assert ExactMaterialPointers.from_json_dict(carried) == encoded


def test_forward_or_partially_forward_reference_is_refused():
    material_identity = hashlib.sha256(b"abcdabcd").hexdigest()

    with pytest.raises(ExactMaterialPointerError, match="already read"):
        ExactMaterialPointers(
            reference_limits=ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=64),
            count=8,
            material_identity=material_identity,
            material=(LiteralPart(b"abcd"), ReferencePart(source_position=2, count=4)),
        )


def test_byte_count_and_commitment_are_verified_against_read():
    material_identity = hashlib.sha256(b"abc").hexdigest()

    with pytest.raises(ExactMaterialPointerError, match="count"):
        ExactMaterialPointers(
            reference_limits=ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=64),
            count=4,
            material_identity=material_identity,
            material=(LiteralPart(b"abc"),),
        )

    with pytest.raises(ExactMaterialPointerError, match="material_identity"):
        ExactMaterialPointers(
            reference_limits=ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=64),
            count=3,
            material_identity="0" * 64,
            material=(LiteralPart(b"abc"),),
        )


def test_malformed_serialized_parts_are_refused():
    honest = represent_exact_material_pointers(b"abcdef").to_json_dict()

    malformed = dict(honest)
    malformed["material"] = [{"kind": "literal", "representation": "not base64!"}]
    with pytest.raises(ExactMaterialPointerError, match="base64"):
        ExactMaterialPointers.from_json_dict(malformed)

    malformed = dict(honest)
    malformed["material"] = [{"kind": "reference", "source_position": True, "count": 4}]
    with pytest.raises(ExactMaterialPointerError, match="reference source_position"):
        ExactMaterialPointers.from_json_dict(malformed)

    malformed = dict(honest)
    malformed["material"] = [{"kind": "word", "value": "through"}]
    with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
        ExactMaterialPointers.from_json_dict(malformed)


def test_encoder_parameters_are_exactly_bounded():
    with pytest.raises(ExactMaterialPointerError, match="exact bytes"):
        represent_exact_material_pointers(bytearray(b"abc"))
    for bad in (True, 1, 1.5, "4"):
        with pytest.raises(ExactMaterialPointerError, match="reference_count_limit"):
            represent_exact_material_pointers(b"abc", reference_count_limit=bad)
    for bad in (True, 0, -1, 1.5, "64"):
        with pytest.raises(ExactMaterialPointerError, match="candidate_limit"):
            represent_exact_material_pointers(b"abc", candidate_limit=bad)


def test_the_account_declares_the_representation_act_and_exact_yield():
    material = (b"the cat jumped the fence. the cat slept. "
                b"a fence is not a cat. the cat jumped the fence.")

    accounts = {
        (reference_count, candidate_count): represent_exact_material_pointers(
            material,
            reference_count_limit=reference_count,
            candidate_limit=candidate_count,
        )
        for reference_count, candidate_count in ((2, 64), (4, 64), (8, 64), (4, 1))
    }
    for (reference_count, candidate_count), encoded in accounts.items():
        assert encoded.reference_limits.reference_count_limit == reference_count
        assert encoded.reference_limits.candidate_limit == candidate_count
        assert read_exact_bytes(encoded) == material
        assert encoded.to_json_dict()["reference_limits"] == {
            "reference_count_limit": reference_count,
            "candidate_limit": candidate_count,
        }

    covered = {
        key: sum(
            len(part.exact_bytes)
            for part in encoded.material
            if isinstance(part, LiteralPart)
        )
        for key, encoded in accounts.items()
    }
    assert len(set(covered.values())) > 1


def test_a_representation_act_establishes_what_its_coordinates_can_be():
    for value in ("4", None, True, False, 4.0, [], {}):
        with pytest.raises(ExactMaterialPointerError, match="must be an integer"):
            ExactMaterialReferenceLimits(reference_count_limit=value, candidate_limit=64)
        with pytest.raises(ExactMaterialPointerError, match="must be an integer"):
            ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=value)
    with pytest.raises(ExactMaterialPointerError, match="at least 2"):
        ExactMaterialReferenceLimits(reference_count_limit=1, candidate_limit=64)
    with pytest.raises(ExactMaterialPointerError, match="must be positive"):
        ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=0)


def test_an_account_without_an_exact_representation_act_is_refused():
    encoded = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    carried = encoded.to_json_dict()
    assert ExactMaterialPointers.from_json_dict(carried) == encoded

    for absent in (None, "not an object", 7, []):
        with pytest.raises(ExactMaterialPointerError, match="reference limits must be an object"):
            ExactMaterialPointers.from_json_dict(dict(carried, reference_limits=absent))
    for key in ("reference_count_limit", "candidate_limit"):
        partial = {k: v for k, v in carried["reference_limits"].items() if k != key}
        with pytest.raises(ExactMaterialPointerError, match="incomplete"):
            ExactMaterialPointers.from_json_dict(dict(carried, reference_limits=partial))
    with pytest.raises(ExactMaterialPointerError, match="reference limits must be an object"):
        ExactMaterialPointers.from_json_dict({k: v for k, v in carried.items()
                                              if k != "reference_limits"})


# --- refusal pass -----------------------------------------------------------
#
# Every live refusal in this representation boundary, fired. A refusal no test
# reaches is a refusal nobody has verified, and after #2486 — where two of three
# untested coordinate refusals turned out to admit values they asserted to
# exclude — these are what stand between a malformed durable account and a
# read that silently means something else.
#
# Each case also holds that the refusal is *this module's*, never a raw
# TypeError, AttributeError or binascii error escaping from an unguarded
# operation.

_MATERIAL_IDENTITY_OF_AB = hashlib.sha256(b"ab").hexdigest()
_REFERENCE_LIMITS = ExactMaterialReferenceLimits(reference_count_limit=4, candidate_limit=64)


def _account(**differences):
    fields = dict(
        count=2,
        material_identity=_MATERIAL_IDENTITY_OF_AB,
        material=(LiteralPart(b"ab"),),
        reference_limits=_REFERENCE_LIMITS,
    )
    fields.update(differences)
    return ExactMaterialPointers(**fields)


def test_a_literal_part_requires_non_empty_exact_bytes():
    _account()  # the honest account is formable
    for value in ("x", bytearray(b"x"), memoryview(b"x"), None, 1, b""):
        with pytest.raises(ExactMaterialPointerError, match="non-empty exact bytes"):
            LiteralPart(value)


def test_a_reference_part_requires_exact_positions():
    ReferencePart(source_position=0, count=1)  # zero is a lawful source_position
    for value in ("1", None, True, False, 1.0, [], -1):
        with pytest.raises(ExactMaterialPointerError, match="reference source_position"):
            ReferencePart(source_position=value, count=1)
    for value in ("1", None, True, False, 1.0, [], 0, -1):
        with pytest.raises(ExactMaterialPointerError, match="reference count"):
            ReferencePart(source_position=0, count=value)


def test_an_account_establishes_each_coordinate_it_carries():
    for value in ("2", None, True, False, 2.0, [], -1):
        with pytest.raises(ExactMaterialPointerError, match="count"):
            _account(count=value)
    for value in (None, 1, [], b"a" * 64, _MATERIAL_IDENTITY_OF_AB[:63], _MATERIAL_IDENTITY_OF_AB + "0"):
        with pytest.raises(ExactMaterialPointerError, match="material_identity"):
            _account(material_identity=value)
    with pytest.raises(ExactMaterialPointerError, match="hexadecimal"):
        _account(material_identity="z" * 64)
    for value in ([LiteralPart(b"ab")], None, "ab"):
        with pytest.raises(ExactMaterialPointerError, match="exact tuple"):
            _account(material=value)
    with pytest.raises(ExactMaterialPointerError, match="only literals or references"):
        _account(material=(object(),))
    for value in (None, {}, "x", _REFERENCE_LIMITS.to_json_dict()):
        with pytest.raises(ExactMaterialPointerError, match="declare its reference limits"):
            _account(reference_limits=value)


def test_an_account_is_verified_against_its_own_read():
    with pytest.raises(ExactMaterialPointerError, match="does not match count"):
        _account(count=99)
    with pytest.raises(ExactMaterialPointerError, match="does not match material_identity"):
        _account(material_identity="0" * 64)
    # A reference with no preceding material, and one reaching past what exists.
    with pytest.raises(ExactMaterialPointerError, match="already read material"):
        _account(material=(ReferencePart(source_position=0, count=4),), count=4)
    with pytest.raises(ExactMaterialPointerError, match="already read material"):
        _account(material=(LiteralPart(b"ab"), ReferencePart(source_position=0, count=4)), count=6)


def test_a_serialized_account_is_refused_when_it_cannot_be_validated():
    carried = represent_exact_material_pointers(b"the cat jumped the cat jumped").to_json_dict()
    for value in (None, "x", 7, [], ()):
        with pytest.raises(ExactMaterialPointerError, match="must be an object"):
            ExactMaterialPointers.from_json_dict(value)
    for value in (None, "x", {}, 7):
        with pytest.raises(ExactMaterialPointerError, match="material must be a list"):
            ExactMaterialPointers.from_json_dict(dict(carried, material=value))
    for value in ("x", 7, None, []):
        with pytest.raises(ExactMaterialPointerError, match="each part must be an object"):
            ExactMaterialPointers.from_json_dict(dict(carried, material=[value]))
    for kind in ("unsupported", None, 7, "Literal"):
        with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
            ExactMaterialPointers.from_json_dict(dict(carried, material=[{"kind": kind}]))
    with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
        ExactMaterialPointers.from_json_dict(dict(carried, material=[{}]))
    for value in (None, 7, [], b"YWI="):
        with pytest.raises(ExactMaterialPointerError, match="representation must be a string"):
            ExactMaterialPointers.from_json_dict(
                dict(carried, material=[{"kind": "literal", "representation": value}])
            )
    # Malformed base64 raises binascii.Error, and non-ascii raises
    # UnicodeEncodeError; neither may escape as itself.
    for value in ("!!!!", "a", "é", "=YWI", "YW J="):
        with pytest.raises(ExactMaterialPointerError, match="not valid base64"):
            ExactMaterialPointers.from_json_dict(
                dict(carried, material=[{"kind": "literal", "representation": value}])
            )
    with pytest.raises(ExactMaterialPointerError, match="reference source_position"):
        ExactMaterialPointers.from_json_dict(
            dict(carried, material=[{"kind": "reference", "count": 4}])
        )


def test_a_literal_must_carry_the_canonical_encoding_of_its_bytes():
    """Acceptance must not depend on which Python process reads the account.

    `b64decode(validate=True)` accepted `"YWJj===="` as `b"abc"` through Python
    3.11 and refuses it as excess padding from 3.12. An earlier revision
    recorded that leniency as a property of the representation and held it by
    test, which passed on 3.11 and failed on 3.12 — a durable boundary whose
    acceptance moved with the runtime.

    Canonicality is now required explicitly, which is exact and identical
    everywhere. This is stricter than either Python process's default in one
    direction only: a representation this module emits is always accepted, since
    `to_json_dict` emits canonical base64.
    """

    material = b"abc"
    account = represent_exact_material_pointers(material)
    carried = account.to_json_dict()
    assert carried["material"] == [{"kind": "literal", "representation": "YWJj"}]
    assert ExactMaterialPointers.from_json_dict(carried) == account

    for non_canonical in ("YWJj====", "YWJj=", "YWJj=="):
        with pytest.raises(ExactMaterialPointerError, match="not valid base64|not the canonical"):
            ExactMaterialPointers.from_json_dict(
                dict(carried, material=[{"kind": "literal", "representation": non_canonical}])
            )

    # An encoding that decodes to different bytes is still refused, by the
    # material identity rather than by base64.
    with pytest.raises(ExactMaterialPointerError, match="does not match"):
        ExactMaterialPointers.from_json_dict(
            dict(carried, material=[{"kind": "literal", "representation": "YWJk"}])
        )

    # Round-tripping anything this module emits stays exact, including bytes
    # whose canonical encoding carries padding.
    for exact in (b"a", b"ab", b"abc", b"abcd", bytes(range(256))):
        rebuilt = ExactMaterialPointers.from_json_dict(
            represent_exact_material_pointers(exact).to_json_dict()
        )
        assert read_exact_bytes(rebuilt) == exact


def test_read_refuses_material_that_is_not_an_account():
    for value in (None, "x", 7, represent_exact_material_pointers(b"abcd").to_json_dict()):
        with pytest.raises(ExactMaterialPointerError, match="must be ExactMaterialPointers"):
            read_exact_bytes(value)


def test_representation_act_bounds_are_established_before_any_material_is_read():
    for value in ("x", bytearray(b"x"), memoryview(b"x"), None, 1):
        with pytest.raises(ExactMaterialPointerError, match="exact_bytes must be exact bytes"):
            represent_exact_material_pointers(value)
    for value in ("4", None, True, False, 4.0, [], 1, 0, -1):
        with pytest.raises(ExactMaterialPointerError, match="reference_count_limit"):
            represent_exact_material_pointers(b"abcdef", reference_count_limit=value)
    for value in ("4", None, True, False, 4.0, [], 0, -1):
        with pytest.raises(ExactMaterialPointerError, match="candidate_limit"):
            represent_exact_material_pointers(b"abcdef", candidate_limit=value)


def test_read_verifies_an_account_that_was_altered_after_input():
    """The verify branch is unreachable through ordinary input, and live anyway.

    `__post_init__` already checks the count and the material identity against a
    read, so `read_exact_bytes` can never refuse an account
    that was built normally. It is not dead: a frozen dataclass is mutable
    through `object.__setattr__`, which is the in-memory analogue of the durable
    tampering the material identity exists to detect. Held so the branch is verified rather
    than assumed, and so removing it later has to be a decision.
    """

    account = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    assert read_exact_bytes(account) == b"the cat jumped the cat jumped"

    altered = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    object.__setattr__(altered, "count", 99)
    with pytest.raises(ExactMaterialPointerError, match="does not match count"):
        read_exact_bytes(altered)

    altered = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    object.__setattr__(altered, "material_identity", "0" * 64)
    with pytest.raises(ExactMaterialPointerError, match="does not match material_identity"):
        read_exact_bytes(altered)

    # verify=False is the internal path __post_init__ uses, and does not check.
    assert read_exact_bytes(altered, verify=False) == b"the cat jumped the cat jumped"


def test_a_candidate_too_close_to_the_current_position_is_not_referenced():
    account = represent_exact_material_pointers(b"a" * 16, reference_count_limit=4)
    assert read_exact_bytes(account) == b"a" * 16
    references = [p for p in account.material if isinstance(p, ReferencePart)]
    placed = 0
    for part in account.material:
        if isinstance(part, ReferencePart):
            assert part.source_position + part.count <= placed
            placed += part.count
        else:
            placed += len(part.exact_bytes)
    assert references, "a run should still yield at least one reference"
