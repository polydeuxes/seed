"""The decoder Stop now carries the outcome the examination actually recorded.

The Stop taken when initial ingress fails to decode used to record a fixed
string in three places:

    dimensions content   "representation insufficiency"
    response_kind        "representation_insufficient"
    operator message     "Representation insufficient: ..."

Two defects, one lexical and one evidentiary.

The lexical one: `suffi*` is banned vocabulary in Book proper, and the word
carries a judgment about a quantity being short of a requirement. Nothing on
this path measures a quantity or names a requirement.

The evidentiary one: the examination distinguishes `decoder_unavailable` from
`bytes_rejected`, and the fixed string collapsed both into one label. The
distinction survived upstream in the examination record, so the collapse was
reconstructible, but the Stop asserted a summary the examination had not made.

Both are fixed by recording the examined outcome itself. This module pins
that, and pins that the two failure outcomes stay apart.

It does not establish that a decoder failure supports a Stop. `#2365` recorded
that as unestablished and it stays unestablished here.
"""

from __future__ import annotations

from io import BytesIO, StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_ingress import run_operator_ingress_attempt
from seed_runtime.operator_ingress_representation import capture_stdin_material

STOP = "operator.ingress.stopping_occurred"
EXAMINED = "operator.ingress.representation_examined"


class UnknownCodecStream(BytesIO):
    """A byte stream whose declared encoding names no codec the decoder has."""

    encoding = "no-such-codec"


def run(stream) -> tuple[list, str]:
    ledger = EventLedger()
    output = StringIO()
    run_operator_ingress_attempt(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        captured_ingress=capture_stdin_material(stream),
        output_stream=output,
    )
    return ledger.list_events("w"), output.getvalue()


@pytest.fixture(scope="module")
def rejected() -> tuple[list, str]:
    return run(BytesIO(b"\xff\n"))


@pytest.fixture(scope="module")
def unavailable() -> tuple[list, str]:
    return run(UnknownCodecStream(b"material\n"))


def only(events: list, kind: str) -> dict:
    matches = [e for e in events if e.kind == kind]
    assert len(matches) == 1
    return matches[0].payload


# --------------------------------------------------------------------------
# Both failure outcomes are reachable, and they are different outcomes.
# --------------------------------------------------------------------------


def test_both_decoder_failures_are_reachable(rejected, unavailable):
    assert only(rejected[0], EXAMINED)["decoder_outcome"] == "bytes_rejected"
    assert only(unavailable[0], EXAMINED)["decoder_outcome"] == "decoder_unavailable"


def test_each_stop_records_its_own_examination_outcome(rejected, unavailable):
    for events, expected in ((rejected[0], "bytes_rejected"), (unavailable[0], "decoder_unavailable")):
        stop = only(events, STOP)
        assert stop["dimensions"]["content"] == expected
        assert stop["response_kind"] == expected


def test_the_stop_restates_the_examination_rather_than_summarising_it(
    rejected, unavailable
):
    """The Stop's content is copied from the examination, not decided again."""
    for events in (rejected[0], unavailable[0]):
        stop = only(events, STOP)
        assert stop["dimensions"]["content"] == only(events, EXAMINED)["decoder_outcome"]
        assert only(events, EXAMINED)["decoder_succeeded"] is False


def test_the_two_stops_are_distinguishable_from_each_other(rejected, unavailable):
    """The defect being fixed: one label for two outcomes."""
    assert only(rejected[0], STOP)["dimensions"]["content"] != (
        only(unavailable[0], STOP)["dimensions"]["content"]
    )
    assert rejected[1] != unavailable[1]


# --------------------------------------------------------------------------
# The operator-facing message.
# --------------------------------------------------------------------------


def test_the_message_names_the_outcome_and_the_mechanism(rejected, unavailable):
    assert rejected[1] == (
        "Decoder outcome bytes_rejected: captured material did not decode under utf-8.\n"
    )
    assert unavailable[1] == (
        "Decoder outcome decoder_unavailable: captured material did not decode "
        "under no-such-codec.\n"
    )


def test_the_message_names_the_mechanism_the_examination_selected(
    rejected, unavailable
):
    for events, output in (rejected, unavailable):
        assert only(events, EXAMINED)["decoder_mechanism"] in output


# --------------------------------------------------------------------------
# The retired wording is gone from what this path yields.
# --------------------------------------------------------------------------


def test_the_retired_wording_appears_nowhere_on_this_path(rejected, unavailable):
    for events, output in (rejected, unavailable):
        assert "suffi" not in output.lower()
        assert "suffi" not in str([e.payload for e in events]).lower()


def test_no_stop_asserts_a_requirement_was_measured(rejected, unavailable):
    """The Stop names a decoder outcome. It names no quantity and no threshold.

    This is what the retired wording asserted and could not support: nothing
    on this path measures how much representation there was, or states how
    much would have been required.
    """
    for events, _ in (rejected, unavailable):
        stop = only(events, STOP)
        assert stop["dimensions"]["authority"] == "closes only this interaction"
        assert stop["dimensions"]["responsibility"] == "competent-local-stopping"
        assert set(stop) - {"dimensions"} == {
            "attempt_ref",
            "closed",
            "provenance_occurrence_refs",
            "mutates_cluster",
            "response_kind",
        }
