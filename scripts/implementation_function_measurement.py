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

import pytest


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ENVIRONMENT_COORDINATE = "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT"
SOURCE_DIRECTORIES = ("seed_runtime", "scripts")

_python: dict[str, list[int]] = {}
_sql: dict[str, int] = {}
_sql_occurrences: list[str] = []
_sqlite_connect = sqlite3.connect
_lock = threading.Lock()
_profiler: cProfile.Profile | None = None
_baselines: list[tuple[dict[str, list[int]], int]] = []
_pytest_occurrences: list[dict[str, object]] = []


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
        _sql_occurrences.append(statement)


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


def _sql_since(occurrence_position: int) -> dict[str, int]:
    found: dict[str, int] = {}
    for statement in _sql_occurrences[occurrence_position:]:
        found[statement] = found.get(statement, 0) + 1
    return found


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
        "sql_occurrences": tuple(_sql_occurrences),
        "reference_pair": reference_pair,
        "pytest": tuple(_pytest_occurrences),
    }


def _observed_measurement(
    python_coordinates: dict[str, list[int]], sql_coordinates: dict[str, int]
) -> dict[str, object]:
    return {
        "python": {
            identity: {
                "occurrence_count": coordinates[0],
                "elapsed_nanoseconds": coordinates[1],
                "self_elapsed_nanoseconds": coordinates[2],
            }
            for identity, coordinates in sorted(python_coordinates.items())
            if any(coordinates)
        },
        "sql": dict(sorted(sql_coordinates.items())),
    }


def measurement() -> dict[str, object]:
    return _measurement(_python, _sql)


def _output_measurement(found: dict[str, object]) -> dict[str, object]:
    python_identities = tuple(found["python"])
    python_positions = {
        identity: position for position, identity in enumerate(python_identities)
    }
    sql_material = tuple(found["sql"])
    sql_positions = {
        material: position for position, material in enumerate(sql_material)
    }
    return {
        "python": tuple(
            {"identity": identity, **found["python"][identity]}
            for identity in python_identities
        ),
        "sql": tuple(
            {
                "exact_material": material,
                "occurrence_count": found["sql"][material],
            }
            for material in sql_material
        ),
        "sql_occurrences": tuple(
            sql_positions[material] for material in found["sql_occurrences"]
        ),
        "reference_pair": tuple(
            python_positions[identity] for identity in found["reference_pair"]
        ),
        "pytest": tuple(
            {
                **{
                    name: value
                    for name, value in occurrence.items()
                    if name != "python"
                },
                "python": tuple(
                    {
                        "implementation_function_position": python_positions[
                            identity
                        ],
                        **coordinates,
                    }
                    for identity, coordinates in occurrence["python"].items()
                ),
            }
            for occurrence in found["pytest"]
        ),
    }


def begin() -> None:
    global _profiler
    if _profiler is not None:
        _profiler.disable()
        _baselines.append((_profile_coordinates(_profiler), len(_sql_occurrences)))
        _profiler.enable()
        return
    _python.clear()
    _sql.clear()
    _sql_occurrences.clear()
    _baselines.clear()
    _pytest_occurrences.clear()
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
        prior_python, prior_sql_position = _baselines.pop()
        found = _measurement(
            _coordinate_difference(current_python, prior_python),
            _sql_since(prior_sql_position),
        )
        _profiler.enable()
        return found
    _python.clear()
    _python.update(current_python)
    _profiler = None
    sqlite3.connect = _sqlite_connect
    return measurement()


def _finish_observed() -> dict[str, object]:
    global _profiler
    if _profiler is None or not _baselines:
        raise RuntimeError("one enclosing implementation measurement is required")
    _profiler.disable()
    current_python = _profile_coordinates(_profiler)
    prior_python, prior_sql_position = _baselines.pop()
    found = _observed_measurement(
        _coordinate_difference(current_python, prior_python),
        _sql_since(prior_sql_position),
    )
    _profiler.enable()
    return found


def pytest_sessionstart(session: object) -> None:
    del session
    begin()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: object, nextitem: object):
    del nextitem
    occurrence_position = len(_pytest_occurrences)
    begin()
    sql_occurrence_position = _baselines[-1][1]
    try:
        yield
    finally:
        found = _finish_observed()
    found.pop("sql")
    _pytest_occurrences.append(
        {
            "occurrence_position": occurrence_position,
            "pytest_identity": item.nodeid,
            "first_sql_occurrence_position": sql_occurrence_position,
            "sql_occurrence_count": len(_sql_occurrences) - sql_occurrence_position,
            **found,
        }
    )


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    del session, exitstatus
    found = finish()
    output = os.environ.get(OUTPUT_ENVIRONMENT_COORDINATE)
    if output:
        Path(output).write_text(
            json.dumps(
                _output_measurement(found),
                sort_keys=True,
                separators=(",", ":"),
            ),
            encoding="utf-8",
        )
