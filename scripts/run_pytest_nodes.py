#!/usr/bin/env python3
"""Collect pytest node addresses once and run them concurrently."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import sys
from time import monotonic


REPOSITORY_DIRECTORY = Path(__file__).resolve().parents[1]
PYTEST_ARGUMENTS = (
    "-m",
    "pytest",
    "-q",
    "--assert=plain",
    "-p",
    "no:cacheprovider",
)


@dataclass(frozen=True)
class ProcessResult:
    number: int
    nodes: tuple[str, ...]
    returncode: int
    seconds: float
    stdout: str
    stderr: str


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect pytest nodes once and run them across sibling processes."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        default=["tests"],
        help="pytest paths or node addresses; defaults to tests",
    )
    parser.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=min(4, os.cpu_count() or 1),
        help="number of sibling pytest processes",
    )
    return parser.parse_args()


def _collect_pytest_nodes(targets: list[str]) -> tuple[str, ...]:
    command = (
        sys.executable,
        *PYTEST_ARGUMENTS,
        "--collect-only",
        *targets,
    )
    completed = subprocess.run(
        command,
        cwd=REPOSITORY_DIRECTORY,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        sys.stdout.write(completed.stdout)
        sys.stderr.write(completed.stderr)
        raise SystemExit(completed.returncode)
    nodes = tuple(
        line.strip()
        for line in completed.stdout.splitlines()
        if "::" in line and not line.startswith(" ")
    )
    if not nodes:
        raise SystemExit("pytest collected no test nodes")
    return nodes


def _divide_pytest_nodes(
    pytest_nodes: tuple[str, ...], jobs: int
) -> tuple[tuple[str, ...], ...]:
    nodes_by_file: dict[str, list[str]] = {}
    for node in pytest_nodes:
        nodes_by_file.setdefault(node.split("::", 1)[0], []).append(node)

    process_count = min(jobs, len(nodes_by_file))
    divided = [[] for _ in range(process_count)]
    node_counts = [0] * process_count
    for file_nodes in sorted(
        nodes_by_file.values(), key=lambda nodes: len(nodes), reverse=True
    ):
        process = min(range(process_count), key=node_counts.__getitem__)
        divided[process].extend(file_nodes)
        node_counts[process] += len(file_nodes)
    return tuple(tuple(process_nodes) for process_nodes in divided)


def _run(number: int, nodes: tuple[str, ...]) -> ProcessResult:
    started = monotonic()
    completed = subprocess.run(
        (sys.executable, *PYTEST_ARGUMENTS, *nodes),
        cwd=REPOSITORY_DIRECTORY,
        capture_output=True,
        text=True,
        check=False,
    )
    return ProcessResult(
        number=number,
        nodes=nodes,
        returncode=completed.returncode,
        seconds=monotonic() - started,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def main() -> int:
    arguments = _arguments()
    if arguments.jobs < 1:
        raise SystemExit("jobs must be positive")

    started = monotonic()
    pytest_nodes = _collect_pytest_nodes(arguments.targets)
    divided = _divide_pytest_nodes(pytest_nodes, arguments.jobs)
    with ThreadPoolExecutor(max_workers=len(divided)) as processes:
        results = tuple(
            processes.map(
                lambda item: _run(*item),
                enumerate(divided, start=1),
            )
        )

    for result in results:
        outcome = "passed" if result.returncode == 0 else "failed"
        print(
            f"process {result.number}: {outcome}; "
            f"{len(result.nodes)} tests; {result.seconds:.2f}s"
        )
        if result.returncode != 0:
            sys.stdout.write(result.stdout)
            sys.stderr.write(result.stderr)

    print(
        f"{len(pytest_nodes)} tests across {len(divided)} processes in "
        f"{monotonic() - started:.2f}s"
    )
    return 1 if any(result.returncode != 0 for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
