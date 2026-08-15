#!/usr/bin/env python3

from __future__ import annotations

import cProfile
import json
import os
from pathlib import Path
import sqlite3
import threading
from types import CodeType
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ENVIRONMENT_COORDINATE = "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT"
SOURCE_DIRECTORIES = ("seed_runtime", "scripts")

_python: dict[str, list[int]] = {}
_sql: dict[str, int] = {}
_sqlite_connect = sqlite3.connect
_lock = threading.Lock()
_profiler: cProfile.Profile | None = None
_baselines: list[tuple[dict[str, list[int]], dict[str, int]]] = []


def _identity(path: Path, line: int, name: str) -> str:
    try:
        shown = path.relative_to(ROOT)
    except ValueError:
        shown = path
    return f"{shown}:{line}:{name}"


def _source_identity(code: CodeType) -> str | None:
    filename = os.path.abspath(code.co_filename)
    if not filename.startswith(f"{ROOT}{os.sep}"):
        return None
    path = Path(filename)
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return None
    if not relative.parts or relative.parts[0] not in SOURCE_DIRECTORIES:
        return None
    return _identity(path, code.co_firstlineno, code.co_qualname)


def _measure_sql(statement: str) -> None:
    with _lock:
        _sql[statement] = _sql.get(statement, 0) + 1


class MeasuredConnection(sqlite3.Connection):
    def set_trace_callback(
        self, callback: Callable[[str], object] | None
    ) -> None:
        def carry(statement: str) -> None:
            _measure_sql(statement)
            if callback is not None:
                callback(statement)

        super().set_trace_callback(carry)


def _connect(*arguments: object, **coordinates: object) -> sqlite3.Connection:
    coordinates.setdefault("factory", MeasuredConnection)
    connection = _sqlite_connect(*arguments, **coordinates)
    connection.set_trace_callback(None)
    return connection


def _compiled_identities(path: Path) -> tuple[str, ...]:
    try:
        compiled = compile(path.read_bytes(), str(path), "exec")
    except (OSError, SyntaxError, ValueError):
        return ()
    found: list[str] = []
    pending = [compiled]
    while pending:
        code = pending.pop()
        for material in code.co_consts:
            if isinstance(material, CodeType):
                found.append(
                    _identity(path.resolve(), material.co_firstlineno, material.co_qualname)
                )
                pending.append(material)
    return tuple(found)


def implementation_function_identities() -> tuple[str, ...]:
    return tuple(
        sorted(
            identity
            for directory in SOURCE_DIRECTORIES
            for path in (ROOT / directory).rglob("*.py")
            for identity in _compiled_identities(path)
        )
    )


def _profile_coordinates(profiler: cProfile.Profile) -> dict[str, list[int]]:
    found: dict[str, list[int]] = {}
    for entry in profiler.getstats():
        if not isinstance(entry.code, CodeType):
            continue
        identity = _source_identity(entry.code)
        if identity is None:
            continue
        coordinates = found.setdefault(identity, [0, 0, 0])
        coordinates[0] += entry.callcount
        coordinates[1] += round(entry.totaltime * 1_000_000_000)
        coordinates[2] += round(entry.inlinetime * 1_000_000_000)
    return found


def _coordinate_difference(
    current: dict[str, list[int]], prior: dict[str, list[int]]
) -> dict[str, list[int]]:
    return {
        identity: [
            current.get(identity, [0, 0, 0])[coordinate]
            - prior.get(identity, [0, 0, 0])[coordinate]
            for coordinate in range(3)
        ]
        for identity in current.keys() | prior.keys()
    }


def _sql_difference(current: dict[str, int], prior: dict[str, int]) -> dict[str, int]:
    return {
        statement: current.get(statement, 0) - prior.get(statement, 0)
        for statement in current.keys() | prior.keys()
        if current.get(statement, 0) != prior.get(statement, 0)
    }


def _measurement(
    python_coordinates: dict[str, list[int]], sql_coordinates: dict[str, int]
) -> dict[str, object]:
    identities = implementation_function_identities()
    python = {
        identity: {
            "occurrence_count": python_coordinates.get(identity, [0, 0, 0])[0],
            "elapsed_nanoseconds": python_coordinates.get(identity, [0, 0, 0])[1],
            "self_elapsed_nanoseconds": python_coordinates.get(identity, [0, 0, 0])[2],
        }
        for identity in identities
    }
    reference_pair = {
        identity: coordinates
        for identity, coordinates in python.items()
        if identity.startswith("scripts/reference_pair_comparison.py:")
    }
    return {
        "python": python,
        "sql": dict(sorted(sql_coordinates.items())),
        "reference_pair": reference_pair,
    }


def measurement() -> dict[str, object]:
    return _measurement(_python, _sql)


def begin() -> None:
    global _profiler
    if _profiler is not None:
        _profiler.disable()
        _baselines.append((_profile_coordinates(_profiler), dict(_sql)))
        _profiler.enable()
        return
    _python.clear()
    _sql.clear()
    _baselines.clear()
    sqlite3.connect = _connect
    _profiler = cProfile.Profile()
    _profiler.enable()


def finish() -> dict[str, object]:
    global _profiler
    if _profiler is None:
        return measurement()
    _profiler.disable()
    current_python = _profile_coordinates(_profiler)
    if _baselines:
        prior_python, prior_sql = _baselines.pop()
        found = _measurement(
            _coordinate_difference(current_python, prior_python),
            _sql_difference(_sql, prior_sql),
        )
        _profiler.enable()
        return found
    _python.clear()
    _python.update(current_python)
    _profiler = None
    sqlite3.connect = _sqlite_connect
    return measurement()


def pytest_sessionstart(session: object) -> None:
    del session
    begin()


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    del session, exitstatus
    found = finish()
    output = os.environ.get(OUTPUT_ENVIRONMENT_COORDINATE)
    if output:
        Path(output).write_text(
            json.dumps(found, sort_keys=True, separators=(",", ":")),
            encoding="utf-8",
        )
