#!/usr/bin/env python3

from __future__ import annotations

import cProfile
from collections import deque
import dis
from functools import lru_cache
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import threading
from types import CodeType
from typing import Callable

import pytest

from scripts.book_admission import book_admission


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ENVIRONMENT_COORDINATE = "SEED_IMPLEMENTATION_FUNCTION_MEASUREMENT"
CATALOG_OUTPUT_ENVIRONMENT_COORDINATE = (
    "SEED_IMPLEMENTATION_FUNCTION_CATALOG"
)
SOURCE_DIRECTORIES = ("seed_runtime", "scripts")
SQL_INVOCATION_NAMES = frozenset(("execute", "executemany", "executescript"))

_python: dict[str, list[int]] = {}
_sql: dict[str, int] = {}
_sql_occurrences: list[str] = []
_sql_invocations: dict[str, int] = {}
_sql_invocation_occurrences: list[str | None] = []
_sql_statement_invocations: list[int | None] = []
_sqlite_connect = sqlite3.connect
_lock = threading.Lock()
_profiler: cProfile.Profile | None = None
_enclosing_measurement_coordinates: list[
    tuple[dict[str, list[int]], int, int]
] = []
_pytest_occurrences: list[dict[str, object]] = []
_PYTEST_SUBJECT_COORDINATES = pytest.StashKey[dict[str, object] | None]()
_active_sql_invocations = threading.local()


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
    active = getattr(_active_sql_invocations, "positions", ())
    with _lock:
        _sql[statement] = _sql.get(statement, 0) + 1
        _sql_occurrences.append(statement)
        _sql_statement_invocations.append(active[-1] if active else None)


def _begin_sql_invocation(frame: object, name: str) -> int:
    identity = _frame_sql_invocation_identity(frame, name)
    with _lock:
        position = len(_sql_invocation_occurrences)
        _sql_invocation_occurrences.append(identity)
        if identity is not None:
            _sql_invocations[identity] = _sql_invocations.get(identity, 0) + 1
    positions = getattr(_active_sql_invocations, "positions", None)
    if positions is None:
        positions = []
        _active_sql_invocations.positions = positions
    positions.append(position)
    return position


def _finish_sql_invocation(position: int) -> None:
    positions = _active_sql_invocations.positions
    if not positions or positions.pop() != position:
        raise RuntimeError("SQL invocation occurrence order changed")


def _invoke_sql(
    invocation: Callable[..., object],
    frame: object,
    name: str,
    arguments: tuple[object, ...],
    coordinates: dict[str, object],
) -> object:
    position = _begin_sql_invocation(frame, name)
    try:
        return invocation(*arguments, **coordinates)
    finally:
        _finish_sql_invocation(position)


class MeasuredCursor(sqlite3.Cursor):
    def execute(self, *arguments: object, **coordinates: object):
        return _invoke_sql(
            getattr(super(), "execute"),
            sys._getframe(1),
            "execute",
            arguments,
            coordinates,
        )

    def executemany(self, *arguments: object, **coordinates: object):
        return _invoke_sql(
            getattr(super(), "executemany"),
            sys._getframe(1),
            "executemany",
            arguments,
            coordinates,
        )

    def executescript(self, *arguments: object, **coordinates: object):
        return _invoke_sql(
            getattr(super(), "executescript"),
            sys._getframe(1),
            "executescript",
            arguments,
            coordinates,
        )


class MeasuredConnection(sqlite3.Connection):
    def cursor(self, *arguments: object, **coordinates: object):
        coordinates.setdefault("factory", MeasuredCursor)
        return super().cursor(*arguments, **coordinates)

    def execute(self, *arguments: object, **coordinates: object):
        return _invoke_sql(
            getattr(super(), "execute"),
            sys._getframe(1),
            "execute",
            arguments,
            coordinates,
        )

    def executemany(self, *arguments: object, **coordinates: object):
        return _invoke_sql(
            getattr(super(), "executemany"),
            sys._getframe(1),
            "executemany",
            arguments,
            coordinates,
        )

    def executescript(self, *arguments: object, **coordinates: object):
        return _invoke_sql(
            getattr(super(), "executescript"),
            sys._getframe(1),
            "executescript",
            arguments,
            coordinates,
        )

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
    pending = deque((compiled,))
    while pending:
        code = pending.popleft()
        for material in code.co_consts:
            if isinstance(material, CodeType):
                found.append(
                    _identity(path.resolve(), material.co_firstlineno, material.co_qualname)
                )
                pending.append(material)
    return tuple(found)


def implementation_function_identities() -> tuple[str, ...]:
    return tuple(
        identity
        for directory in SOURCE_DIRECTORIES
        for path in (ROOT / directory).rglob("*.py")
        for identity in _compiled_identities(path)
    )


def _sql_invocation_identity(
    path: Path,
    code: CodeType,
    instruction: dis.Instruction,
) -> str | None:
    positions = instruction.positions
    line = positions.lineno
    column = positions.col_offset
    if line is None or column is None:
        return None
    return f"{_identity(path, line, code.co_qualname)}:{column}:{instruction.argval}"


def _compiled_sql_invocation_identities(path: Path) -> tuple[str, ...]:
    try:
        compiled = compile(path.read_bytes(), str(path), "exec")
    except (OSError, SyntaxError, ValueError):
        return ()
    found = []
    pending = deque((compiled,))
    while pending:
        code = pending.popleft()
        for material in code.co_consts:
            if isinstance(material, CodeType):
                pending.append(material)
        for instruction in dis.get_instructions(code):
            if (
                instruction.opname in {"LOAD_METHOD", "LOAD_ATTR"}
                and instruction.argval in SQL_INVOCATION_NAMES
            ):
                identity = _sql_invocation_identity(path.resolve(), code, instruction)
                if identity is not None:
                    found.append(identity)
    return tuple(found)


def implementation_sql_invocation_identities() -> tuple[str, ...]:
    return tuple(
        identity
        for directory in SOURCE_DIRECTORIES
        for path in (ROOT / directory).rglob("*.py")
        for identity in _compiled_sql_invocation_identities(path)
    )


@lru_cache(maxsize=None)
def _code_sql_invocation_identities(
    code: CodeType, name: str
) -> tuple[tuple[int, str], ...]:
    if _source_identity(code) is None:
        return ()
    path = Path(code.co_filename).resolve()
    return tuple(
        (instruction.offset, identity)
        for instruction in dis.get_instructions(code)
        if instruction.opname in {"LOAD_METHOD", "LOAD_ATTR"}
        and instruction.argval == name
        and (identity := _sql_invocation_identity(path, code, instruction)) is not None
    )


def _frame_sql_invocation_identity(frame: object, name: str) -> str | None:
    return next(
        (
            identity
            for offset, identity in reversed(
                _code_sql_invocation_identities(frame.f_code, name)
            )
            if offset <= frame.f_lasti
        ),
        None,
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


def _sql_invocations_since(occurrence_position: int) -> dict[str, int]:
    found: dict[str, int] = {}
    for identity in _sql_invocation_occurrences[occurrence_position:]:
        if identity is not None:
            found[identity] = found.get(identity, 0) + 1
    return found


def _measurement(
    python_coordinates: dict[str, list[int]],
    sql_coordinates: dict[str, int],
    sql_invocation_coordinates: dict[str, int] | None = None,
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
    sql_invocations = {
        identity: {
            "occurrence_count": (
                _sql_invocations
                if sql_invocation_coordinates is None
                else sql_invocation_coordinates
            ).get(identity, 0)
        }
        for identity in implementation_sql_invocation_identities()
    }
    return {
        "python": python,
        "sql": dict(sql_coordinates.items()),
        "sql_invocations": sql_invocations,
        "reference_pair": reference_pair,
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
            for identity, coordinates in python_coordinates.items()
            if any(coordinates)
        },
        "sql": dict(sql_coordinates.items()),
    }


def measurement() -> dict[str, object]:
    found = _measurement(_python, _sql)
    found.update(
        {
            "sql_occurrences": tuple(_sql_occurrences),
            "sql_invocation_occurrences": tuple(_sql_invocation_occurrences),
            "sql_statement_invocations": tuple(_sql_statement_invocations),
            "pytest": tuple(_pytest_occurrences),
        }
    )
    return found


def _output_materials(
    found: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    python_identities = tuple(found["python"])
    python_positions = {
        identity: position for position, identity in enumerate(python_identities)
    }
    sql_material = tuple(found["sql"])
    sql_positions = {
        material: position for position, material in enumerate(sql_material)
    }
    sql_invocation_identities = tuple(found["sql_invocations"])
    sql_invocation_positions = {
        identity: position
        for position, identity in enumerate(sql_invocation_identities)
    }
    catalog = {
        "python": python_identities,
        "sql_invocations": sql_invocation_identities,
        "reference_pair": tuple(
            python_positions[identity] for identity in found["reference_pair"]
        ),
    }
    observation = {
        "python": tuple(
            {
                "implementation_function_position": python_positions[identity],
                **found["python"][identity],
            }
            for identity in python_identities
            if any(found["python"][identity].values())
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
        "sql_invocations": tuple(
            {
                "implementation_function_position": sql_invocation_positions[
                    identity
                ],
                **found["sql_invocations"][identity],
            }
            for identity in sql_invocation_identities
            if any(found["sql_invocations"][identity].values())
        ),
        "sql_invocation_occurrences": tuple(
            (
                None
                if identity is None
                else sql_invocation_positions[identity]
            )
            for identity in found["sql_invocation_occurrences"]
        ),
        "sql_statement_invocations": found["sql_statement_invocations"],
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
    return catalog, observation


def _json_material(found: dict[str, object]) -> bytes:
    represented = json.dumps(
        found,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return bytes(ord(unit) for unit in represented)


def begin() -> None:
    global _profiler
    if _profiler is not None:
        _profiler.disable()
        _enclosing_measurement_coordinates.append(
            (
                _profile_coordinates(_profiler),
                len(_sql_occurrences),
                len(_sql_invocation_occurrences),
            )
        )
        _profiler.enable()
        return
    _python.clear()
    _sql.clear()
    _sql_occurrences.clear()
    _sql_invocations.clear()
    _sql_invocation_occurrences.clear()
    _sql_statement_invocations.clear()
    _active_sql_invocations.positions = []
    _enclosing_measurement_coordinates.clear()
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
    if _enclosing_measurement_coordinates:
        prior_python, prior_sql_position, prior_sql_invocation_position = (
            _enclosing_measurement_coordinates.pop()
        )
        found = _measurement(
            _coordinate_difference(current_python, prior_python),
            _sql_since(prior_sql_position),
            _sql_invocations_since(prior_sql_invocation_position),
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
    if _profiler is None or not _enclosing_measurement_coordinates:
        raise RuntimeError("one enclosing implementation measurement is required")
    _profiler.disable()
    current_python = _profile_coordinates(_profiler)
    prior_python, prior_sql_position, _ = _enclosing_measurement_coordinates.pop()
    found = _observed_measurement(
        _coordinate_difference(current_python, prior_python),
        _sql_since(prior_sql_position),
    )
    _profiler.enable()
    return found


def pytest_sessionstart(session: object) -> None:
    del session
    begin()


def _fidelity_test_subjects() -> dict[str, dict[str, object]]:
    grammar = json.loads(
        (ROOT / "book_of_seed" / "grammar.json").read_text(encoding="utf-8")
    )
    fidelity = grammar["clause_coordinates"]["01.Source.C"]
    relation = fidelity["test_subject_relation"]
    if relation != {
        "first_subject": "test_subject",
        "relation": "witness_for",
        "second_subject": "this_Fidelity",
        "first_subject_distinct_from": "this_Witness",
    }:
        raise ValueError("exact Fidelity test-subject relation is required")
    test_subjects = fidelity["test_subjects"]
    if type(test_subjects) is not list or not test_subjects:
        raise TypeError("exact Fidelity test subjects are required")
    declared: dict[str, dict[str, object]] = {}
    for coordinates in test_subjects:
        if type(coordinates) is not dict:
            raise TypeError("exact Fidelity test subject coordinates are required")
        subject = coordinates.get("subject")
        if type(subject) is not str or not subject:
            raise TypeError("one exact Fidelity test subject is required")
        if subject in declared:
            raise ValueError("Fidelity test subject entered the grammar twice")
        for name, value in coordinates.items():
            if type(name) is not str:
                raise TypeError("exact Fidelity test subject coordinates are required")
            if name != "grammar_coordinate_reference":
                if type(value) is not str:
                    raise TypeError(
                        "exact Fidelity test subject coordinates are required"
                    )
                continue
            if (
                type(value) is not list
                or not value
                or any(
                    not (
                        (type(part) is str and part)
                        or (
                            type(part) is dict
                            and tuple(part) == (
                                "identity",
                                "first_subject",
                                "relation",
                                "second_subject",
                            )
                            and all(
                                type(coordinate) is str and coordinate
                                for coordinate in part.values()
                            )
                        )
                    )
                    for part in value
                )
            ):
                raise TypeError(
                    "one exact grammar coordinate reference is required"
                )
        declared[subject] = {
            **coordinates,
            "witness_for": relation["second_subject"],
            "distinct_from": relation["first_subject_distinct_from"],
        }

    admission = book_admission()
    for subject in declared:
        subject_words = tuple(
            word.lower() for word in re.findall(r"[A-Za-z]+", subject)
        )
        if not subject_words or any(word not in admission for word in subject_words):
            raise ValueError("test subject carries words absent from Book admission")
    return declared


def _pytest_subject(
    module: object,
    function_under_test: object,
    declared: dict[str, dict[str, object]],
) -> dict[str, object] | None:
    uniform = getattr(module, "FIDELITY_SUBJECT", None)
    families = getattr(module, "FIDELITY_SUBJECTS", None)
    witnesses = getattr(module, "WITNESSES", ())
    if type(witnesses) is not tuple:
        raise TypeError("exact Witness functions are required")
    if any(not callable(function) for function in witnesses):
        raise TypeError("exact Witness functions are required")
    if len(set(witnesses)) != len(witnesses):
        raise ValueError("test function entered Witnesses twice")
    is_witness = function_under_test in witnesses
    if uniform is not None and families is not None:
        raise ValueError("test module carries two Fidelity subject boundaries")
    if uniform is not None and witnesses:
        raise ValueError("uniform Fidelity subject crossed Witnesses")
    if uniform is not None:
        if type(uniform) is not str:
            raise TypeError("one exact test subject reference is required")
        subject = uniform
    else:
        if families is None:
            raise ValueError("one exact test subject is required")
        if type(families) is not dict:
            raise TypeError("exact Fidelity subject families are required")
        if not families:
            raise ValueError("one exact test subject is required")
        matches: list[str] = []
        entered_functions: set[object] = set()
        for family_subject, functions in families.items():
            if type(family_subject) is not str or type(functions) is not tuple:
                raise TypeError("exact Fidelity subject families are required")
            for function in functions:
                if not callable(function):
                    raise TypeError("exact Fidelity subject functions are required")
                if function in entered_functions:
                    raise ValueError("test function entered Fidelity subjects twice")
                entered_functions.add(function)
                if function is function_under_test:
                    matches.append(family_subject)
        if is_witness:
            if matches:
                raise ValueError("test function crossed Fidelity and Witnesses")
            return None
        if len(matches) != 1:
            raise ValueError("one exact test subject is required")
        subject = matches[0]
    try:
        return declared[subject]
    except KeyError as error:
        raise ValueError("test subject is absent from witness grammar") from error


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(
    session: object, config: object, items: list[object]
) -> None:
    del session, config
    declared = _fidelity_test_subjects()
    resolved = tuple(
        _pytest_subject(item.module, item.function, declared) for item in items
    )
    for item, coordinates in zip(items, resolved):
        item.stash[_PYTEST_SUBJECT_COORDINATES] = coordinates


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_protocol(item: object, nextitem: object):
    del nextitem
    subject_coordinates = item.stash[_PYTEST_SUBJECT_COORDINATES]
    if subject_coordinates is None:
        yield
        return
    occurrence_position = len(_pytest_occurrences)
    begin()
    (
        _,
        sql_occurrence_position,
        sql_invocation_occurrence_position,
    ) = _enclosing_measurement_coordinates[-1]
    try:
        yield
    finally:
        found = _finish_observed()
    found.pop("sql")
    _pytest_occurrences.append(
        {
            "occurrence_position": occurrence_position,
            "pytest_identity": item.nodeid,
            **subject_coordinates,
            "first_sql_occurrence_position": sql_occurrence_position,
            "sql_occurrence_count": len(_sql_occurrences) - sql_occurrence_position,
            "first_sql_invocation_occurrence_position": (
                sql_invocation_occurrence_position
            ),
            "sql_invocation_occurrence_count": (
                len(_sql_invocation_occurrences)
                - sql_invocation_occurrence_position
            ),
            **found,
        }
    )


def pytest_sessionfinish(session: object, exitstatus: int) -> None:
    del session, exitstatus
    found = finish()
    output = os.environ.get(OUTPUT_ENVIRONMENT_COORDINATE)
    catalog_output = os.environ.get(CATALOG_OUTPUT_ENVIRONMENT_COORDINATE)
    if output and catalog_output:
        catalog, observation = _output_materials(found)
        Path(catalog_output).write_bytes(_json_material(catalog))
        Path(output).write_bytes(_json_material(observation))
