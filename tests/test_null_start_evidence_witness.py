"""Null-start evidence witness for E1/E2/E3.

This module is a microscope, not a claim.  It runs the live operator console
from an empty ledger over fixed operator material and reports exactly what Seed
preserved.  Its assertions are deliberately confined to *what is present in the
record*.  Nothing here asserts meaning, relation, structure, or intent, because
none of that is established by ingress -- ``operator.ingress.ingress_occurred``
records ``authority="occurrence-only; meaning Unknown"``.

`render_null_start_evidence` produces the human-readable dump for inspection.
Run it directly to look through the microscope:

    python -m tests.test_null_start_evidence_witness
"""

from __future__ import annotations

import json
from io import StringIO

import pytest

from seed_runtime.events import EventLedger

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import seed_local  # noqa: E402

# Fixed, reproducible operator material.
#
# IMPORTANT: this material is developer-chosen.  Any regularity visible in the
# dump -- recurring newlines, a recurring "# " prefix, a recurring "is a word."
# -- is a property of material written here, not a discovery about Seed or
# about any real acquisition corpus.  Do not choose a measurement because a
# pattern appears in E3 below; that would be selecting the measurement to match
# material we planted, which is the Structure Probe error one level up.
#
# E3 is a small multi-line corpus so that the module can record how the current
# ingress boundary treats multi-line material at all.
E1 = "hello"
E2 = "learn proficient english language"
E3 = "# Nouns\n\nA noun is a word.\n\n# Verbs\n\nA verb is a word."

CAPTURED = "operator.ingress.raw_material_captured"
EXAMINED = "operator.ingress.representation_examined"
OCCURRED = "operator.ingress.ingress_occurred"


def run_null_start() -> list:
    """Drive the live console from an empty ledger.  No fixture is supplied."""
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO("\n".join([E1, E2, E3]) + "\nexit\n"),
        output_stream=StringIO(),
    )
    return ledger.list()


def render_null_start_evidence() -> str:
    """Render every preserved coordinate, without interpreting any of it."""
    events = run_null_start()
    lines = [f"null-start events: {len(events)}", ""]
    for position, event in enumerate(events, start=1):
        lines.append(f"[{position}] {event.kind}  {event.id}")
        for key, value in sorted(event.payload.items()):
            lines.append(f"      {key} = {json.dumps(value, default=str)}")
        lines.append("")
    return "\n".join(lines)


@pytest.fixture(scope="module")
def events() -> list:
    return run_null_start()


def test_null_start_accumulates_occurrence_evidence(events):
    """From nothing, the console preserves a record for every operator line."""
    assert events, "a null start preserved no events at all"
    captured = [e for e in events if e.kind == CAPTURED]
    examined = [e for e in events if e.kind == EXAMINED]
    occurred = [e for e in events if e.kind == OCCURRED]
    # One capture, one examination, one ingress occurrence per delivered line.
    assert len(captured) == len(examined) == len(occurred)
    assert len(captured) > 0


def test_exact_bytes_are_preserved_for_every_capture(events):
    """The measurable substrate: exact bytes, not a paraphrase of them."""
    for event in (e for e in events if e.kind == CAPTURED):
        exact = event.payload.get("exact_bytes_hex")
        assert isinstance(exact, str) and exact
        bytes.fromhex(exact)  # round-trips as bytes, or this raises


def test_decoded_representation_is_preserved_for_every_ingress(events):
    """The second measurable substrate, distinct from the bytes."""
    for event in (e for e in events if e.kind == OCCURRED):
        assert isinstance(event.payload.get("decoded_text"), str)


def test_ingress_claims_only_occurrence_and_records_meaning_unknown(events):
    """Ingress states its own limit in its own record."""
    for event in (e for e in events if e.kind == OCCURRED):
        authority = event.payload["dimensions"]["authority_warrant"]
        assert authority == "occurrence-only; meaning Unknown"


def test_capture_claims_only_occurrence_evidence(events):
    for event in (e for e in events if e.kind == CAPTURED):
        assert (
            event.payload["dimensions"]["authority_warrant"]
            == "occurrence evidence only"
        )


def test_examination_claims_only_decoder_outcome(events):
    for event in (e for e in events if e.kind == EXAMINED):
        assert (
            event.payload["dimensions"]["authority_warrant"]
            == "decoder outcome evidence only"
        )


def test_console_ingress_is_line_bounded_not_document_bounded(events):
    """E3 arrives as several occurrences, not one.

    This is a fact about the current ingress boundary, recorded here because it
    is not obvious and it bounds what any later measurement may range over.  A
    multi-line corpus does not enter as a single preserved material; each line
    is its own capture, examination, and ingress occurrence.
    """
    decoded = [
        e.payload["decoded_text"] for e in events if e.kind == OCCURRED
    ]
    assert decoded[0] == E1 + "\n"
    assert decoded[1] == E2 + "\n"
    # E3 is not present as a single preserved representation.
    assert E3 + "\n" not in decoded
    assert len(decoded) == 2 + len(E3.split("\n"))


def test_null_start_does_not_activate_the_dormant_goal_chain(events):
    """A null start records none of the goal chain's three event kinds.

    Narrow by intent.  This asserts only that the dormant Applicability /
    Admission / Consumption chain did not run, which is consistent with its
    gating input being fixture-only.  It makes no broader claim that no
    semantic standing of any kind was established -- this module is a
    microscope and should not issue negative constitutional findings.
    """
    kinds = {e.kind for e in events}
    for semantic in (
        "operator.interaction.goal_applicability_established",
        "operator.interaction.goal_admitted",
        "operator.interaction.goal_consumed",
    ):
        assert semantic not in kinds


def test_render_produces_inspectable_evidence():
    rendered = render_null_start_evidence()
    assert "operator.ingress.ingress_occurred" in rendered
    assert "exact_bytes_hex" in rendered


if __name__ == "__main__":  # pragma: no cover - inspection entry point
    print(render_null_start_evidence())
