"""Do the live ingress occurrences stay inside the boundaries they declare?

Three evidence-producing ingress acts write a limit into their own records:

    raw_material_captured     "occurrence evidence only"
    representation_examined   "decoder outcome evidence only"
    ingress_occurred          "occurrence-only; meaning Unknown"

All three constrain **claim strength**, which is what makes them auditable
against their own contents.

`stopping_occurred` is deliberately excluded. Its declaration, "closes only
this interaction", constrains **closure scope** rather than evidentiary claim
strength, so the same audit does not apply to it. Its constitutional warrant
is separately unexamined: `#2365` recorded that whether decoder rejection
warrants a Stop at all is unrecovered.

**These are runtime-declared limits, not Authority.** This module can
establish that a recorded claim does not exceed its own declared boundary. It
cannot establish that the declared boundary is itself constitutionally
authorized, and nothing here should be read as doing so. Local
self-consistency is not warrant.

Narrows the seam left open at `#2349` to the three evidence-producing acts.

Three findings are pinned rather than repaired. See the tests named
`test_finding_*`.
"""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path

import pytest

from seed_runtime.events import EventLedger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import seed_local  # noqa: E402

CAPTURED = "operator.ingress.raw_material_captured"
EXAMINED = "operator.ingress.representation_examined"
OCCURRED = "operator.ingress.ingress_occurred"


def run(text: str) -> list:
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO(text),
        output_stream=StringIO(),
    )
    return ledger.list()


@pytest.fixture(scope="module")
def events() -> list:
    return run("the cat jumped the fence\nexit\n")


def one(events: list, kind: str) -> dict:
    matches = [e for e in events if e.kind == kind]
    assert len(matches) == 1
    return matches[0].payload


# --------------------------------------------------------------------------
# Each act declares its own limit, and keeps declaring it.
# --------------------------------------------------------------------------


def test_each_act_declares_a_boundary(events):
    assert one(events, CAPTURED)["dimensions"]["authority_warrant"] == (
        "occurrence evidence only"
    )
    assert one(events, EXAMINED)["dimensions"]["authority_warrant"] == (
        "decoder outcome evidence only"
    )
    assert one(events, OCCURRED)["dimensions"]["authority_warrant"] == (
        "occurrence-only; meaning Unknown"
    )


# --------------------------------------------------------------------------
# Capture: "occurrence evidence only"
# --------------------------------------------------------------------------


def test_capture_records_only_material_and_its_own_boundary(events):
    payload = one(events, CAPTURED)
    assert set(payload) - {"dimensions"} == {
        "attempt_ref",
        "byte_count",
        "byte_material_origin",
        "capture_boundary",
        "delimiter_hex",
        "encoding_testimony",
        "eof",
        "exact_bytes_hex",
        "known_loss",
        "lineage",
        "material_role",
        "mutates_cluster",
    }


def test_capture_derived_fields_are_derivable_from_the_material(events):
    """`byte_count` and `delimiter_hex` restate the bytes; they add no claim."""
    payload = one(events, CAPTURED)
    material = bytes.fromhex(payload["exact_bytes_hex"])
    assert payload["byte_count"] == len(material)
    assert payload["delimiter_hex"] == ("0a" if material.endswith(b"\n") else None)


def test_capture_asserts_no_meaning_and_no_stronger_standing(events):
    payload = one(events, CAPTURED)
    assert payload["dimensions"]["standing"] == "captured"
    assert payload["mutates_cluster"] is False
    assert payload["encoding_testimony"] is None
    assert payload["known_loss"]


# --------------------------------------------------------------------------
# representation_examined: "decoder outcome evidence only"
# --------------------------------------------------------------------------


def test_representation_examined_carries_only_the_decoder_outcome(events):
    payload = one(events, EXAMINED)
    assert payload["decoder_outcome"] == "decoded"
    assert payload["decoder_succeeded"] is True
    assert payload["decoder_failure"] is None
    assert payload["capture_event_id"] in payload["lineage"]
    assert payload["unknowns"] == ["true source-relative encoding Unknown"]


def test_representation_examined_preserves_the_encoding_unknown(events):
    """The decoder ran under a chosen mechanism; the true encoding is Unknown."""
    payload = one(events, EXAMINED)
    assert payload["decoder_mechanism"] == "utf-8"
    assert payload["decoder_mechanism_selection"] == "implementation_utf8_fallback"
    assert payload["encoding_testimony"] is None


# --------------------------------------------------------------------------
# Ingress: "occurrence-only; meaning Unknown"
# --------------------------------------------------------------------------


def test_ingress_cites_both_upstream_occurrences(events):
    payload = one(events, OCCURRED)
    assert payload["raw_material_event_id"] in payload["lineage"]
    assert payload["representation_examination_event_id"] in payload["lineage"]


def test_ingress_records_no_interpretation_of_the_material(events):
    """No field names what the material is about, refers to, or requests."""
    payload = one(events, OCCURRED)
    assert set(payload) - {"dimensions"} == {
        "attempt_ref",
        "decoded_text",
        "ingress_kind",
        "known_loss",
        "lineage",
        "mutates_cluster",
        "raw_input",
        "raw_material_event_id",
        "representation_examination_event_id",
    }


# --------------------------------------------------------------------------
# Findings. Pinned, not repaired.
# --------------------------------------------------------------------------


def test_finding_ingress_kind_names_a_weaker_test_than_it_sounds():
    """`ingress_kind` is `empty` or `text`, decided by one delimiter check.

        ingress_kind = "empty" if raw_ingress in {"\\n", "\\r\\n"} else "text"

    So whitespace-only material classifies as `text`. The test performed is
    *does the decoded material consist of nothing but a delimiter*; the name
    `text` asserts more than that, under a record declaring meaning Unknown.

    Whether a decoder outcome warrants calling the result `text` is
    unrecovered. The field is pinned here, not renamed.
    """
    for material, expected in (
        ("the cat jumped the fence", "text"),
        ("", "empty"),
        ("   ", "text"),
        ("\t", "text"),
        ("1", "text"),
    ):
        payload = one(run(material + "\nexit\n"), OCCURRED)
        assert payload["ingress_kind"] == expected


def test_finding_decoded_text_and_raw_input_are_the_same_value():
    """Two fields carrying one value, from two different sources.

    `raw_input` is assigned the ingress text, and `decoded_text` the text the
    decoder produced. They agree on every sample tried,
    including whitespace and non-ASCII. Two names for one value invite a
    later reader to treat them as separate coordinates.
    """
    for material in ("abc", "", "   ", "\ttab", "ünïcode"):
        payload = one(run(material + "\nexit\n"), OCCURRED)
        assert payload["decoded_text"] == payload["raw_input"]


def test_finding_material_role_is_single_valued_on_this_path(events):
    """`material_role` does not discriminate anything on the observed path.

    Every capture on the live initial-ingress path records
    `initial_ingress`. That establishes only that the field discriminates
    nothing *here*; a constant on one path may still carry meaning in a
    broader shared representation.

    The field name overlaps constitutional role vocabulary -- `01.Kinds:28`
    lists participants and roles among relation dimensions -- but no relation
    between this implementation field and constitutional Role is established
    here, and a shared name would not establish one.
    """
    assert one(events, CAPTURED)["material_role"] == "initial_ingress"
    for material in ("abc", "", "   "):
        assert one(run(material + "\nexit\n"), CAPTURED)["material_role"] == (
            "initial_ingress"
        )


def test_self_consistency_does_not_establish_the_boundary(events):
    """Guard against this module being read as more than it is.

    Every test above compares a record against a limit the same record
    declares. That establishes local self-consistency and nothing else. No
    clause has been shown to authorize these boundaries, and this module does
    not attempt to show one.
    """
    for kind in (CAPTURED, EXAMINED, OCCURRED):
        declared = one(events, kind)["dimensions"]["authority_warrant"]
        assert isinstance(declared, str) and declared
