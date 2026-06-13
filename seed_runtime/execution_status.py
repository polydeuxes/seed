"""Transient execution-status events for operator-visible activity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, TextIO
import sys


@dataclass(frozen=True)
class ExecutionStatus:
    """Renderer-independent, non-authoritative activity visibility."""

    phase: str
    message: str
    current: int | None = None
    total: int | None = None
    completed: bool = False


class ExecutionStatusConsumer(Protocol):
    """Consumes transient execution status without owning execution state."""

    def consume(self, status: ExecutionStatus) -> None:
        """Observe an execution-status update."""


class NullExecutionStatusConsumer:
    """Default status consumer that preserves execution behavior by doing nothing."""

    def consume(self, status: ExecutionStatus) -> None:
        return None


class RecordingExecutionStatusConsumer:
    """In-memory consumer for tests and non-persistent status inspection."""

    def __init__(self) -> None:
        self.statuses: list[ExecutionStatus] = []

    def consume(self, status: ExecutionStatus) -> None:
        self.statuses.append(status)


class CliExecutionStatusConsumer:
    """Render execution status as CLI operator feedback."""

    def __init__(
        self, stream: TextIO | None = None, *, progress_interval: int = 100
    ) -> None:
        self.stream = stream or sys.stderr
        self.progress_interval = max(1, progress_interval)

    def consume(self, status: ExecutionStatus) -> None:
        if status.current is not None and status.total is not None:
            if status.completed and status.message.endswith("."):
                line = status.message
            elif not self._should_render_progress(status):
                return
            else:
                line = f"{status.message}: {status.current} / {status.total}"
        else:
            line = status.message
        print(line, file=self.stream)

    def _should_render_progress(self, status: ExecutionStatus) -> bool:
        if status.current in (0, status.total):
            return True
        return status.current % self.progress_interval == 0


def emit_status(
    consumer: ExecutionStatusConsumer | None,
    phase: str,
    message: str,
    *,
    current: int | None = None,
    total: int | None = None,
    completed: bool = False,
) -> None:
    """Emit one transient execution-status update if a consumer is present."""

    if consumer is None:
        return
    consumer.consume(
        ExecutionStatus(
            phase=phase,
            message=message,
            current=current,
            total=total,
            completed=completed,
        )
    )
