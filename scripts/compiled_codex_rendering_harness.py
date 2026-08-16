#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import shutil
import shlex
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_material_invocation import MaterialImplementationFunction


def implementation_functions() -> tuple[MaterialImplementationFunction, ...]:
    executable = shutil.which("codex")
    if executable is None:
        raise ValueError("Codex implementation function is unavailable")
    return (
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=(executable, "--help"),
        ),
        MaterialImplementationFunction(
            identity="compiled-1",
            invocation=(executable, "completion", "bash"),
        ),
        MaterialImplementationFunction(
            identity="compiled-2",
            invocation=(
                "/bin/sh",
                "-c",
                "(sleep 0.5; cat) | TERM=xterm-256color "
                "/usr/bin/script -qefc "
                f"{shlex.quote(executable)}' --no-alt-screen' /dev/null",
            ),
        ),
    )


def rendering_material() -> tuple[bytes, ...]:
    return (
        b"\x03",
        b"\x1b\x03",
        b"\x1b[A\x03",
        b"/\x03",
        b"hello\x03",
    )
