"""Witness for the live stopping surface.

`08.Stopping:10` names thirteen non-movement conditions that may warrant a
bounded Stop: existing bounded horizons, constraint prohibitions, explicit goal
standing, exhaustion findings, impossibility findings, operator boundaries,
evidence gaps, capability Unknowns, authority gaps, resource limits, unresolved
causation, preservation failure, and satisfied scope.

This module records which of them the live console can currently produce, and
pins two facts that are easy to misread as defects but are not.

The last test fails by design.  It names the gap rather than assuming it away.
"""

from __future__ import annotations

import inspect
import sys
from io import StringIO
from pathlib import Path

import pytest

from seed_runtime.events import EventLedger
from seed_runtime import operator_ingress_representation, operator_ingress

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import seed_local  # noqa: E402

STOPPING_KIND = "operator.ingress.stopping_occurred"


def run_console(text: str) -> list:
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=StringIO(text),
        output_stream=StringIO(),
    )
    return ledger.list()


def test_process_termination_produces_no_stop():
    """Correct behaviour, pinned so it is not "fixed" into a defect.

    `08.Stopping:19` holds `local stop != process termination`.  A console
    loop ending is not a constitutional Stop, and recording one at exit would
    assert a bounded reason no occurrence established.
    """
    for text in ("a\nexit\n", "a\n"):
        events = run_console(text)
        assert not [e for e in events if "stop" in e.kind]


def test_a_preventing_condition_is_not_a_stopping_occurrence():
    """`08.Stopping:21` — running out of implemented paths establishes nothing.

    The console ends on `presentation.emitted` in both termination modes.  That
    is the absence of a next act, which the clause distinguishes from a
    Stopping occurrence.
    """
    for text in ("a\nexit\n", "a\n"):
        events = run_console(text)
        assert events[-1].kind == "operator.presentation.emitted"


def test_the_only_stopping_producer_is_decoder_failure():
    """One branch records a Stop, and it is not a goal-derived reason."""
    source = inspect.getsource(operator_ingress)
    # Two occurrences: the projector's dispatch table, and one _record call.
    assert source.count(STOPPING_KIND) == 2
    assert source.count(f'"{STOPPING_KIND}",\n') == 1, "more than one record site"
    guard = "if not ingress_examination.succeeded:"
    assert guard in source
    # The first occurrence is the dispatch table; the record site is the last.
    record_site = source.rindex(STOPPING_KIND)
    guard_at = source.index(guard)
    assert guard_at < record_site, "the record no longer sits under that guard"
    between = source[guard_at:record_site]
    assert "_record(" in between and between.count("def ") == 0, (
        "the stopping record is no longer the branch body of that guard"
    )


def test_that_stopping_branch_is_unreachable_through_the_console():
    """Capture strict-encodes; examination strict-decodes the same bytes.

    `capture_stdin_material` encodes the captured text with
    ``errors="strict"``, and the examination decodes those exact bytes with the
    same mechanism, also strict.  A strict encode followed by a strict decode
    of its own output cannot fail, so `ingress_examination.succeeded` is always
    true on the console path and the Stop branch is dead code there.

    Recorded because it means the live path has no reachable Stop producer at
    all -- a stronger statement than "no goal-derived reason has a producer".
    """
    capture_src = inspect.getsource(operator_ingress_representation.capture_stdin_material)
    assert 'encode(adapter_encoding, errors="strict")' in capture_src
    examine_src = inspect.getsource(operator_ingress_representation)
    assert 'decode(mechanism, errors="strict")' in examine_src

    # And nothing in a normal run reaches it.
    events = run_console("the cat jumped the fence\nexit\n")
    assert not [e for e in events if e.kind == STOPPING_KIND]


def test_unencodable_input_raises_rather_than_stopping():
    """The capture boundary raises before any Stop could be recorded.

    A lone surrogate cannot be strict-encoded, so `capture_stdin_material`
    raises `UnicodeEncodeError`.  Whether that should instead be a bounded
    reason is not decided here; it is recorded because the raise happens
    upstream of every stopping path.
    """

    class LoneSurrogate:
        def __init__(self) -> None:
            self.reads = 0

        def readline(self) -> str:
            self.reads += 1
            return "\udcff\n" if self.reads == 1 else ""

    with pytest.raises(UnicodeEncodeError):
        seed_local.run_persistent_operator_console(
            ledger=EventLedger(),
            workspace_id="w",
            session_id="s",
            input_stream=LoneSurrogate(),
            output_stream=StringIO(),
        )


# `08.Stopping:10`, verbatim.  The clause calls the set illustrative rather
# than exhaustive, so this is not a required checklist -- it is the corpus's
# own enumeration of what a Stop may carry.
NON_MOVEMENT_CONDITIONS = (
    "existing bounded horizons",
    "constraint prohibitions",
    "explicit goal standing",
    "exhaustion findings",
    "impossibility findings",
    "operator boundaries",
    "evidence gaps",
    "capability Unknowns",
    "authority gaps",
    "resource limits",
    "unresolved causation",
    "preservation failure",
    "satisfied scope",
)


def test_live_path_can_produce_a_stop_for_some_named_condition():
    """FAILS BY DESIGN.  This is the gap, stated rather than assumed.

    Of the thirteen non-movement conditions `08.Stopping:10` enumerates, the
    live console can produce a Stop for none.  Its one stopping branch fires on
    decoder failure -- which is not among them -- and that branch is
    unreachable through the console anyway.

    This test goes green when any responsible occurrence on the live path can
    establish a Stop carrying one of these reasons.  It is not asserting that
    all thirteen must be producible, nor that a Goal is the only way to reach
    one.
    """
    events = run_console("the cat jumped the fence\nexit\n")
    stops = [e for e in events if e.kind == STOPPING_KIND]
    assert stops, (
        "the live path produced no Stop for any of the conditions "
        f"08.Stopping:10 names: {', '.join(NON_MOVEMENT_CONDITIONS)}. "
        "Its only stopping branch fires on decoder failure, which is not "
        "among them and is unreachable through the console."
    )
