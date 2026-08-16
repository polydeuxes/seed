#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIRECTORY))
sys.path.insert(0, str(SCRIPT_DIRECTORY.parent))

from compiled_material_invocation import MaterialImplementationFunction
from compiled_stream_measurement_harness import measured_material


def implementation_functions() -> tuple[MaterialImplementationFunction, ...]:
    return (
        MaterialImplementationFunction(
            identity="compiled-0",
            invocation=(
                "/usr/bin/env",
                "-i",
                "/bin/bash",
                "--noprofile",
                "--norc",
                "-n",
            ),
        ),
        MaterialImplementationFunction(
            identity="compiled-1",
            invocation=(
                "/usr/bin/prlimit",
                "--cpu=1",
                "--as=268435456",
                "--nproc=32",
                "--nofile=64",
                "--",
                "/usr/bin/bwrap",
                "--unshare-all",
                "--die-with-parent",
                "--new-session",
                "--clearenv",
                "--ro-bind",
                "/usr",
                "/usr",
                "--symlink",
                "usr/bin",
                "/bin",
                "--symlink",
                "usr/lib",
                "/lib",
                "--symlink",
                "usr/lib64",
                "/lib64",
                "--proc",
                "/proc",
                "--dev",
                "/dev",
                "--tmpfs",
                "/tmp",
                "--dir",
                "/home",
                "--chdir",
                "/tmp",
                "/bin/bash",
                "--noprofile",
                "--norc",
            ),
        ),
    )


def measured_bash_material():
    return measured_material()
