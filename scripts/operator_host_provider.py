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
    SuppliedWitnessReadOccurrence,
)


TIME_BOUNDARY_SECOND_COUNT = 2.0
MATERIAL_BYTE_COUNT_BOUNDARY = 1_048_576
PIPE_DRAIN_TIME_BOUNDARY_SECONDS = 0.05
_WITNESS_INVOCATIONS = {
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
    b"scripts.compiled_witness_measurement",
    b"--",
)
_PYTEST_MEASUREMENT_ENVIRONMENT_COORDINATE = (
    "SEED_COMPILED_WITNESS_MEASUREMENT"
)
_PYTEST_CATALOG_ENVIRONMENT_COORDINATE = (
    "SEED_COMPILED_WITNESS_CATALOG"
)
_ROOT = Path(__file__).resolve().parents[1]
_TRUNCATION_LOSS = (
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
        witness_invocation = _WITNESS_INVOCATIONS.get(name)
        if witness_invocation is None:
            raise OperatorHostProviderError("one exact invocation is required")
        invocation = (witness_invocation,)
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
    time_boundary_second_count: float,
    material_byte_count_boundary: int,
    environment: dict[str, str] | None = None,
    working_directory: Path | None = None,
) -> tuple[bool, bool, bool]:
    if (
        type(time_boundary_second_count) is not float
        or time_boundary_second_count <= 0
    ):
        raise TypeError("exact positive time boundary second count required")
    if (
        type(material_byte_count_boundary) is not int
        or material_byte_count_boundary < 1
    ):
        raise TypeError("exact positive material byte count boundary required")
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
    read_occurrences = {"output": [], "error": []}
    invocation_read_position = 0
    time_boundary_reached = False
    output_boundary_reached = False
    error_boundary_reached = False
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
    deadline = time.monotonic() + time_boundary_second_count
    try:
        while streams.get_map():
            now = time.monotonic()
            remaining = deadline - now
            if remaining <= 0:
                if process.poll() is None:
                    if not time_boundary_reached:
                        time_boundary_reached = True
                        end_process()
                    remaining = PIPE_DRAIN_TIME_BOUNDARY_SECONDS
                elif pipe_drain_deadline is None:
                    pipe_drain_deadline = now + PIPE_DRAIN_TIME_BOUNDARY_SECONDS
                    remaining = PIPE_DRAIN_TIME_BOUNDARY_SECONDS
                elif now >= pipe_drain_deadline:
                    for key in streams.get_map().values():
                        if key.data == "output":
                            output_boundary_reached = True
                        else:
                            error_boundary_reached = True
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
                available = (
                    material_byte_count_boundary - supplied_counts[key.data]
                )
                exact = found[:available]
                if exact:
                    read_occurrences[key.data].append(
                        SuppliedWitnessReadOccurrence(
                            exact_bytes=exact,
                            source_boundary=(
                                f"invocation {key.data} read "
                                f"{len(read_occurrences[key.data])}"
                            ),
                            invocation_position=invocation_read_position,
                        )
                    )
                    supplied_counts[key.data] += len(exact)
                    invocation_read_position += 1
                if len(found) > available:
                    if key.data == "output":
                        output_boundary_reached = True
                    else:
                        error_boundary_reached = True
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
        occurrences = tuple(read_occurrences[role])
        supply(
            SuppliedWitnessMaterialOccurrence(
                exact_bytes=b"".join(
                    occurrence.exact_bytes for occurrence in occurrences
                ),
                source_boundary=f"invocation {role}",
                known_loss=(
                    _TRUNCATION_LOSS
                    if time_boundary_reached
                    or (role == "output" and output_boundary_reached)
                    or (role == "error" and error_boundary_reached)
                    else ()
                ),
                read_occurrences=occurrences,
            )
        )
    return time_boundary_reached, output_boundary_reached, error_boundary_reached


def _bounded_artifact(
    path: Path, *, missing_is_known_loss: bool = False
) -> tuple[bytes, bool]:
    try:
        with path.open("rb") as stream:
            material = stream.read(MATERIAL_BYTE_COUNT_BOUNDARY + 1)
    except FileNotFoundError as error:
        if missing_is_known_loss:
            return b"", True
        raise OperatorHostProviderError(
            "exact compiled Witness measurement material required"
        ) from error
    return (
        material[:MATERIAL_BYTE_COUNT_BOUNDARY],
        len(material) > MATERIAL_BYTE_COUNT_BOUNDARY,
    )


def _supply_completion(
    supply: SuppliedWitnessMaterialConsumer,
    *,
    timed_out: bool,
    output_truncated: bool,
    error_truncated: bool,
) -> None:
    invocation_loss = (
        _TRUNCATION_LOSS
        if timed_out or output_truncated or error_truncated
        else ()
    )
    supply(
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=b"",
            source_boundary="invocation completion",
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
        timed_out, output_truncated, error_truncated = _bounded_invocation(
            argv,
            supply=supply,
            time_boundary_second_count=TIME_BOUNDARY_SECOND_COUNT,
            material_byte_count_boundary=MATERIAL_BYTE_COUNT_BOUNDARY,
        )
        _supply_completion(
            supply,
            timed_out=timed_out,
            output_truncated=output_truncated,
            error_truncated=error_truncated,
        )
        return
    with tempfile.TemporaryDirectory(prefix="seed-pytest-measurement-") as directory:
        artifact_path = Path(directory) / "compiled-Witness-measurement"
        catalog_path = Path(directory) / "compiled-Witness-catalog"
        timed_out, output_truncated, error_truncated = _bounded_invocation(
            argv,
            supply=supply,
            time_boundary_second_count=TIME_BOUNDARY_SECOND_COUNT,
            material_byte_count_boundary=MATERIAL_BYTE_COUNT_BOUNDARY,
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
        artifact, artifact_truncated = _bounded_artifact(
            artifact_path,
            missing_is_known_loss=(
                timed_out or output_truncated or error_truncated
            ),
        )
        catalog, catalog_truncated = _bounded_artifact(
            catalog_path,
            missing_is_known_loss=(
                timed_out or output_truncated or error_truncated
            ),
        )
    supply(
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=catalog,
            source_boundary="compiled Witness catalog",
            known_loss=(
                _TRUNCATION_LOSS
                if catalog_truncated
                or timed_out
                or output_truncated
                or error_truncated
                else ()
            ),
        )
    )
    supply(
        SuppliedWitnessMaterialOccurrence(
            exact_bytes=artifact,
            source_boundary="compiled Witness measurement",
            known_loss=(
                _TRUNCATION_LOSS
                if artifact_truncated
                or timed_out
                or output_truncated
                or error_truncated
                else ()
            ),
        )
    )
    _supply_completion(
        supply,
        timed_out=timed_out,
        output_truncated=output_truncated,
        error_truncated=error_truncated,
    )
