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
    SuppliedInvocationMaterial,
    SuppliedMaterialOccurrence,
)


TIME_LIMIT_SECONDS = 2.0
MATERIAL_BYTE_LIMIT = 65536
IMPLEMENTATION_MEASUREMENT_BYTE_LIMIT = 262144
_IMPLEMENTATIONS = {
    b"ls": b"/usr/bin/ls",
    b"cat": b"/usr/bin/cat",
}
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
    else:
        implementation = _IMPLEMENTATIONS.get(name)
        if implementation is None:
            raise OperatorHostProviderError("one exact invocation is required")
        invocation = (implementation,)
    if b"\x00" in argument:
        raise OperatorHostProviderError("exact material cannot cross this boundary")
    if not argument:
        return invocation
    if name == b"pytest":
        return *invocation, argument
    return *invocation, b"--", argument


def _bounded_invocation(
    argv: tuple[bytes, ...],
    *,
    environment: dict[str, str] | None = None,
    working_directory: Path | None = None,
) -> tuple[bytes, bytes, bool, bool, bool]:
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
    output = bytearray()
    error = bytearray()
    time_limit_reached = False
    output_limit_reached = False
    error_limit_reached = False

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
            remaining = deadline - time.monotonic()
            if remaining <= 0 and not time_limit_reached:
                time_limit_reached = True
                end_process()
                remaining = 0.05
            elif remaining <= 0:
                remaining = 0.05
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
                material = output if key.data == "output" else error
                available = MATERIAL_BYTE_LIMIT - len(material)
                material.extend(found[:available])
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
    return (
        bytes(output),
        bytes(error),
        time_limit_reached,
        output_limit_reached,
        error_limit_reached,
    )


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


def _supplied_invocation(
    output: bytes,
    error: bytes,
    *,
    timed_out: bool,
    output_limited: bool,
    error_limited: bool,
    additional_occurrences: tuple[SuppliedMaterialOccurrence, ...] = (),
) -> SuppliedInvocationMaterial:
    invocation_loss = (
        _LIMIT_LOSS
        if timed_out or output_limited or error_limited
        else ()
    )
    return SuppliedInvocationMaterial(
        occurrences=(
            SuppliedMaterialOccurrence(
                exact_bytes=output,
                source_boundary="invocation output",
                known_loss=invocation_loss,
            ),
            SuppliedMaterialOccurrence(
                exact_bytes=error,
                source_boundary="invocation error",
                known_loss=invocation_loss,
            ),
            *additional_occurrences,
            SuppliedMaterialOccurrence(
                exact_bytes=b"",
                source_boundary="invocation end",
            ),
        ),
        egress_occurrence_positions=(0, 1),
    )


def invoke_operator_host(exact_command: bytes) -> SuppliedInvocationMaterial:
    argv = _invocation_argv(exact_command)
    if argv[: len(_PYTEST_INVOCATION)] != _PYTEST_INVOCATION:
        output, error, timed_out, output_limited, error_limited = (
            _bounded_invocation(argv)
        )
        return _supplied_invocation(
            output,
            error,
            timed_out=timed_out,
            output_limited=output_limited,
            error_limited=error_limited,
        )
    with tempfile.TemporaryDirectory(prefix="seed-pytest-measurement-") as directory:
        artifact_path = Path(directory) / "implementation-measurement"
        catalog_path = Path(directory) / "implementation-catalog"
        output, error, timed_out, output_limited, error_limited = (
            _bounded_invocation(
                argv,
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
    return _supplied_invocation(
        output,
        error,
        timed_out=timed_out,
        output_limited=output_limited,
        error_limited=error_limited,
        additional_occurrences=(
            SuppliedMaterialOccurrence(
                exact_bytes=catalog,
                source_boundary="implementation function catalog",
                known_loss=(
                    _LIMIT_LOSS
                    if catalog_limited
                    or timed_out
                    or output_limited
                    or error_limited
                    else ()
                ),
            ),
            SuppliedMaterialOccurrence(
                exact_bytes=artifact,
                source_boundary="implementation function measurement",
                known_loss=(
                    _LIMIT_LOSS
                    if artifact_limited
                    or timed_out
                    or output_limited
                    or error_limited
                    else ()
                ),
            ),
        ),
    )
