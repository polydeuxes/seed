#!/usr/bin/env python3
"""Bounded host mechanics for exact opt-in operator invocations."""

from __future__ import annotations

import os
from pathlib import Path
import selectors
import subprocess
import sys
import tempfile
import time

from seed_runtime.supplied_invocation_material import (
    SuppliedWitnessMaterialConsumer,
    SuppliedWitnessMaterialOccurrence,
)


TIME_LIMIT_SECONDS = 2.0
MATERIAL_BYTE_LIMIT = 65536
IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT = 262144
PIPE_DRAIN_LIMIT_SECONDS = 0.05
_IMPLEMENTATIONS = {
    b"ls": b"/usr/bin/ls",
    b"cat": b"/usr/bin/cat",
}
_CALCULATOR_INVOCATION = (b"/usr/bin/gnome-calculator",)
_PYTEST_INVOCATION = (
    os.fsencode(sys.executable),
    b"-m",
    b"pytest",
    b"-q",
    b"-p",
    b"scripts.implementation_function_measurement",
    b"--",
)
_PYTEST_MEASUREMENT_ENVIRONMENT_COORDINATE = (
    "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT"
)
_PYTEST_CATALOG_ENVIRONMENT_COORDINATE = (
    "SEED_IMPLEMENTATION_FUNCTION_CATALOG"
)
_ROOT = Path(__file__).resolve().parents[1]
_LIMIT_LOSS = (
    "material beyond the supplied boundary is not available",
)


class OperatorHostProviderError(ValueError):
    pass


def _invocation_argv(exact_command: bytes) -> tuple[bytes, ...]:
    if type(exact_command) is not bytes or not exact_command.startswith(b"!"):
        raise OperatorHostProviderError("one exact invocation is required")
    if exact_command.endswith(b"\r\n"):
        body = exact_command[:-2]
    elif exact_command.endswith(b"\n"):
        body = exact_command[:-1]
    else:
        body = exact_command
    addressed = body[1:]
    split_at = next(
        (
            position
            for position, byte in enumerate(addressed)
            if byte in (0x20, 0x09)
        ),
        len(addressed),
    )
    name = addressed[:split_at]
    argument = (
        addressed[split_at + 1 :]
        if split_at < len(addressed)
        else b""
    )
    if name == b"pytest":
        invocation = _PYTEST_INVOCATION
    elif name == b"calculator":
        invocation = _CALCULATOR_INVOCATION
    else:
        implementation = _IMPLEMENTATIONS.get(name)
        if implementation is None:
            raise OperatorHostProviderError("one exact invocation is required")
        invocation = (implementation,)
    if b"\x00" in argument:
        raise OperatorHostProviderError("exact material cannot cross this boundary")
    if name == b"calculator":
        if not argument:
            raise OperatorHostProviderError("one exact invocation is required")
        return *invocation, b"--solve=" + argument
    if not argument:
        return invocation
    if name == b"pytest":
        return *invocation, argument
    return *invocation, b"--", argument


def _bounded_invocation(
    argv: tuple[bytes, ...],
    *,
    supply: SuppliedWitnessMaterialConsumer,
    environment: dict[str, str] | None = None,
    working_directory: Path | None = None,
) -> tuple[bool, bool, bool]:
    coordinates = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "bufsize": 0,
        "shell": False,
    }
    if environment is not None:
        coordinates["env"] = environment
    if working_directory is not None:
        coordinates["cwd"] = working_directory
    process = subprocess.Popen(argv, **coordinates)
    if process.stdout is None or process.stderr is None:
        process.kill()
        process.wait()
        raise OperatorHostProviderError("exact supplied material required")

    streams = selectors.DefaultSelector()
    supplied_counts = {"output": 0, "error": 0}
    supplied_positions = {"output": 0, "error": 0}
    time_limit_reached = False
    output_limit_reached = False
    error_limit_reached = False
    pipe_drain_deadline = None

    def end_process() -> None:
        if process.poll() is None:
            try:
                process.kill()
            except ProcessLookupError:
                pass

    for stream, role in ((process.stdout, "output"), (process.stderr, "error")):
        os.set_blocking(stream.fileno(), False)
        streams.register(stream, selectors.EVENT_READ, role)
    deadline = time.monotonic() + TIME_LIMIT_SECONDS
    try:
        while streams.get_map():
            now = time.monotonic()
            remaining = deadline - now
            if remaining <= 0:
                if process.poll() is None:
                    if not time_limit_reached:
                        time_limit_reached = True
                        end_process()
                    remaining = PIPE_DRAIN_LIMIT_SECONDS
                elif pipe_drain_deadline is None:
                    pipe_drain_deadline = now + PIPE_DRAIN_LIMIT_SECONDS
                    remaining = PIPE_DRAIN_LIMIT_SECONDS
                elif now >= pipe_drain_deadline:
                    for key in streams.get_map().values():
                        if key.data == "output":
                            output_limit_reached = True
                        else:
                            error_limit_reached = True
                    break
                else:
                    remaining = pipe_drain_deadline - now
            for key, _ in streams.select(min(remaining, 0.05)):
                stream = key.fileobj
                try:
                    found = os.read(stream.fileno(), 65536)
                except BlockingIOError:
                    continue
                if not found:
                    streams.unregister(stream)
                    stream.close()
                    continue
                available = MATERIAL_BYTE_LIMIT - supplied_counts[key.data]
                exact = found[:available]
                if exact:
                    supply(
                        SuppliedWitnessMaterialOccurrence(
                            exact_bytes=exact,
                            source_boundary=(
                                f"invocation {key.data} occurrence "
                                f"{supplied_positions[key.data]}"
                            ),
                            egress=True,
                        )
                    )
                    supplied_counts[key.data] += len(exact)
                    supplied_positions[key.data] += 1
                if len(found) > available:
                    if key.data == "output":
                        output_limit_reached = True
                    else:
                        error_limit_reached = True
                    end_process()
    except BaseException:
        end_process()
        raise
    finally:
        streams.close()
        for stream in (process.stdout, process.stderr):
            if not stream.closed:
                stream.close()
        process.wait()
    for role in ("output", "error"):
        if supplied_positions[role] == 0:
            supply(
                SuppliedWitnessMaterialOccurrence(
                    exact_bytes=b"",
                    source_boundary=f"invocation {role} occurrence 0",
                    egress=True,
                )
            )
    return time_limit_reached, output_limit_reached, error_limit_reached


def _bounded_artifact(
    path: Path, *, missing_is_known_loss: bool = False
) -> tuple[bytes, bool]:
    try:
        with path.open("rb") as stream:
            material = stream.read(IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT + 1)
    except FileNotFoundError as error:
        if missing_is_known_loss:
            return b"", True
        raise OperatorHostProviderError(
            "exact implementation measurement material required"
        ) from error
    return (
        material[:IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT],
        len(material) > IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT,
    )


def _supply_completion(
    supply: SuppliedWitnessMaterialConsumer,
    *,
    timed_out: bool,
    output_limited: bool,
    error_limited: bool,
) -> None:
    invocation_loss = (
        _LIMIT_LOSS
        if timed_out or output_limited or error_limited
        else ()
    )
    supply(
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=b"",
            source_boundary="invocation completion",
            egress=False,
            known_loss=invocation_loss,
        )
    )


def invoke_operator_host(
    exact_command: bytes,
    supply: SuppliedWitnessMaterialConsumer,
) -> None:
    if not callable(supply):
        raise TypeError("exact supplied material consumer required")
    argv = _invocation_argv(exact_command)
    if argv[: len(_PYTEST_INVOCATION)] != _PYTEST_INVOCATION:
        timed_out, output_limited, error_limited = _bounded_invocation(
            argv,
            supply=supply,
        )
        _supply_completion(
            supply,
            timed_out=timed_out,
            output_limited=output_limited,
            error_limited=error_limited,
        )
        return
    with tempfile.TemporaryDirectory(prefix="seed-pytest-measurement-") as directory:
        artifact_path = Path(directory) / "implementation-measurement"
        catalog_path = Path(directory) / "implementation-catalog"
        timed_out, output_limited, error_limited = _bounded_invocation(
            argv,
            supply=supply,
            environment={
                "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
                _PYTEST_MEASUREMENT_ENVIRONMENT_COORDINATE: str(
                    artifact_path
                ),
                _PYTEST_CATALOG_ENVIRONMENT_COORDINATE: str(catalog_path),
            },
            working_directory=_ROOT,
        )
        artifact, artifact_limited = _bounded_artifact(
            artifact_path,
            missing_is_known_loss=(
                timed_out or output_limited or error_limited
            ),
        )
        catalog, catalog_limited = _bounded_artifact(
            catalog_path,
            missing_is_known_loss=(
                timed_out or output_limited or error_limited
            ),
        )
    supply(
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=catalog,
            source_boundary="implementation function catalog",
            egress=False,
            known_loss=(
                _LIMIT_LOSS
                if catalog_limited
                or timed_out
                or output_limited
                or error_limited
                else ()
            ),
        )
    )
    supply(
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=artifact,
            source_boundary="implementation function measurement",
            egress=False,
            known_loss=(
                _LIMIT_LOSS
                if artifact_limited
                or timed_out
                or output_limited
                or error_limited
                else ()
            ),
        )
    )
    _supply_completion(
        supply,
        timed_out=timed_out,
        output_limited=output_limited,
        error_limited=error_limited,
    )
