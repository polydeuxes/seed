"""Witness for the live stopping surface.

`08.Stopping:10` names thirteen possible non-movement conditions. It calls them
illustrative rather than exhaustive, and the chapter allows a consumer facing
such Standing to respond with a Stop, a deferral, narrowing, a return to
inquiry, exposure of unmet requirements, or consumer-local non-reliance.

**Nothing here asserts that the console must produce a Stop.** No recorded
Goal, Demand, or response-selection surface appears on this path, so requiring
a Stop producer would manufacture the obligation rather than find it.

What this module does is pin what the runtime's stopping surface actually is,
including two behaviours that are correct and easy to "fix" into defects.
"""

from __future__ import annotations

import inspect
import sys
from io import StringIO
from pathlib import Path

from seed_runtime.events import EventLedger
from seed_runtime import operator_ingress, operator_ingress_representation

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import seed_local  # noqa: E402

STOPPING_KIND = "operator.ingress.stopping_occurred"


class UndecodableByteStream:
    """A byte boundary supplying material Seed's own encoder did not produce."""

    def __init__(self) -> None:
        self.reads = 0

    def readline(self) -> bytes:
        self.reads += 1
        return b"\xff\xfe\n" if self.reads == 1 else b""


def run_console(stream) -> list:
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=stream,
        output_stream=StringIO(),
    )
    return ledger.list()


def test_process_termination_produces_no_stop():
    """Correct behaviour, pinned so it is not "fixed" into a defect.

    `08.Stopping:19` holds `local stop != process termination`. Recording a
    Stop when the loop ends would assert a bounded reason that no occurrence
    established.
    """
    for text in ("a\nexit\n", "a\n"):
        assert not [e for e in run_console(StringIO(text)) if "stop" in e.kind]


def test_reaching_the_end_of_the_act_path_produces_no_stop():
    """`08.Stopping:21` — `a preventing condition != a Stopping occurrence`.

    The console ends on `presentation.emitted`. That is the absence of a next
    act, which the clause distinguishes from a Stopping occurrence.
    """
    for text in ("a\nexit\n", "a\n"):
        assert run_console(StringIO(text))[-1].kind == "operator.presentation.emitted"


def test_ingress_holds_exactly_one_stopping_branch():
    source = inspect.getsource(operator_ingress)
    # Two mentions: the projector's dispatch table, and one record site.
    assert source.count(STOPPING_KIND) == 2
    guard = "if not ingress_examination.succeeded:"
    assert guard in source
    record_site = source.rindex(STOPPING_KIND)
    guard_at = source.index(guard)
    assert guard_at < record_site
    between = source[guard_at:record_site]
    assert "_record(" in between and "def " not in between


def test_capture_has_three_boundaries_and_only_one_re_encodes():
    """Which boundary is exercised decides whether decoding can fail.

    `capture_stdin_material` reads bytes directly from `.buffer` when present,
    accepts bytes supplied directly, and otherwise re-encodes text through an
    adapter. Only the third produces bytes from Seed's own strict encoder.
    """
    source = inspect.getsource(operator_ingress_representation.capture_stdin_material)
    assert "binary.readline()" in source
    assert "isinstance(value, bytes)" in source
    assert 'value.encode(adapter_encoding, errors="strict")' in source


def test_text_adapter_input_cannot_reach_the_stopping_branch():
    """Strict encode followed by strict decode of its own output cannot fail.

    This is a property of the adapter branch, not of the console.
    """
    events = run_console(StringIO("the cat jumped the fence\nexit\n"))
    assert not [e for e in events if e.kind == STOPPING_KIND]


def test_a_byte_boundary_does_reach_the_stopping_branch():
    """The branch is live, not dead code.

    Bytes arriving from a byte boundary were not produced by Seed's encoder and
    can fail the selected strict decoder. Driving the console with such a
    stream records the Stop.
    """
    stops = [e for e in run_console(UndecodableByteStream()) if e.kind == STOPPING_KIND]
    assert len(stops) == 1
    dimensions = stops[0].payload["dimensions"]
    assert dimensions["standing"] == "closed"
    assert dimensions["authority_warrant"] == "closes only this interaction"


def test_the_reachable_stop_carries_pre_recovery_vocabulary():
    """Recorded, not judged.

    The one reachable Stop describes itself with `representation
    insufficiency` and `competent-local-stopping`, and the branch it sits in is
    named `ingress_examination`. `suffi*` and Examination-era vocabulary were
    both removed from Book proper; this runtime surface predates that.

    Whether decoder rejection warrants a *Stop* rather than a deferral,
    narrowing, or exposure of an unmet requirement is unrecovered. The branch
    existing does not settle its constitutional interpretation.
    """
    stops = [e for e in run_console(UndecodableByteStream()) if e.kind == STOPPING_KIND]
    dimensions = stops[0].payload["dimensions"]
    assert dimensions["content"] == "representation insufficiency"
    assert dimensions["responsibility"] == "competent-local-stopping"
    assert "ingress_examination" in inspect.getsource(operator_ingress)


def test_no_recorded_goal_bounded_response_selection_surface_exists():
    """The gap, stated as an observation rather than an obligation.

    A normal console run produces five recorded event kinds. None is a Goal,
    Demand, Gap, Capability, Inquiry, or Question, so no recorded
    goal-bounded response-selection surface exists on this path.

    This is a claim about what is recorded. It does not establish that no
    unrecorded Responsibility reaches such a condition, which these events
    cannot show either way. It does not require any of those surfaces to
    exist. It fails only if the observation stops being true, at which point
    the response-selection question becomes live.
    """
    kinds = {e.kind for e in run_console(StringIO("the cat jumped the fence\nexit\n"))}
    assert kinds == {
        "operator.presentation.formed",
        "operator.presentation.emitted",
        "operator.ingress.raw_material_captured",
        "operator.ingress.representation_examined",
        "operator.ingress.ingress_occurred",
    }
    for absent in ("goal", "demand", "gap", "capability", "inquiry", "question"):
        assert not [k for k in kinds if absent in k]
