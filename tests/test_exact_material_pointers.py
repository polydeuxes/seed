from __future__ import annotations

import base64
import hashlib

import pytest

from seed_runtime.exact_material_pointers import (
    ExactMaterialPointerRule,
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
    assert any(isinstance(part, ReferencePart) for part in encoded.parts)
    assert encoded.byte_count == len(material)
    assert encoded.sha256 == hashlib.sha256(material).hexdigest()


def test_a_reference_may_reuse_bytes_that_an_earlier_reference_read():
    material = b"abcdabcdabcd"
    encoded = ExactMaterialPointers(
        pointer_rule=ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=64),
        byte_count=len(material),
        sha256=hashlib.sha256(material).hexdigest(),
        parts=(
            LiteralPart(b"abcd"),
            ReferencePart(start=0, byte_count=4),
            # These bytes were themselves yielded by the preceding reference.
            ReferencePart(start=4, byte_count=4),
        ),
    )

    assert read_exact_bytes(encoded) == material


def test_references_do_not_depend_on_word_or_token_boundaries():
    material = b"got through the door; through the wall"

    encoded = represent_exact_material_pointers(material)

    assert read_exact_bytes(encoded) == material
    references = [part for part in encoded.parts if isinstance(part, ReferencePart)]
    assert references
    assert max(part.byte_count for part in references) >= len(b"through the ")


def test_arbitrary_bytes_round_trip_without_text_read():
    material = bytes(range(256)) + bytes(range(256))

    encoded = represent_exact_material_pointers(material)
    read = ExactMaterialPointers.from_json_dict(encoded.to_json_dict())

    assert read_exact_bytes(read) == material
    assert any(isinstance(part, ReferencePart) for part in read.parts)


def test_empty_material_is_exactly_representable():
    encoded = represent_exact_material_pointers(b"")

    assert encoded.parts == ()
    assert encoded.byte_count == 0
    assert read_exact_bytes(encoded) == b""


def test_serialized_literal_is_exact_bytes_not_decoded_text():
    encoded = ExactMaterialPointers(
        pointer_rule=ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=64),
        byte_count=3,
        sha256=hashlib.sha256(b"\x00\xffA").hexdigest(),
        parts=(LiteralPart(b"\x00\xffA"),),
    )

    carried = encoded.to_json_dict()

    assert base64.b64decode(carried["parts"][0]["bytes_b64"]) == b"\x00\xffA"
    assert ExactMaterialPointers.from_json_dict(carried) == encoded


def test_forward_or_partially_forward_reference_is_refused():
    digest = hashlib.sha256(b"abcdabcd").hexdigest()

    with pytest.raises(ExactMaterialPointerError, match="already read"):
        ExactMaterialPointers(
            pointer_rule=ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=64),
            byte_count=8,
            sha256=digest,
            parts=(LiteralPart(b"abcd"), ReferencePart(start=2, byte_count=4)),
        )


def test_byte_count_and_commitment_are_verified_against_read():
    digest = hashlib.sha256(b"abc").hexdigest()

    with pytest.raises(ExactMaterialPointerError, match="byte_count"):
        ExactMaterialPointers(
            pointer_rule=ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=64),
            byte_count=4,
            sha256=digest,
            parts=(LiteralPart(b"abc"),),
        )

    with pytest.raises(ExactMaterialPointerError, match="sha256"):
        ExactMaterialPointers(
            pointer_rule=ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=64),
            byte_count=3,
            sha256="0" * 64,
            parts=(LiteralPart(b"abc"),),
        )


def test_malformed_serialized_parts_are_refused():
    honest = represent_exact_material_pointers(b"abcdef").to_json_dict()

    malformed = dict(honest)
    malformed["parts"] = [{"kind": "literal", "bytes_b64": "not base64!"}]
    with pytest.raises(ExactMaterialPointerError, match="base64"):
        ExactMaterialPointers.from_json_dict(malformed)

    malformed = dict(honest)
    malformed["parts"] = [{"kind": "reference", "start": True, "byte_count": 4}]
    with pytest.raises(ExactMaterialPointerError, match="reference start"):
        ExactMaterialPointers.from_json_dict(malformed)

    malformed = dict(honest)
    malformed["parts"] = [{"kind": "word", "value": "through"}]
    with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
        ExactMaterialPointers.from_json_dict(malformed)


def test_encoder_parameters_are_exactly_bounded():
    with pytest.raises(ExactMaterialPointerError, match="exact bytes"):
        represent_exact_material_pointers(bytearray(b"abc"))
    for bad in (True, 1, 1.5, "4"):
        with pytest.raises(ExactMaterialPointerError, match="minimum_reference_byte_count"):
            represent_exact_material_pointers(b"abc", minimum_reference_byte_count=bad)
    for bad in (True, 0, -1, 1.5, "64"):
        with pytest.raises(ExactMaterialPointerError, match="candidate_limit"):
            represent_exact_material_pointers(b"abc", candidate_limit=bad)


def test_the_account_declares_the_representation_act_that_yielded_it():
    """The same material yields different accounts under different bounds, so
    an account that did not disclose its bounds would read as complete."""

    material = (b"the cat jumped the fence. the cat slept. "
                b"a fence is not a cat. the cat jumped the fence.")

    accounts = {
        (minimum, limit): represent_exact_material_pointers(
            material, minimum_reference_byte_count=minimum, candidate_limit=limit
        )
        for minimum, limit in ((2, 64), (4, 64), (8, 64), (4, 1))
    }
    for (minimum, limit), encoded in accounts.items():
        assert encoded.pointer_rule.minimum_reference_byte_count == minimum
        assert encoded.pointer_rule.candidate_limit == limit
        # Read does not depend on the pointer_rule.
        assert read_exact_bytes(encoded) == material
        assert encoded.to_json_dict()["pointer_rule"] == {
            "minimum_reference_byte_count": minimum,
            "candidate_limit": limit,
        }

    covered = {
        key: sum(
            len(part.exact_bytes)
            for part in encoded.parts
            if isinstance(part, LiteralPart)
        )
        for key, encoded in accounts.items()
    }
    # The accounts genuinely differ, which is why the pointer_rule must travel.
    assert len(set(covered.values())) > 1


def test_a_representation_act_establishes_what_its_coordinates_can_be():
    for value in ("4", None, True, False, 4.0, [], {}):
        with pytest.raises(ExactMaterialPointerError, match="must be an integer"):
            ExactMaterialPointerRule(minimum_reference_byte_count=value, candidate_limit=64)
        with pytest.raises(ExactMaterialPointerError, match="must be an integer"):
            ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=value)
    with pytest.raises(ExactMaterialPointerError, match="at least 2"):
        ExactMaterialPointerRule(minimum_reference_byte_count=1, candidate_limit=64)
    with pytest.raises(ExactMaterialPointerError, match="must be positive"):
        ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=0)


def test_an_account_without_a_addressable_representation_act_is_refused():
    encoded = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    carried = encoded.to_json_dict()
    assert ExactMaterialPointers.from_json_dict(carried) == encoded

    for absent in (None, "not an object", 7, []):
        with pytest.raises(ExactMaterialPointerError, match="pointer_rule must be an object"):
            ExactMaterialPointers.from_json_dict(dict(carried, pointer_rule=absent))
    for key in ("minimum_reference_byte_count", "candidate_limit"):
        partial = {k: v for k, v in carried["pointer_rule"].items() if k != key}
        with pytest.raises(ExactMaterialPointerError, match="incomplete"):
            ExactMaterialPointers.from_json_dict(dict(carried, pointer_rule=partial))
    with pytest.raises(ExactMaterialPointerError, match="pointer_rule must be an object"):
        ExactMaterialPointers.from_json_dict({k: v for k, v in carried.items()
                                              if k != "pointer_rule"})


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

_DIGEST_OF_AB = hashlib.sha256(b"ab").hexdigest()
_POINTER_RULE = ExactMaterialPointerRule(minimum_reference_byte_count=4, candidate_limit=64)


def _account(**differences):
    fields = dict(
        byte_count=2,
        sha256=_DIGEST_OF_AB,
        parts=(LiteralPart(b"ab"),),
        pointer_rule=_POINTER_RULE,
    )
    fields.update(differences)
    return ExactMaterialPointers(**fields)


def test_a_literal_part_requires_non_empty_exact_bytes():
    _account()  # the honest account is formable
    for value in ("x", bytearray(b"x"), memoryview(b"x"), None, 1, b""):
        with pytest.raises(ExactMaterialPointerError, match="non-empty exact bytes"):
            LiteralPart(value)


def test_a_reference_part_requires_exact_positions():
    ReferencePart(start=0, byte_count=1)  # zero is a lawful start
    for value in ("1", None, True, False, 1.0, [], -1):
        with pytest.raises(ExactMaterialPointerError, match="reference start"):
            ReferencePart(start=value, byte_count=1)
    for value in ("1", None, True, False, 1.0, [], 0, -1):
        with pytest.raises(ExactMaterialPointerError, match="reference byte_count"):
            ReferencePart(start=0, byte_count=value)


def test_an_account_establishes_each_coordinate_it_carries():
    for value in ("2", None, True, False, 2.0, [], -1):
        with pytest.raises(ExactMaterialPointerError, match="byte_count"):
            _account(byte_count=value)
    for value in (None, 1, [], b"a" * 64, _DIGEST_OF_AB[:63], _DIGEST_OF_AB + "0"):
        with pytest.raises(ExactMaterialPointerError, match="sha256"):
            _account(sha256=value)
    with pytest.raises(ExactMaterialPointerError, match="hexadecimal"):
        _account(sha256="z" * 64)
    for value in ([LiteralPart(b"ab")], None, "ab"):
        with pytest.raises(ExactMaterialPointerError, match="exact tuple"):
            _account(parts=value)
    with pytest.raises(ExactMaterialPointerError, match="only literals or references"):
        _account(parts=(object(),))
    for value in (None, {}, "x", _POINTER_RULE.to_json_dict()):
        with pytest.raises(ExactMaterialPointerError, match="declare the pointer_rule"):
            _account(pointer_rule=value)


def test_an_account_is_verified_against_its_own_read():
    with pytest.raises(ExactMaterialPointerError, match="does not match byte_count"):
        _account(byte_count=99)
    with pytest.raises(ExactMaterialPointerError, match="does not match sha256"):
        _account(sha256="0" * 64)
    # A reference with no preceding material, and one reaching past what exists.
    with pytest.raises(ExactMaterialPointerError, match="already read material"):
        _account(parts=(ReferencePart(start=0, byte_count=4),), byte_count=4)
    with pytest.raises(ExactMaterialPointerError, match="already read material"):
        _account(parts=(LiteralPart(b"ab"), ReferencePart(start=0, byte_count=4)), byte_count=6)


def test_a_serialized_account_is_refused_when_it_cannot_be_validated():
    carried = represent_exact_material_pointers(b"the cat jumped the cat jumped").to_json_dict()
    for value in (None, "x", 7, [], ()):
        with pytest.raises(ExactMaterialPointerError, match="must be an object"):
            ExactMaterialPointers.from_json_dict(value)
    for value in (None, "x", {}, 7):
        with pytest.raises(ExactMaterialPointerError, match="parts must be a list"):
            ExactMaterialPointers.from_json_dict(dict(carried, parts=value))
    for value in ("x", 7, None, []):
        with pytest.raises(ExactMaterialPointerError, match="each part must be an object"):
            ExactMaterialPointers.from_json_dict(dict(carried, parts=[value]))
    for kind in ("unsupported", None, 7, "Literal"):
        with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
            ExactMaterialPointers.from_json_dict(dict(carried, parts=[{"kind": kind}]))
    with pytest.raises(ExactMaterialPointerError, match="unknown exact-material part kind"):
        ExactMaterialPointers.from_json_dict(dict(carried, parts=[{}]))
    for value in (None, 7, [], b"YWI="):
        with pytest.raises(ExactMaterialPointerError, match="bytes_b64 must be a string"):
            ExactMaterialPointers.from_json_dict(
                dict(carried, parts=[{"kind": "literal", "bytes_b64": value}])
            )
    # Malformed base64 raises binascii.Error, and non-ascii raises
    # UnicodeEncodeError; neither may escape as itself.
    for value in ("!!!!", "a", "é", "=YWI", "YW J="):
        with pytest.raises(ExactMaterialPointerError, match="not valid base64"):
            ExactMaterialPointers.from_json_dict(
                dict(carried, parts=[{"kind": "literal", "bytes_b64": value}])
            )
    with pytest.raises(ExactMaterialPointerError, match="reference start"):
        ExactMaterialPointers.from_json_dict(
            dict(carried, parts=[{"kind": "reference", "byte_count": 4}])
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
    assert carried["parts"] == [{"kind": "literal", "bytes_b64": "YWJj"}]
    assert ExactMaterialPointers.from_json_dict(carried) == account

    for non_canonical in ("YWJj====", "YWJj=", "YWJj=="):
        with pytest.raises(ExactMaterialPointerError, match="not valid base64|not the canonical"):
            ExactMaterialPointers.from_json_dict(
                dict(carried, parts=[{"kind": "literal", "bytes_b64": non_canonical}])
            )

    # An encoding that decodes to different bytes is still refused, by the
    # digest rather than by base64.
    with pytest.raises(ExactMaterialPointerError, match="does not match"):
        ExactMaterialPointers.from_json_dict(
            dict(carried, parts=[{"kind": "literal", "bytes_b64": "YWJk"}])
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
        with pytest.raises(ExactMaterialPointerError, match="minimum_reference_byte_count"):
            represent_exact_material_pointers(b"abcdef", minimum_reference_byte_count=value)
    for value in ("4", None, True, False, 4.0, [], 0, -1):
        with pytest.raises(ExactMaterialPointerError, match="candidate_limit"):
            represent_exact_material_pointers(b"abcdef", candidate_limit=value)


def test_read_verifies_an_account_that_was_altered_after_input():
    """The verify branch is unreachable through ordinary input, and live anyway.

    `__post_init__` already checks the count and the digest against a
    read, so `read_exact_bytes` can never refuse an account
    that was built normally. It is not dead: a frozen dataclass is mutable
    through `object.__setattr__`, which is the in-memory analogue of the durable
    tampering the digest exists to detect. Held so the branch is verified rather
    than assumed, and so removing it later has to be a decision.
    """

    account = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    assert read_exact_bytes(account) == b"the cat jumped the cat jumped"

    altered = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    object.__setattr__(altered, "byte_count", 99)
    with pytest.raises(ExactMaterialPointerError, match="does not match byte_count"):
        read_exact_bytes(altered)

    altered = represent_exact_material_pointers(b"the cat jumped the cat jumped")
    object.__setattr__(altered, "sha256", "0" * 64)
    with pytest.raises(ExactMaterialPointerError, match="does not match sha256"):
        read_exact_bytes(altered)

    # verify=False is the internal path __post_init__ uses, and does not check.
    assert read_exact_bytes(altered, verify=False) == b"the cat jumped the cat jumped"


def test_a_candidate_too_close_to_the_current_position_is_not_referenced():
    """A source span must be complete before the part that references it begins.

    Overlapping references are refused by design, so a candidate whose distance
    back is shorter than the minimum byte_count cannot supply one and is skipped.
    Exercised with a run, where every prior occurrence of the key sits closer
    than the minimum until enough material accumulates.
    """

    account = represent_exact_material_pointers(b"a" * 16, minimum_reference_byte_count=4)
    assert read_exact_bytes(account) == b"a" * 16
    references = [p for p in account.parts if isinstance(p, ReferencePart)]
    # Every reference is non-overlapping: its source ends at or before the
    # position where it is placed.
    placed = 0
    for part in account.parts:
        if isinstance(part, ReferencePart):
            assert part.start + part.byte_count <= placed
            placed += part.byte_count
        else:
            placed += len(part.exact_bytes)
    assert references, "a run should still yield at least one reference"
