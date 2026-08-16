#!/usr/bin/env python3

from __future__ import annotations

import logging
import os
from pathlib import Path
import selectors
import signal
import sys
import time
import traceback
from typing import Hashable

from compiled_material_invocation import (
    MaterialAdmissionOccurrence,
    MaterialImplementationFunction,
    MaterialInvocationOccurrence,
    admit_invocation_occurrences,
)


def piper_implementation_function(
    executable: Path,
    compiled_material: Path,
    *,
    identity: str,
) -> MaterialImplementationFunction:
    return MaterialImplementationFunction(
        identity=identity,
        invocation=(
            str(executable),
            "-m",
            str(compiled_material),
            "--output-raw",
        ),
    )


def piper_material_occurrences(
    references: tuple[Hashable, ...],
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    time_limit_second_count: float,
    material_byte_count_limit: int,
    max_workers: int,
) -> tuple[
    tuple[MaterialInvocationOccurrence, ...],
    MaterialAdmissionOccurrence,
]:
    occurrences = _piper_reference_occurrences(
        references,
        implementation_function,
        boundary_identity=f"{boundary_identity}-invocation",
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
        max_workers=max_workers,
    )
    admission = admit_invocation_occurrences(
        occurrences,
        boundary_identity=f"{boundary_identity}-admission",
    )
    return occurrences, admission


def _piper_reference_occurrences(
    references: tuple[Hashable, ...],
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    time_limit_second_count: float,
    material_byte_count_limit: int,
    max_workers: int,
) -> tuple[MaterialInvocationOccurrence, ...]:
    if type(references) is not tuple or any(
        type(getattr(reference, "exact_material", None)) is not bytes
        for reference in references
    ):
        raise TypeError("Piper inputs require exact references")
    if not isinstance(implementation_function, MaterialImplementationFunction):
        raise TypeError("one exact Piper implementation function is required")
    if type(boundary_identity) is not str or not boundary_identity:
        raise TypeError("one exact boundary identity is required")
    if (
        type(time_limit_second_count) is not float
        or time_limit_second_count <= 0
    ):
        raise TypeError("one exact positive time limit second count is required")
    if (
        type(material_byte_count_limit) is not int
        or material_byte_count_limit < 1
    ):
        raise TypeError("one exact positive material byte count limit is required")
    if type(max_workers) is not int or max_workers < 1:
        raise TypeError("invocation count must be one positive integer")
    if not references:
        return ()

    invocation = implementation_function.invocation
    if (
        len(invocation) != 4
        or invocation[1] != "-m"
        or invocation[3] != "--output-raw"
    ):
        raise ValueError("Piper invocation requires its exact supported shape")

    # Piper's command-line loop can keep a model resident across input lines, but
    # its raw output concatenates those results without a provider-owned boundary.
    # Load the provider once here and fork its already-loaded state instead. Each
    # exact source still gets a distinct stdin/stdout/stderr and child-process EOF,
    # while Piper's own command-line code retains ownership of text decoding.
    from piper import PiperVoice

    voice = PiperVoice.load(Path(invocation[2]))
    return tuple(
        _forked_piper_invocation_occurrence(
            reference.exact_material,
            reference,
            implementation_function,
            voice,
            boundary_identity=boundary_identity,
            invocation_position=position,
            time_limit_second_count=time_limit_second_count,
            material_byte_count_limit=material_byte_count_limit,
        )
        for position, reference in enumerate(references)
    )


def _forked_piper_invocation_occurrence(
    exact_material: bytes,
    source_reference: Hashable,
    implementation_function: MaterialImplementationFunction,
    voice,
    *,
    boundary_identity: str,
    invocation_position: int,
    time_limit_second_count: float,
    material_byte_count_limit: int,
) -> MaterialInvocationOccurrence:
    stdin_read, stdin_write = os.pipe()
    stdout_read, stdout_write = os.pipe()
    stderr_read, stderr_write = os.pipe()
    for stream in (
        sys.stdin,
        sys.stdout,
        sys.stderr,
        sys.__stdin__,
        sys.__stdout__,
        sys.__stderr__,
    ):
        try:
            stream.flush()
        except (AttributeError, OSError):
            pass

    process_identity = os.fork()
    if process_identity == 0:
        try:
            os.dup2(stdin_read, 0)
            os.dup2(stdout_write, 1)
            os.dup2(stderr_write, 2)
            for descriptor in (
                stdin_read,
                stdin_write,
                stdout_read,
                stdout_write,
                stderr_read,
                stderr_write,
            ):
                try:
                    os.close(descriptor)
                except OSError:
                    pass

            # Reuse the interpreter-created standard streams just as the Piper
            # executable does. Seed does not decode the exact input material.
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            import piper.__main__ as piper_main

            # A fresh executable has no handlers inherited from its caller.
            # Restore that condition so every provider diagnostic stays on this
            # occurrence's exact stderr pipe.
            root_logger = logging.getLogger()
            for handler in tuple(root_logger.handlers):
                root_logger.removeHandler(handler)
            root_logger.setLevel(logging.WARNING)
            piper_main.PiperVoice.load = staticmethod(
                lambda *args, **kwargs: voice
            )
            sys.argv = list(implementation_function.invocation)
            piper_main.main()
        except BaseException:
            traceback.print_exc(file=sys.stderr)
            os._exit(1)
        os._exit(0)

    os.close(stdin_read)
    os.close(stdout_write)
    os.close(stderr_write)
    return _capture_forked_piper_occurrence(
        process_identity,
        stdin_write,
        stdout_read,
        stderr_read,
        exact_material,
        source_reference,
        implementation_function,
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
    )


def _capture_forked_piper_occurrence(
    process_identity: int,
    stdin_write: int,
    stdout_read: int,
    stderr_read: int,
    exact_material: bytes,
    source_reference: Hashable,
    implementation_function: MaterialImplementationFunction,
    *,
    boundary_identity: str,
    invocation_position: int,
    time_limit_second_count: float,
    material_byte_count_limit: int,
) -> MaterialInvocationOccurrence:
    streams = selectors.DefaultSelector()
    input_position = 0
    stdout = bytearray()
    stderr = bytearray()
    time_limit_reached = False
    stdout_limit_reached = False
    stderr_limit_reached = False
    status = None

    for descriptor in (stdin_write, stdout_read, stderr_read):
        os.set_blocking(descriptor, False)
    streams.register(stdin_write, selectors.EVENT_WRITE, "stdin")
    streams.register(stdout_read, selectors.EVENT_READ, "stdout")
    streams.register(stderr_read, selectors.EVENT_READ, "stderr")
    deadline = time.monotonic() + time_limit_second_count

    def end_process() -> None:
        try:
            os.kill(process_identity, signal.SIGKILL)
        except ProcessLookupError:
            pass

    try:
        while streams.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0 and not time_limit_reached:
                time_limit_reached = True
                end_process()
            for key, _ in streams.select(max(0.0, min(remaining, 0.05))):
                descriptor = key.fileobj
                if key.data == "stdin":
                    try:
                        count = os.write(
                            descriptor, exact_material[input_position:]
                        )
                    except BrokenPipeError:
                        count = 0
                        input_position = len(exact_material)
                    else:
                        input_position += count
                    if input_position == len(exact_material):
                        streams.unregister(descriptor)
                        os.close(descriptor)
                    continue
                try:
                    found = os.read(descriptor, 65536)
                except BlockingIOError:
                    continue
                if not found:
                    streams.unregister(descriptor)
                    os.close(descriptor)
                    continue
                material = stdout if key.data == "stdout" else stderr
                available = material_byte_count_limit - len(material)
                material.extend(found[:available])
                if len(found) > available:
                    if key.data == "stdout":
                        stdout_limit_reached = True
                    else:
                        stderr_limit_reached = True
                    end_process()
            if status is None:
                waited_identity, found_status = os.waitpid(
                    process_identity, os.WNOHANG
                )
                if waited_identity:
                    status = found_status
                    if stdin_write in tuple(streams.get_map()):
                        streams.unregister(stdin_write)
                        os.close(stdin_write)
    except BaseException:
        end_process()
        raise
    finally:
        streams.close()
        for descriptor in (stdin_write, stdout_read, stderr_read):
            try:
                os.close(descriptor)
            except OSError:
                pass
        if status is None:
            _, status = os.waitpid(process_identity, 0)

    returned = not (
        time_limit_reached or stdout_limit_reached or stderr_limit_reached
    )
    return MaterialInvocationOccurrence(
        boundary_identity=boundary_identity,
        invocation_position=invocation_position,
        exact_material=exact_material,
        implementation_function=implementation_function,
        returned=returned,
        returncode=os.waitstatus_to_exitcode(status) if returned else None,
        stdout_bytes=bytes(stdout),
        stderr_bytes=bytes(stderr),
        source_reference=source_reference,
        time_limit_second_count=time_limit_second_count,
        material_byte_count_limit=material_byte_count_limit,
        time_limit_reached=time_limit_reached,
        stdout_byte_count_limit_reached=stdout_limit_reached,
        stderr_byte_count_limit_reached=stderr_limit_reached,
    )
