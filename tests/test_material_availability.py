from __future__ import annotations

import os
import tempfile

import pytest

from seed_runtime.material_availability import (
    MaterialAvailabilityError,
    MaterialIdentity,
    ProcessLocalMaterial,
    exact_material_identity,
)


MATERIAL = b"the cat jumped the fence\n" * 40


def test_exact_bytes_are_addressable_while_held():
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)

    assert holder.is_available(identity)
    assert holder.read(identity) == MATERIAL
    assert identity.identity == exact_material_identity(MATERIAL)
    assert holder.held_count == 1


def test_release_removes_only_the_exact_identity():
    holder = ProcessLocalMaterial()
    first = holder.hold(b"first material")
    second = holder.hold(b"second material")
    holder.release(first)
    assert not holder.is_available(first)
    assert holder.read(second) == b"second material"


def test_fresh_holder_has_no_material_from_another_holder():
    first = ProcessLocalMaterial()
    identity = first.hold(MATERIAL)
    second = ProcessLocalMaterial()

    assert not second.is_available(identity)
    with pytest.raises(MaterialAvailabilityError, match="not available"):
        second.read(identity)


def test_equal_material_has_one_identity():
    holder = ProcessLocalMaterial()
    first = holder.hold(MATERIAL)
    second = holder.hold(MATERIAL)

    assert first == second
    assert holder.held_count == 1


def test_empty_material_can_be_held():
    holder = ProcessLocalMaterial()
    identity = holder.hold(b"")

    assert holder.read(identity) == b""


def test_release_all_removes_every_held_identity():
    holder = ProcessLocalMaterial()
    identities = (holder.hold(b"a"), holder.hold(b"b"))

    holder.release_all()

    assert holder.held_count == 0
    assert not any(holder.is_available(identity) for identity in identities)


def test_holder_writes_no_files(tmp_path):
    before = set(os.listdir(tmp_path))
    temp_before = set(os.listdir(tempfile.gettempdir()))
    holder = ProcessLocalMaterial()

    identity = holder.hold(b"y" * 2_000_000)
    assert holder.read(identity) == b"y" * 2_000_000
    holder.release_all()

    assert set(os.listdir(tmp_path)) == before
    assert set(os.listdir(tempfile.gettempdir())) == temp_before


def test_every_identity_refusal_is_reachable():
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)

    for value in ("bytes", bytearray(b"x"), memoryview(b"x"), None, 1, True):
        with pytest.raises(MaterialAvailabilityError, match="is bytes"):
            exact_material_identity(value)
        with pytest.raises(MaterialAvailabilityError, match="is bytes"):
            holder.hold(value)

    for value in (None, 1, "z" * 64, "abc", b"a" * 64, identity.identity[:63]):
        with pytest.raises(MaterialAvailabilityError, match="identity"):
            MaterialIdentity(identity=value)

    for value in (None, "x", 7, []):
        with pytest.raises(MaterialAvailabilityError, match="not present"):
            MaterialIdentity.from_json_dict(value)
    with pytest.raises(MaterialAvailabilityError, match="incomplete"):
        MaterialIdentity.from_json_dict({})
