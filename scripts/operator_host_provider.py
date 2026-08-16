#!/usr/bin/env python3
"""Bounded host mechanics for exact ``!ls`` and ``!cat`` material."""

from __future__ import annotations

import os
import selectors
import subprocess
import time

from seed_runtime.supplied_invocation_material import (
    SuppliedInvocationMaterial,
    SuppliedMaterialOccurrence,
)


TIME_LIMIT_SECONDS = 2.0
MATERIAL_BYTE_LIMIT = 65536
_IMPLEMENTATIONS = {
    b"ls": b"/usr/bin/ls",
    b"cat": b"/usr/bin/cat",
}
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
    implementation = _IMPLEMENTATIONS.get(name)
    if implementation is None:
        raise OperatorHostProviderError("one exact invocation is required")
    if b"\x00" in argument:
        raise OperatorHostProviderError("exact material cannot cross this boundary")
    if not argument:
        return (implementation,)
    return implementation, b"--", argument


def _bounded_invocation(
    argv: tuple[bytes, ...],
) -> tuple[bytes, bytes, bool, bool, bool]:
    process = subprocess.Popen(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
        shell=False,
    )
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


def invoke_operator_host(exact_command: bytes) -> SuppliedInvocationMaterial:
    argv = _invocation_argv(exact_command)
    output, error, timed_out, output_limited, error_limited = (
        _bounded_invocation(argv)
    )
    timed_loss = _LIMIT_LOSS if timed_out else ()
    return SuppliedInvocationMaterial(
        output_material=SuppliedMaterialOccurrence(
            exact_bytes=output,
            source_boundary="invocation output",
            known_loss=_LIMIT_LOSS if output_limited else timed_loss,
        ),
        error_material=SuppliedMaterialOccurrence(
            exact_bytes=error,
            source_boundary="invocation error",
            known_loss=_LIMIT_LOSS if error_limited else timed_loss,
        ),
        end_material=SuppliedMaterialOccurrence(
            exact_bytes=b"",
            source_boundary="invocation end",
        ),
    )
