"""Measure the operator console against real corpus material.

This is the path that matters. `run_persistent_operator_console` is where a
real operator occurrence is preserved, and it is the only path measured here.
Chains that read a file into transient Python objects are not measured, because
what they cost says nothing about what Seed costs -- see
`book_of_seed/developer_compiled_probe_register_001.md`.

    python -m scripts.measure_operator_console_corpus grammar_goold_brown.txt
    python -m scripts.measure_operator_console_corpus grammar_goold_brown.txt --profile

Cost grows with the square of the line count, so the default ladder stops at
800 lines and extrapolates. Recorded runs live in
`book_of_seed/corpus_relation_observation_run_001.md`.

`corpus/` is gitignored, so nothing here runs in CI.
"""

from __future__ import annotations

import argparse
import cProfile
import io
import pstats
import resource
import sys
import time
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for entry in (str(ROOT), str(ROOT / "scripts")):
    if entry not in sys.path:
        sys.path.insert(0, entry)

import seed_local  # noqa: E402

from seed_runtime.events import EventLedger  # noqa: E402

CORPUS = ROOT / "corpus"
LADDER = (25, 50, 100, 200, 400, 800)


def _peak_rss_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def _feed(lines: list[str], count: int) -> tuple[float, int]:
    ledger = EventLedger()
    stream = StringIO("\n".join(lines[:count]) + "\nexit\n")
    started = time.perf_counter()
    seed_local.run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        session_id="s",
        input_stream=stream,
        output_stream=StringIO(),
    )
    return time.perf_counter() - started, len(ledger.list_events("w"))


def _format_duration(seconds: float) -> str:
    for divisor, unit in ((31557600, "years"), (86400, "days"), (3600, "hours"), (60, "min")):
        if seconds >= divisor:
            return f"{seconds / divisor:,.1f} {unit}"
    return f"{seconds:.1f}s"


def measure(name: str) -> None:
    path = CORPUS / name
    if not path.is_file():
        raise SystemExit(f"no such corpus file: {path}")
    lines = path.read_text(encoding="utf-8").split("\n")
    print(f"{name}: {len(lines):,} lines -> run_persistent_operator_console")
    print(f"{'lines':>7} {'events':>8} {'wall':>10} {'per line':>10} {'growth':>8} {'RSS MB':>8}")

    previous: float | None = None
    fitted: list[float] = []
    for count in LADDER:
        if count > len(lines):
            break
        elapsed, events = _feed(lines, count)
        growth = f"x{elapsed / previous:.2f}" if previous else ""
        print(
            f"{count:>7} {events:>8} {elapsed:>9.2f}s {elapsed / count * 1000:>9.1f}ms "
            f"{growth:>8} {_peak_rss_mb():>7.0f}"
        )
        previous = elapsed
        fitted.append(elapsed / count**2)

    if len(fitted) >= 3:
        coefficient = sum(fitted[-3:]) / 3
        whole = coefficient * len(lines) ** 2
        print()
        print(f"fitted t = {coefficient:.3e} * n^2 from the three largest points")
        print(f"whole artifact ({len(lines):,} lines): {_format_duration(whole)}")


def profile(name: str, count: int = 300) -> None:
    lines = (CORPUS / name).read_text(encoding="utf-8").split("\n")
    profiler = cProfile.Profile()
    profiler.enable()
    _feed(lines, count)
    profiler.disable()
    buffer = io.StringIO()
    pstats.Stats(profiler, stream=buffer).sort_stats("cumulative").print_stats(14)
    print(f"cumulative profile, {count} lines")
    for line in buffer.getvalue().splitlines()[4:24]:
        print(line)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="file name inside corpus/")
    parser.add_argument("--profile", action="store_true", help="profile one 300-line run")
    args = parser.parse_args()
    if args.profile:
        profile(args.name)
    else:
        measure(args.name)


if __name__ == "__main__":
    main()
