"""Observe presentation-host capability boundaries as exact invocations."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compiled_material_invocation import (  # noqa: E402
    MaterialImplementationFunction,
    invocation_occurrence,
)


TERMINAL_CAPABILITY_FUNCTIONS = (
    MaterialImplementationFunction(
        identity="terminal-text",
        invocation=("/bin/sh", "-c", "printf text"),
    ),
    MaterialImplementationFunction(
        identity="terminal-identity",
        invocation=("/usr/bin/env",),
    ),
    MaterialImplementationFunction(
        identity="terminal-image",
        invocation=("/bin/sh", "-c", "command -v viu || command -v chafa || false"),
    ),
    MaterialImplementationFunction(
        identity="terminal-video",
        invocation=("/bin/sh", "-c", "command -v mpv || command -v ffplay || false"),
    ),
    MaterialImplementationFunction(
        identity="terminal-caca-frame",
        invocation=(
            "/bin/sh",
            "-c",
            "/usr/bin/ffmpeg -hide_banner -loglevel error "
            "-f lavfi -i color=c=red:s=2x2:d=0.1 -vf format=rgb24 "
            "-frames:v 1 -f caca - | head -c 2048",
        ),
    ),
    MaterialImplementationFunction(
        identity="terminal-termios",
        invocation=("/usr/bin/stty", "-a"),
    ),
    MaterialImplementationFunction(
        identity="terminal-readline",
        invocation=(
            "/bin/bash",
            "--noprofile",
            "--norc",
            "-c",
            "bind -v",
        ),
    ),
)


def terminal_capability_occurrences(*, boundary_identity: str):
    return tuple(
        invocation_occurrence(
            b"",
            function,
            boundary_identity=boundary_identity,
            invocation_position=position,
        )
        for position, function in enumerate(TERMINAL_CAPABILITY_FUNCTIONS)
    )
