from __future__ import annotations

from pathlib import Path
import sqlite3
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import implementation_function_measurement as measured  # noqa: E402


def test_compiled_code_supplies_identities_without_ast_taxonomy(tmp_path):
    source = tmp_path / "fixture.py"
    source.write_bytes(b"def a():\n    return 1\n\ndef b():\n    return 2\n")

    identities = measured._compiled_identities(source)

    assert len(identities) == 2
    assert any(identity.endswith(":1:a") for identity in identities)
    assert any(identity.endswith(":4:b") for identity in identities)


def test_python_invocation_occurrence_is_measured():
    measured.begin()
    try:
        assert (
            measured._identity(ROOT / "seed_runtime" / "events.py", 1, "fixture")
            == "seed_runtime/events.py:1:fixture"
        )
    finally:
        result = measured.finish()

    identity, coordinates = next(
        (identity, coordinates)
        for identity, coordinates in result["python"].items()
        if identity.endswith(":_identity")
    )
    assert identity.startswith("scripts/implementation_function_measurement.py:")
    assert coordinates["occurrence_count"] == 1
    assert coordinates["elapsed_nanoseconds"] > 0
    assert coordinates["self_elapsed_nanoseconds"] > 0


def test_uninvoked_compiled_identity_remains_unobserved():
    measured.begin()
    result = measured.finish()

    identity, coordinates = next(
        (identity, coordinates)
        for identity, coordinates in result["python"].items()
        if identity.endswith(":pytest_sessionstart")
    )
    assert identity
    assert coordinates == {
        "occurrence_count": 0,
        "elapsed_nanoseconds": 0,
        "self_elapsed_nanoseconds": 0,
    }


def test_one_measurement_does_not_replace_an_active_measurement():
    measured.begin()
    try:
        measured._identity(ROOT, 1, "before")
        measured.begin()
        try:
            measured._identity(ROOT, 2, "inside")
        finally:
            inside = measured.finish()
        measured._identity(ROOT, 3, "after")
    finally:
        complete = measured.finish()

    identity = next(
        identity for identity in complete["python"] if identity.endswith(":_identity")
    )
    assert inside["python"][identity]["occurrence_count"] == 1
    assert complete["python"][identity]["occurrence_count"] == 3


def test_reference_pair_measurement_contains_each_surviving_function():
    result = measured.measurement()

    names = {identity.rsplit(":", 1)[-1] for identity in result["reference_pair"]}
    assert names == {
        "ReferencePairComparison",
        "ReferencePairComparison.__init__",
        "ReferencePairComparison.load",
        "ReferencePairComparison.references_from",
        "ReferencePairComparison.references_from.<locals>.<listcomp>",
        "ReferencePairComparison.references_to",
        "ReferencePairComparison.references_to.<locals>.<listcomp>",
        "_references",
    }


def test_sql_occurrence_preserves_exact_statement_material():
    measured.begin()
    try:
        connection = sqlite3.connect(":memory:")
        connection.execute("CREATE TABLE exact_material (value INTEGER)")
        connection.execute("INSERT INTO exact_material VALUES (?)", (7,))
        assert connection.execute("SELECT value FROM exact_material").fetchone()[0] == 7
    finally:
        result = measured.finish()

    assert result["sql"]["CREATE TABLE exact_material (value INTEGER)"] == 1
    assert result["sql"]["INSERT INTO exact_material VALUES (7)"] == 1
    assert result["sql"]["SELECT value FROM exact_material"] == 1


def test_existing_sql_trace_callback_receives_the_same_statement():
    carried = []
    measured.begin()
    try:
        connection = sqlite3.connect(":memory:")
        connection.set_trace_callback(carried.append)
        connection.execute("SELECT 1").fetchone()
    finally:
        result = measured.finish()

    assert carried == ["SELECT 1"]
    assert result["sql"]["SELECT 1"] == 1
