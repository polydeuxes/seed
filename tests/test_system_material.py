"""The system boundary: what came back, and who asked for it.

`#2491` adds a third material boundary. The two that existed carry the
operator's material inward and Seed's own material outward; this carries what
the system returned when something was invoked.

The distinction these tests hold hardest is that **nothing here invokes
anything**. An invocation is declared and its result supplied, so a record never
says Seed invoked — which is what keeps the authority question visible instead
of arriving inside a capture path.
"""

from __future__ import annotations

import pytest

from seed_runtime.events import EventLedger, SQLiteEventLedger
from seed_runtime.event import Event
from seed_runtime.system_material import (
    SYSTEM_MATERIAL_OCCURRED_KIND,
    SYSTEM_ORIGIN,
    DeclaredInvocation,
    SystemMaterialError,
    declare_invocation,
    preserve_system_material,
    system_material_bytes,
)


def _declared(**changes):
    fields = dict(
        invocation="ls corpus/",
        declared_performer="operator system-material harness",
        on_behalf_of="this Seed",
    )
    fields.update(changes)
    return DeclaredInvocation(**fields)


def _preserve(ledger, returned=b"a.txt\nb.txt\n", **changes):
    fields = dict(
        workspace_id="w",
        locality_id="sys_000001",
        exact_bytes=returned,
        observed_boundary="operator harness, subprocess stdout",
    )
    fields.update(changes)
    return preserve_system_material(ledger, **fields)


def _declare(ledger, **changes):
    fields = dict(workspace_id="w", locality_id="sys_000001", declared=_declared())
    fields.update(changes)
    return declare_invocation(ledger, **fields)


def test_a_declaration_records_a_declaration_not_an_act():
    ledger = EventLedger()
    declaration = _declare(ledger)

    assert declaration.payload["declared_invocation"] == {
        "invocation": "ls corpus/",
        "declared_performer": "operator system-material harness",
        "on_behalf_of": "this Seed",
    }
    assert declaration.payload["dimensions"]["authority"] == "unestablished"
    support = declaration.payload["dimensions"]["evidence_scope"]
    assert "establishes no act of it" in support
    assert "no Evidence or Authority for this Seed to invoke" in support
    # No coordinate asserts that Seed did not invoke. Not established that it
    # did is not established that it did not, and a caller may name Seed as the
    # declared performer.
    assert "seed_invoked" not in declaration.payload
    assert any("this Seed invoked" in item for item in declaration.payload["unknowns"])
    # The occurrence must not assert the act while recording it Unknown.
    assert any("remains Unknown" in item for item in declaration.payload["unknowns"])
    assert "performed by" not in declaration.payload["dimensions"]["source_provenance"]


def test_system_material_requires_no_invocation():
    """The system yields material nobody asked for, and it is still material.

    An earlier revision made system material inherently an invocation's answer
    and carried the invocation's identity inside it. That excluded unprompted
    material, and it put a relation between two subjects inside one of them.
    """

    ledger = EventLedger()
    unprompted = _preserve(ledger, returned=b"a file changed\n")

    assert unprompted.kind == SYSTEM_MATERIAL_OCCURRED_KIND
    assert unprompted.payload["material_origin"] == SYSTEM_ORIGIN
    for absent in ("declared_invocation", "invocation_event_id", "seed_invoked"):
        assert absent not in unprompted.payload
    assert unprompted.payload["provenance_occurrence_refs"] == []

    # And a declaration beside it relates to it only if something establishes so.
    declaration = _declare(ledger)
    assert declaration.id not in str(unprompted.payload)


def test_returned_material_is_system_origin_and_exact():
    ledger = EventLedger()
    material = bytes(range(256)) * 3
    returned = _preserve(ledger, returned=material)

    assert returned.payload["material_origin"] == SYSTEM_ORIGIN
    assert returned.payload["byte_count"] == len(material)
    assert system_material_bytes(returned) == material
    # Arbitrary bytes, including 0x0A, arrive whole. The console boundary is
    # line-framed and would have cut this at its first newline.
    assert b"\n" in material
    assert len(material) == 768


def test_material_without_a_text_representation_is_still_material():
    ledger = EventLedger()
    decoded = _preserve(ledger, returned=b"a.txt\nb.txt\n")
    rejected = _preserve(ledger, returned=b"\xff\xfe\x00", locality_id="sys_000002")

    assert decoded.payload["text_representation"]["available"] is True
    assert decoded.payload["text_representation"]["decoder_outcome"] == "decoded"
    assert rejected.payload["text_representation"]["available"] is False
    assert rejected.payload["text_representation"]["decoder_outcome"] == "bytes_rejected"
    assert rejected.payload["text_representation"]["decoder_failure"]
    # The occurrence exists either way, and both preserve exact bytes.
    assert system_material_bytes(rejected) == b"\xff\xfe\x00"


def test_empty_material_is_material():
    ledger = EventLedger()
    occurred = _preserve(ledger, returned=b"")

    assert occurred.payload["byte_count"] == 0
    assert system_material_bytes(occurred) == b""
    # Empty is not absent: the occurrence is recorded as having happened.
    assert occurred.payload["dimensions"]["standing"] == "occurred"


def test_the_exchange_is_declared_by_the_caller():
    ledger = EventLedger()
    first = _preserve(ledger, locality_id="sys_000001")
    second = _preserve(ledger, locality_id="sys_000002")

    assert first.locality_id == "sys_000001"
    assert second.locality_id == "sys_000002"
    assert first.payload["dimensions"]["scope_locality"] == "workspace:w;locality:sys_000001"


def test_a_declared_invocation_requires_each_attribution():
    for name in ("invocation", "declared_performer", "on_behalf_of"):
        for value in ("", "   ", None, 1, True, [], b"ls"):
            with pytest.raises(SystemMaterialError, match=name):
                _declared(**{name: value})


def test_preservation_refuses_what_it_cannot_preserve_exactly():
    ledger = EventLedger()
    for value in ("bytes", bytearray(b"x"), memoryview(b"x"), None, 1):
        with pytest.raises(SystemMaterialError, match="exact bytes"):
            _preserve(ledger, returned=value)
    for value in ("", "  ", None, 1, []):
        with pytest.raises(SystemMaterialError, match="boundary"):
            _preserve(ledger, observed_boundary=value)
    for value in ("", "  ", None, 1, []):
        with pytest.raises(SystemMaterialError, match="bounded exchange"):
            _preserve(ledger, locality_id=value)
        with pytest.raises(SystemMaterialError, match="bounded exchange"):
            _declare(ledger, locality_id=value)


def test_exact_bytes_are_validated_or_refused_never_guessed():
    ledger = EventLedger()
    _preserve(ledger, returned=b"a.txt\n")

    with pytest.raises(SystemMaterialError, match="only system material occurrences"):
        system_material_bytes(
            Event(id="evt_x", kind="something.else", workspace_id="w", payload={})
        )
    for payload in ({}, {"exact_bytes_hex": None}, {"exact_bytes_hex": 7}):
        with pytest.raises(SystemMaterialError, match="carries no exact bytes"):
            system_material_bytes(
                Event(id="evt_x", kind=SYSTEM_MATERIAL_OCCURRED_KIND,
                      workspace_id="w", payload=payload)
            )
    with pytest.raises(SystemMaterialError, match="not exact bytes"):
        system_material_bytes(
            Event(id="evt_x", kind=SYSTEM_MATERIAL_OCCURRED_KIND, workspace_id="w",
                  payload={"exact_bytes_hex": "zz", "byte_count": 1})
        )
    with pytest.raises(SystemMaterialError, match="does not match its byte count"):
        system_material_bytes(
            Event(id="evt_x", kind=SYSTEM_MATERIAL_OCCURRED_KIND, workspace_id="w",
                  payload={"exact_bytes_hex": "6100", "byte_count": 99})
        )


def test_system_material_is_not_operator_material():
    """The two boundaries stay separable, which is the point of the split."""

    from seed_runtime.operator_ingress import OPERATOR_ORIGIN, SEED_ORIGIN

    ledger = EventLedger()
    returned = _preserve(ledger)
    assert returned.payload["material_origin"] not in {OPERATOR_ORIGIN, SEED_ORIGIN}
    assert len({SYSTEM_ORIGIN, OPERATOR_ORIGIN, SEED_ORIGIN}) == 3


def test_subject_identities_stay_distinct_across_a_durable_reopen(tmp_path):
    """Two independent subjects must not Assertion one identity.

    `new_id` is process-local, and a durable store reserves only the prefixes it
    knows. Before these were reserved, a fresh process reissued
    `system_material_000001` for a different subject while the event rows stayed
    distinct, so the store accepted both.

    The harness's exchange identity had the same defect and was fixed by
    deriving it from durable contents; these were minted the same way and kept
    it. Held across a genuine close and reopen rather than within one process,
    since within one process the counter alone would hide it.
    """

    database = str(tmp_path / "reopen.db")
    identities = []
    for index in range(3):
        ledger = SQLiteEventLedger(database)
        try:
            material = preserve_system_material(
                ledger,
                workspace_id="w",
                locality_id=f"sys_{index}",
                exact_bytes=f"material {index}".encode(),
                observed_boundary="operator harness",
            )
            declaration = declare_invocation(
                ledger,
                workspace_id="w",
                locality_id=f"sys_{index}",
                declared=_declared(),
            )
        finally:
            ledger.close()
        identities.append((
            material.payload["dimensions"]["identity"],
            declaration.payload["dimensions"]["identity"],
        ))

    material_subjects = [pair[0] for pair in identities]
    invocation_subjects = [pair[1] for pair in identities]
    assert len(set(material_subjects)) == 3, material_subjects
    assert len(set(invocation_subjects)) == 3, invocation_subjects

    # And the exact material is still reconstructible per subject after reopening.
    ledger = SQLiteEventLedger(database)
    try:
        reconstructed = [
            system_material_bytes(event)
            for event in ledger.list("w")
            if event.kind == SYSTEM_MATERIAL_OCCURRED_KIND
        ]
    finally:
        ledger.close()
    assert reconstructed == [b"material 0", b"material 1", b"material 2"]
