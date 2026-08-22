"""Transient activity-status events for operator-visible activity."""

from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Callable, Protocol, TextIO
import sys


@dataclass(frozen=True)
class ActivityStatus:
    """Renderer-independent, non-authoritative activity visibility."""

    phase: str
    message: str
    current: int | None = None
    total: int | None = None
    completed: bool = False


class ActivityStatusSink(Protocol):
    """Receives transient activity status without owning activity state."""

    def receive(self, status: ActivityStatus) -> None:
        """Observe an activity-status update."""


class NullActivityStatusSink:
    """Default status sink that preserves activity behavior by doing nothing."""

    def receive(self, status: ActivityStatus) -> None:
        return None


class RecordingActivityStatusSink:
    """In-memory sink for tests and non-persistent status inspection."""

    def __init__(self) -> None:
        self.statuses: list[ActivityStatus] = []

    def receive(self, status: ActivityStatus) -> None:
        self.statuses.append(status)


class CliActivityStatusSink:
    """Render activity status as CLI operator feedback."""

    def __init__(
        self, stream: TextIO | None = None, *, progress_interval: int = 100
    ) -> None:
        self.stream = stream or sys.stderr
        self.progress_interval = max(1, progress_interval)

    def receive(self, status: ActivityStatus) -> None:
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

    def _should_render_progress(self, status: ActivityStatus) -> bool:
        if status.current in (0, status.total):
            return True
        return status.current % self.progress_interval == 0


class ActivityStatusEmitter:
    """Construct and emit status updates without receiving or rendering them.

    Callers use this boundary to publish renderer-independent status payloads.
    Sinks remain responsible for recording, rendering, or ignoring those
    payloads; the emitter does not own activity state or sink behavior.
    """

    def __init__(self, sink: ActivityStatusSink | None) -> None:
        self.sink = sink

    def emit(
        self,
        phase: str,
        message: str,
        *,
        current: int | None = None,
        total: int | None = None,
        completed: bool = False,
    ) -> None:
        """Publish one status update when a sink is attached."""

        if self.sink is None:
            return
        self.sink.receive(
            ActivityStatus(
                phase=phase,
                message=message,
                current=current,
                total=total,
                completed=completed,
            )
        )


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


class ObservationActivity:
    """Shared transient lifecycle vocabulary for observation occurrences.

    The lifecycle standardizes operator-visible work phases around existing
    observation collection, normalization, ingestion, and event writing paths.
    It does not define observation semantics, create observations, append events,
    or derive Assertions.
    """

    def __init__(
        self, sink: ActivityStatusSink | None, source_name: str
    ) -> None:
        self.sink = sink
        self.source_name = source_name

    def collecting(self) -> None:
        emit_status(
            self.sink,
            "observation_collection",
            f"Collecting {self.source_name} observations...",
        )

    def collected(self, count: int) -> None:
        emit_status(
            self.sink,
            "observation_collection",
            f"Collected {count} observations.",
            current=count,
            total=count,
            completed=True,
        )

    def normalizing(self, count: int) -> None:
        emit_status(
            self.sink,
            "observation_normalization",
            f"Normalizing {self.source_name} observations...",
            current=0,
            total=count,
        )

    def normalized(self, count: int) -> None:
        emit_status(
            self.sink,
            "observation_normalization",
            f"Normalized {count} observations.",
            current=count,
            total=count,
            completed=True,
        )

    def ingesting(self, count: int) -> None:
        emit_status(
            self.sink,
            "observation_ingestion",
            f"Ingesting {self.source_name} observations...",
            current=0,
            total=count,
        )

    def completed(self, count: int) -> None:
        emit_status(
            self.sink,
            "observation_lifecycle",
            f"Completed {self.source_name} observation lifecycle.",
            current=count,
            total=count,
            completed=True,
        )


def emit_progress_if_due(
    sink: ActivityStatusSink | None,
    cadence: ProgressCadence,
    phase: str,
    message: str,
    *,
    current: int,
    total: int,
) -> None:
    """Emit loop progress only when bounded cadence says it is useful."""

    if sink is None or not cadence.should_emit(current, total):
        return
    emit_status(
        sink,
        phase,
        message,
        current=current,
        total=total,
        completed=current >= total,
    )
    cadence.mark_emitted(current)


def emit_status(
    sink: ActivityStatusSink | None,
    phase: str,
    message: str,
    *,
    current: int | None = None,
    total: int | None = None,
    completed: bool = False,
) -> None:
    """Emit one transient activity-status update if a sink is present."""

    ActivityStatusEmitter(sink).emit(
        phase,
        message,
        current=current,
        total=total,
        completed=completed,
    )
