"""Transient execution-status events for operator-visible activity."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Callable, Protocol, TextIO
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


class ProgressCadence:
    """Bound transient progress updates for long-running item loops."""

    def __init__(
        self,
        *,
        item_interval: int = 500,
        time_interval_seconds: float = 1.0,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        self.item_interval = max(1, item_interval)
        self.time_interval_seconds = max(0.0, time_interval_seconds)
        self.clock = clock
        self._last_current = 0
        self._last_emit_at = clock()

    def should_emit(self, current: int, total: int) -> bool:
        """Return True for first, final, item-interval, or elapsed-time progress."""

        if current <= 0:
            return False
        if current == 1 or current >= total:
            return True
        if current - self._last_current >= self.item_interval:
            return True
        return self.clock() - self._last_emit_at >= self.time_interval_seconds

    def mark_emitted(self, current: int) -> None:
        self._last_current = current
        self._last_emit_at = self.clock()


class ObservationProducerLifecycle:
    """Shared transient lifecycle vocabulary for observation producers.

    The lifecycle standardizes operator-visible work phases around existing
    observation collection, normalization, ingestion, and event writing paths.
    It does not define observation semantics, create observations, append events,
    or derive facts.
    """

    def __init__(
        self, consumer: ExecutionStatusConsumer | None, source_name: str
    ) -> None:
        self.consumer = consumer
        self.source_name = source_name

    def collecting(self) -> None:
        emit_status(
            self.consumer,
            "observation_collection",
            f"Collecting {self.source_name} observations...",
        )

    def collected(self, count: int) -> None:
        emit_status(
            self.consumer,
            "observation_collection",
            f"Collected {count} observations.",
            current=count,
            total=count,
            completed=True,
        )

    def normalizing(self, count: int) -> None:
        emit_status(
            self.consumer,
            "observation_normalization",
            f"Normalizing {self.source_name} observations...",
            current=0,
            total=count,
        )

    def normalized(self, count: int) -> None:
        emit_status(
            self.consumer,
            "observation_normalization",
            f"Normalized {count} observations.",
            current=count,
            total=count,
            completed=True,
        )

    def ingesting(self, count: int) -> None:
        emit_status(
            self.consumer,
            "observation_ingestion",
            f"Ingesting {self.source_name} observations...",
            current=0,
            total=count,
        )

    def completed(self, count: int) -> None:
        emit_status(
            self.consumer,
            "observation_lifecycle",
            f"Completed {self.source_name} observation lifecycle.",
            current=count,
            total=count,
            completed=True,
        )


def emit_progress_if_due(
    consumer: ExecutionStatusConsumer | None,
    cadence: ProgressCadence,
    phase: str,
    message: str,
    *,
    current: int,
    total: int,
) -> None:
    """Emit loop progress only when bounded cadence says it is useful."""

    if consumer is None or not cadence.should_emit(current, total):
        return
    emit_status(
        consumer,
        phase,
        message,
        current=current,
        total=total,
        completed=current >= total,
    )
    cadence.mark_emitted(current)


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
