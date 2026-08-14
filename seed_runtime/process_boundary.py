"""One no-shell process boundary with bounded exact output material."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
from typing import Sequence


class ProcessBoundaryError(ValueError):
    """A process boundary could not be entered as declared."""


@dataclass(frozen=True)
class ProcessBoundaryResult:
    argv: tuple[str, ...]
    cwd: str
    returncode: int | None
    timed_out: bool
    stdout: bytes
    stderr: bytes
    stdout_total_bytes: int
    stderr_total_bytes: int

    @property
    def stdout_complete(self) -> bool:
        return len(self.stdout) == self.stdout_total_bytes

    @property
    def stderr_complete(self) -> bool:
        return len(self.stderr) == self.stderr_total_bytes


def run_process_boundary(
    cwd: str | Path,
    argv: Sequence[str],
    *,
    timeout_seconds: float = 60.0,
    max_output_bytes: int = 1_000_000,
) -> ProcessBoundaryResult:
    """Run exact arguments without a shell and retain bounded stream prefixes."""

    command = tuple(argv)
    if not command or not all(type(part) is str and part for part in command):
        raise ProcessBoundaryError("a process requires exact non-empty arguments")
    if isinstance(timeout_seconds, bool) or not isinstance(
        timeout_seconds, (int, float)
    ) or timeout_seconds <= 0:
        raise ProcessBoundaryError("a process timeout must be positive")
    if type(max_output_bytes) is not int or max_output_bytes < 0:
        raise ProcessBoundaryError("a process output boundary must be non-negative")
    exact_cwd = str(Path(cwd).resolve(strict=True))

    timed_out = False
    returncode: int | None = None
    with tempfile.TemporaryFile() as stdout_stream, tempfile.TemporaryFile() as stderr_stream:
        try:
            completed = subprocess.run(
                command,
                cwd=exact_cwd,
                stdin=subprocess.DEVNULL,
                stdout=stdout_stream,
                stderr=stderr_stream,
                shell=False,
                timeout=float(timeout_seconds),
                check=False,
            )
        except subprocess.TimeoutExpired:
            timed_out = True
        else:
            returncode = completed.returncode
        stdout_total = stdout_stream.tell()
        stderr_total = stderr_stream.tell()
        stdout_stream.seek(0)
        stderr_stream.seek(0)
        stdout = stdout_stream.read(max_output_bytes)
        stderr = stderr_stream.read(max_output_bytes)

    return ProcessBoundaryResult(
        argv=command,
        cwd=exact_cwd,
        returncode=returncode,
        timed_out=timed_out,
        stdout=stdout,
        stderr=stderr,
        stdout_total_bytes=stdout_total,
        stderr_total_bytes=stderr_total,
    )
