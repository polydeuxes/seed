"""Material occurred, material is available now, and material is retained.

`#2496` separates three things that had been wearing one coat. The occurrence is
permanent; availability is a present-tense answer that changes without anything
being recorded; retention beyond this process is an outward Act requiring an
Authority this module does not have.

The hardest property held here is the one that keeps them separate: **an
occurrence carries no availability coordinate at all**. A payload asserting
`available` would state present-tense Standing in a permanent record, and would
read as true after it stopped being so.
"""

from __future__ import annotations

import os

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.material_availability import (
    MATERIAL_OCCURRED_KIND,
    MaterialAvailabilityError,
    MaterialIdentity,
    ProcessLocalMaterial,
    identity_of_occurrence,
    material_digest,
    record_transient_material,
)

MATERIAL = b"the cat jumped the fence\n" * 40


def _record(ledger, holder, identity, **changes):
    fields = dict(
        workspace_id="w",
        locality_id="s",
        holder=holder,
        identity=identity,
        material_origin="operator",
        observed_boundary="stdin, one frame",
    )
    fields.update(changes)
    return record_transient_material(ledger, **fields)


def test_transient_bytes_are_addressable_while_the_holder_holds_them():
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)

    assert holder.is_available(identity) is True
    assert holder.reconstruct(identity) == MATERIAL
    assert identity.byte_count == len(MATERIAL)
    assert holder.held_count == 1


def test_the_occurrence_does_not_contain_the_body():
    import json

    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)
    event = _record(ledger, holder, identity)

    serialized = json.dumps(event.payload)
    assert MATERIAL.decode() not in serialized
    assert MATERIAL.hex() not in serialized
    for absent in ("exact_bytes_hex", "exact_bytes", "material", "body"):
        assert absent not in event.payload
    # And the occurrence stays a constant size as the material grows.
    tiny = ProcessLocalMaterial()
    small = _record(ledger, tiny, tiny.hold(b"x"))
    huge = ProcessLocalMaterial()
    large = _record(ledger, huge, huge.hold(b"x" * 5_000_000))
    assert abs(len(json.dumps(small.payload)) - len(json.dumps(large.payload))) < 64


def test_the_occurrence_identifies_what_was_held():
    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)
    event = _record(ledger, holder, identity)

    reconstructed = identity_of_occurrence(event)
    assert reconstructed == identity
    assert reconstructed.digest == material_digest(MATERIAL)
    assert reconstructed.byte_count == len(MATERIAL)
    # The identity is enough to ask a holder for the material.
    assert holder.reconstruct(reconstructed) == MATERIAL


def test_releasing_makes_validation_unavailable_and_leaves_the_occurrence():
    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)
    event = _record(ledger, holder, identity)

    holder.release(identity)
    assert holder.is_available(identity) is False
    with pytest.raises(MaterialAvailabilityError, match="not available in this process"):
        holder.reconstruct(identity)

    # The occurrence is untouched. That the material occurred is permanent.
    assert identity_of_occurrence(event) == identity
    assert event.payload["dimensions"]["standing"] == "occurred"
    assert ledger.list("w") == [event]


def test_a_fresh_holder_is_a_process_that_never_held_it():
    """Restarting the holder is the in-process equivalent of restarting."""

    ledger = EventLedger()
    first = ProcessLocalMaterial()
    identity = first.hold(MATERIAL)
    event = _record(ledger, first, identity)

    second = ProcessLocalMaterial()
    assert second.is_available(identity) is False
    with pytest.raises(MaterialAvailabilityError):
        second.reconstruct(identity)
    assert identity_of_occurrence(event) == identity


def test_an_occurrence_carries_no_availability_coordinate():
    """Availability is asked of a holder, never read from a record.

    A payload saying `available` would be a present-tense Assertion in a permanent
    record: true when written, wrong the moment the process ended, and reading
    as true either way. What the occurrence says instead is where the material
    was held at the time, which stays true forever.
    """

    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)
    event = _record(ledger, holder, identity)

    flat = str(event.payload)
    for forbidden in ("available", "availability", "retained", "unavailable"):
        assert f'"{forbidden}"' not in flat
    assert "available" not in event.payload
    assert event.payload["held_at_occurrence"] == "process-local"
    # It records only that this process held it; other sources remain Unknown.
    assert any("does not survive the process" in item
               for item in event.payload["known_loss"])
    assert any("not answerable from this record" in item
               for item in event.payload["unknowns"])


def test_nothing_is_written_anywhere(tmp_path):
    """Holding is retention without an outward act.

    Spooling, a temporary file, memory mapping or restart reconstruction would each be
    Seed preserving material outside itself, which is the Authority question
    `#2496` deliberately does not touch.
    """

    before = set(os.listdir(tmp_path))
    cwd_before = set(os.listdir("."))
    import tempfile
    temp_before = set(os.listdir(tempfile.gettempdir()))

    holder = ProcessLocalMaterial()
    identity = holder.hold(b"y" * 2_000_000)
    ledger = EventLedger()
    _record(ledger, holder, identity)
    assert holder.reconstruct(identity) == b"y" * 2_000_000
    holder.release_all()

    assert set(os.listdir(tmp_path)) == before
    assert set(os.listdir(".")) == cwd_before
    assert set(os.listdir(tempfile.gettempdir())) == temp_before


def test_a_holder_answers_only_the_identity_it_was_asked_for():
    holder = ProcessLocalMaterial()
    first = holder.hold(b"first material")
    second = holder.hold(b"second material")

    assert holder.reconstruct(first) == b"first material"
    assert holder.reconstruct(second) == b"second material"
    assert first.digest != second.digest

    # An identity is digest and extent together, and all three answers agree
    # about it. Keying on the digest alone made an identity with the wrong
    # extent report available, refuse to reconstruct, and release the material that
    # was genuinely held.
    mismatched = MaterialIdentity(digest=first.digest, byte_count=first.byte_count + 1)
    assert holder.is_available(mismatched) is False
    with pytest.raises(MaterialAvailabilityError, match="not available"):
        holder.reconstruct(mismatched)
    holder.release(mismatched)
    assert holder.is_available(first) is True
    assert holder.reconstruct(first) == b"first material"


def test_identical_material_is_one_identity():
    holder = ProcessLocalMaterial()
    a = holder.hold(b"the same exact bytes")
    b = holder.hold(b"the same exact bytes")
    assert a == b
    assert holder.held_count == 1
    assert holder.reconstruct(a) == b"the same exact bytes"


def test_empty_material_occurred():
    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    identity = holder.hold(b"")
    event = _record(ledger, holder, identity)

    assert identity.byte_count == 0
    assert holder.is_available(identity) is True
    assert holder.reconstruct(identity) == b""
    assert identity_of_occurrence(event) == identity


def test_every_refusal_can_be_reached(tmp_path):
    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)

    for value in ("bytes", bytearray(b"x"), memoryview(b"x"), None, 1, True):
        with pytest.raises(MaterialAvailabilityError, match="is bytes"):
            material_digest(value)
        with pytest.raises(MaterialAvailabilityError, match="is bytes"):
            holder.hold(value)

    for value in (None, 1, "z" * 64, "abc", b"a" * 64, identity.digest[:63]):
        with pytest.raises(MaterialAvailabilityError, match="digest"):
            MaterialIdentity(digest=value, byte_count=1)
    for value in ("1", None, True, False, 1.0, [], -1):
        with pytest.raises(MaterialAvailabilityError, match="byte count"):
            MaterialIdentity(digest=identity.digest, byte_count=value)

    for value in (None, "x", 7, []):
        with pytest.raises(MaterialAvailabilityError, match="not present"):
            MaterialIdentity.from_json_dict(value)
    for key in ("digest", "byte_count"):
        partial = {k: v for k, v in identity.to_json_dict().items() if k != key}
        with pytest.raises(MaterialAvailabilityError, match="incomplete"):
            MaterialIdentity.from_json_dict(partial)

    for name in ("material_origin", "observed_boundary", "locality_id"):
        for value in ("", "   ", None, 1, []):
            with pytest.raises(MaterialAvailabilityError, match=name):
                _record(ledger, holder, identity, **{name: value})
    for value in (None, "x", identity.to_json_dict()):
        with pytest.raises(MaterialAvailabilityError, match="identity of what occurred"):
            _record(ledger, holder, value)
    for value in (None, "x", 7):
        with pytest.raises(MaterialAvailabilityError, match="the holder that held it"):
            _record(ledger, value, identity)

    with pytest.raises(MaterialAvailabilityError, match="only transient material"):
        identity_of_occurrence(
            Event(id="evt_x", kind="something.else", workspace_id="w", payload={})
        )
    with pytest.raises(MaterialAvailabilityError, match="not present"):
        identity_of_occurrence(
            Event(id="evt_x", kind=MATERIAL_OCCURRED_KIND, workspace_id="w", payload={})
        )


def test_it_works_the_same_against_a_durable_ledger(tmp_path):
    """The occurrence is durable; the material is not, and that is the point."""

    path = str(tmp_path / "transient.db")
    holder = ProcessLocalMaterial()
    identity = holder.hold(MATERIAL)

    ledger = SQLiteEventLedger(path)
    try:
        event = _record(ledger, holder, identity)
        event_id = event.id
    finally:
        ledger.close()

    # Reopening is a new process as far as material is concerned.
    ledger = SQLiteEventLedger(path)
    fresh = ProcessLocalMaterial()
    try:
        reconstructed = identity_of_occurrence(ledger.get(event_id))
        assert reconstructed == identity
        assert fresh.is_available(reconstructed) is False
        # The occurrence survived exactly; the material did not, and nothing
        # pretends otherwise.
        assert ledger.integrity_of(event_id) == "verified"
    finally:
        ledger.close()


def test_recording_requires_the_holder_that_holds_it():
    """A permanent record must not assert what the function cannot observe.

    Taking only an identity let a caller record that material was held
    process-locally when nothing had ever held it. `record_transient_material`
    receives an identity, and an identity can be computed from bytes that were
    then discarded — so the holder is required and is asked.
    """

    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    never_held = MaterialIdentity.of(b"nobody ever held this")

    with pytest.raises(MaterialAvailabilityError, match="does not hold this material"):
        _record(ledger, holder, never_held)
    assert ledger.list("w") == []

    # A holder that once held it but has released it cannot record it either.
    identity = holder.hold(MATERIAL)
    holder.release(identity)
    with pytest.raises(MaterialAvailabilityError, match="does not hold this material"):
        _record(ledger, holder, identity)

    # And a different holder's holding does not license this one's record.
    other = ProcessLocalMaterial()
    other.hold(MATERIAL)
    with pytest.raises(MaterialAvailabilityError, match="does not hold this material"):
        _record(ledger, holder, identity)

    held_again = holder.hold(MATERIAL)
    event = _record(ledger, holder, held_again)
    assert event.payload["held_at_occurrence"] == "process-local"


def test_the_occurrence_asserts_nothing_about_any_other_source(tmp_path):
    """Process-locally held and externally located are simultaneous.

    Bytes read from a file are both at once, so recording that this process held
    them establishes nothing about whether anything else does. No locator
    recorded is not no external source — the same rule that made a filename
    source-labelled material rather than truth.
    """

    ledger = EventLedger()
    holder = ProcessLocalMaterial()
    # Material that plainly does have an external source, manufactured here so
    # the test does not depend on any particular machine's filesystem.
    source = tmp_path / "source.bin"
    source.write_bytes(MATERIAL)
    identity = holder.hold(source.read_bytes())
    event = _record(ledger, holder, identity, observed_boundary=f"file read {source}")
    assert source.exists()

    flat = str(event.payload)
    for forbidden in ("no external source", "only source", "sole source"):
        assert forbidden not in flat
    assert any("any other source" in item for item in event.payload["unknowns"])
    # What it does say is exactly what happened.
    assert event.payload["held_at_occurrence"] == "process-local"


def test_the_occurrence_identity_survives_a_fresh_process(tmp_path):
    """`transient_material` is durably minted and must be durably reserved.

    **In a fresh process, not a reopen.** `new_id` keeps its counter for the
    lifetime of the interpreter, so reopening a store in the same process
    increments regardless of what the store reserves — an earlier version of
    this test passed with the reservation removed and therefore proved nothing.
    Curator caught it. The collision this guards against needs a genuinely new
    process, where the counter starts again and only the store's reservation
    can prevent a reissue.
    """

    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    program = tmp_path / "mint.py"
    program.write_text(
        "import sys\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "from seed_runtime.events import SQLiteEventLedger\n"
        "from seed_runtime.ids import new_id\n"
        "ledger = SQLiteEventLedger(sys.argv[2])\n"
        "try:\n"
        "    ledger.append('k', 'w', {'identity': new_id(sys.argv[3])})\n"
        "    print(ledger.list('w')[-1].payload['identity'])\n"
        "finally:\n"
        "    ledger.close()\n"
    )
    database = str(tmp_path / "fresh.db")

    minted = []
    for _ in range(3):
        result = subprocess.run(
            [sys.executable, str(program), str(root), database, "transient_material"],
            capture_output=True, text=True, timeout=120,
        )
        assert result.returncode == 0, result.stderr
        minted.append(result.stdout.strip())

    assert len(set(minted)) == 3, minted
    assert minted == [
        "transient_material_000001",
        "transient_material_000002",
        "transient_material_000003",
    ], minted
