from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from terminal_capability_invocation import terminal_capability_occurrences  # noqa: E402


FIDELITY_SUBJECT = "exact_invocation_coordinates"


def test_terminal_capabilities_remain_raw_invocation_coordinates():
    occurrences = terminal_capability_occurrences(
        boundary_identity="terminal-capability-test"
    )

    assert len(occurrences) == 10
    assert {occurrence.implementation_function_identity for occurrence in occurrences} == {
        "terminal-text",
        "terminal-identity",
        "terminal-image",
        "terminal-video",
        "terminal-caca-frame",
        "terminal-termios",
        "terminal-readline",
        "terminal-alsa-material",
        "terminal-pipewire-material",
        "terminal-ffmpeg-audio-material",
    }
    assert all(
        occurrence.stdout_bytes is None or type(occurrence.stdout_bytes) is bytes
        for occurrence in occurrences
    )
    assert all(
        occurrence.stderr_bytes is None or type(occurrence.stderr_bytes) is bytes
        for occurrence in occurrences
    )
