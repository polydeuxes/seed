"""A driven console may present material the operator's escape would consume.

`#2435` measured the deadlock: the Bash guide carries a line whose entire
content is `exit`, the console's process-boundary escape consumes it as control,
and ingestion stopped at 2,957 of 54,264 lines while reporting nothing.

This is bootstrap scaffolding and these tests say so. The interactive console is
unchanged; a non-interactive driver may decline to install the escape, and then
termination comes from EOF — outside the material stream, where no corpus line
can collide with it.
"""

from __future__ import annotations

from io import StringIO

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.preserved_material_measurement import (
    preserved_ingress_occurrences,
)
from scripts import seed_local

MATERIAL = "alpha\nexit\nomega\n"


def _run(escape: bool):
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO(MATERIAL),        # EOF terminates; no trailing exit
        output_stream=StringIO(),
        process_boundary_escape=escape,
    )
    return [
        e.payload["decoded_text"]
        for e in preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s")
    ]


def test_the_operator_console_still_exits_on_the_token():
    """Unchanged, and the default."""
    assert _run(True) == ["alpha\n"]


def test_a_driven_console_may_preserve_the_token_as_material():
    assert _run(False) == ["alpha\n", "exit\n", "omega\n"]


def test_the_default_is_the_interactive_behaviour():
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO(MATERIAL), output_stream=StringIO())
    assert len(preserved_ingress_occurrences(
        ledger, workspace_id="w", session_id="s")) == 1


def test_eof_terminates_either_way():
    """Termination comes from outside the material stream."""
    for escape in (True, False):
        ledger = EventLedger()
        seed_local.run_persistent_operator_console(
            ledger=ledger, workspace_id="w", session_id="s",
            input_stream=StringIO("alpha\n"), output_stream=StringIO(),
            process_boundary_escape=escape)
        assert preserved_ingress_occurrences(
            ledger, workspace_id="w", session_id="s")


def test_the_material_is_preserved_byte_for_byte():
    """No escaping, no capitalisation, no rewriting of the source."""
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO("exit\nExit\nEXIT\n exit\n"),
        output_stream=StringIO(), process_boundary_escape=False)
    assert [
        e.payload["decoded_text"]
        for e in preserved_ingress_occurrences(ledger, workspace_id="w", session_id="s")
    ] == ["exit\n", "Exit\n", "EXIT\n", " exit\n"]


def test_the_cli_console_does_not_expose_suppression():
    """No operator-facing flag: the accommodation is for a driver, not a person."""
    parser = seed_local.build_parser()
    rendered = parser.format_help()
    assert "process-boundary-escape" not in rendered
    assert "process_boundary_escape" not in rendered


def test_a_console_that_declines_the_escape_does_not_announce_it():
    """`#2436` announced a boundary it was not enforcing.

    The notice was unconditional while the check was conditional, so a driven
    console told its reader that `exit` exits while preserving `exit` as
    material.
    """
    out = StringIO()
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO(MATERIAL), output_stream=out,
        process_boundary_escape=False)
    assert "`exit` exits" not in out.getvalue()


def test_the_operator_console_still_announces_it():
    out = StringIO()
    ledger = EventLedger()
    seed_local.run_persistent_operator_console(
        ledger=ledger, workspace_id="w", session_id="s",
        input_stream=StringIO(MATERIAL), output_stream=out)
    assert "Seed console: `exit` exits." in out.getvalue()
