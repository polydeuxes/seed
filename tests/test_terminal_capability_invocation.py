from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from terminal_capability_invocation import terminal_capability_occurrences  # noqa: E402


def test_terminal_capabilities_remain_raw_invocation_coordinates():
    occurrences = terminal_capability_occurrences(
        boundary_identity="terminal-capability-test"
    )

    assert len(occurrences) == 5
    assert {occurrence.implementation_function_identity for occurrence in occurrences} == {
        "terminal-text",
        "terminal-identity",
        "terminal-image",
        "terminal-video",
        "terminal-caca-frame",
    }
    assert all(type(occurrence.stdout_bytes) is bytes for occurrence in occurrences)
    assert all(type(occurrence.stderr_bytes) is bytes for occurrence in occurrences)
