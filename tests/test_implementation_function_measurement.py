from __future__ import annotations

import ast
from pathlib import Path
import sqlite3
import sys
from types import CodeType, SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import implementation_function_measurement as measured  # noqa: E402
from reference_pair_comparison import ReferencePairComparison  # noqa: E402


def test_compiled_code_supplies_exact_identities(tmp_path):
    source = tmp_path / "fixture.py"
    source.write_bytes(b"def a():\n    return 1\n\ndef b():\n    return 2\n")

    identities = measured._compiled_identities(source)

    assert tuple(tuple(identity.rsplit(":", 2)[1:]) for identity in identities) == (
        ("1", "a"),
        ("4", "b"),
    )


def test_observed_measurement_preserves_observation_order_without_sorting():
    observed = measured._observed_measurement(
        {
            "implementation-z": [1, 2, 3],
            "implementation-a": [4, 5, 6],
        },
        {"SELECT z": 1, "SELECT a": 2},
    )

    assert tuple(observed["python"]) == ("implementation-z", "implementation-a")
    assert tuple(observed["sql"]) == ("SELECT z", "SELECT a")


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
        if identity.startswith("scripts/implementation_function_measurement.py:")
        and identity.endswith(":_identity")
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
        connection = sqlite3.connect(":memory:")
        connection.execute("SELECT 1").fetchone()
        measured._identity(ROOT, 1, "before")
        measured.begin()
        try:
            connection.execute("SELECT 2").fetchone()
            measured._identity(ROOT, 2, "inside")
        finally:
            inside = measured.finish()
        connection.execute("SELECT 3").fetchone()
        measured._identity(ROOT, 3, "after")
    finally:
        complete = measured.finish()

    identity = next(
        identity
        for identity in complete["python"]
        if identity.startswith("scripts/implementation_function_measurement.py:")
        and identity.endswith(":_identity")
    )
    assert inside["python"][identity]["occurrence_count"] == 1
    assert complete["python"][identity]["occurrence_count"] == 3
    assert inside["sql"] == {"SELECT 2": 1}
    assert complete["sql"] == {"SELECT 1": 1, "SELECT 2": 1, "SELECT 3": 1}


def test_one_pytest_occurrence_keeps_its_exact_witness_measurement():
    def exact_function():
        pass

    item = SimpleNamespace(
        nodeid="tests/exact.py::test_one_occurrence",
        stash={},
        module=SimpleNamespace(
            FIDELITY_SUBJECT="this_book_material_acquisition_witness"
        ),
        function=exact_function,
    )
    measured.begin()
    measured.pytest_collection_modifyitems(None, None, [item])
    protocol = measured.pytest_runtest_protocol(item, None)
    try:
        next(protocol)
        measured._identity(ROOT, 7, "inside-pytest-occurrence")
        connection = sqlite3.connect(":memory:")
        connection.execute("SELECT 9").fetchone()
        with pytest.raises(StopIteration):
            next(protocol)
    finally:
        result = measured.finish()

    assert len(result["pytest"]) == 1
    occurrence = result["pytest"][0]
    assert occurrence["occurrence_position"] == 0
    assert occurrence["pytest_identity"] == item.nodeid
    assert occurrence["subject"] == "this_book_material_acquisition_witness"
    assert occurrence["witness_for"] == "this_Fidelity"
    assert occurrence["first_sql_occurrence_position"] == 0
    assert occurrence["sql_occurrence_count"] == 1
    assert result["sql_occurrences"] == ("SELECT 9",)
    identity = next(
        identity
        for identity in occurrence["python"]
        if identity.endswith(":_identity")
    )
    assert occurrence["python"][identity]["occurrence_count"] == 1

    catalog, observation = measured._output_materials(result)
    assert observation["sql"] == (
        {"exact_material": "SELECT 9", "occurrence_count": 1},
    )
    assert observation["sql_occurrences"] == (0,)
    assert observation["sql_invocation_occurrences"] == (None,)
    assert observation["sql_statement_invocations"] == (0,)
    output_occurrence = observation["pytest"][0]
    output_coordinate = next(
        coordinate
        for coordinate in output_occurrence["python"]
        if catalog["python"][
            coordinate["implementation_function_position"]
        ].endswith(":_identity")
    )
    assert output_coordinate["occurrence_count"] == 1
    assert all(unit < 128 for unit in measured._json_material(catalog))
    assert all(unit < 128 for unit in measured._json_material(observation))


def test_pytest_subject_refuses_missing_crossed_or_unadmitted_families():
    def first():
        pass

    def second():
        pass

    empty = SimpleNamespace()
    uniform = SimpleNamespace(
        FIDELITY_SUBJECT="this_book_material_acquisition_witness"
    )
    crossed = SimpleNamespace(
        FIDELITY_SUBJECT="this_book_material_acquisition_witness",
        FIDELITY_SUBJECTS={"this_book_material_acquisition_witness": (first,)},
    )
    repeated = SimpleNamespace(
        FIDELITY_SUBJECTS={
            "this_book_material_acquisition_witness": (first,),
            "another_subject": (first, second),
        }
    )
    uncurated = SimpleNamespace(FIDELITY_SUBJECT="uncurated_subject_word")
    list_family = SimpleNamespace(
        FIDELITY_SUBJECTS=[("this_book_material_acquisition_witness", (first,))]
    )
    functions_list = SimpleNamespace(
        FIDELITY_SUBJECTS={"this_book_material_acquisition_witness": [first]}
    )
    nonfunction_family = SimpleNamespace(
        FIDELITY_SUBJECTS={"this_book_material_acquisition_witness": ("first",)}
    )

    fidelity_subject_coordinates = measured._fidelity_test_subjects()
    with pytest.raises(ValueError, match="one exact test subject"):
        measured._pytest_subject(empty, first, fidelity_subject_coordinates)
    assert (
        measured._pytest_subject(uniform, first, fidelity_subject_coordinates)
        == {
            "subject": "this_book_material_acquisition_witness",
            "material_reference": "this_Book",
            "witness_for": "this_Fidelity",
            "distinct_from": "this_Witness",
        }
    )
    with pytest.raises(ValueError, match="two Fidelity subject boundaries"):
        measured._pytest_subject(crossed, first, fidelity_subject_coordinates)
    with pytest.raises(ValueError, match="entered Fidelity subjects twice"):
        measured._pytest_subject(repeated, first, fidelity_subject_coordinates)
    with pytest.raises(ValueError, match="absent from witness grammar"):
        measured._pytest_subject(uncurated, first, fidelity_subject_coordinates)
    with pytest.raises(TypeError, match="exact Fidelity subject families"):
        measured._pytest_subject(list_family, first, fidelity_subject_coordinates)
    with pytest.raises(TypeError, match="exact Fidelity subject families"):
        measured._pytest_subject(functions_list, first, fidelity_subject_coordinates)
    with pytest.raises(TypeError, match="exact Fidelity subject functions"):
        measured._pytest_subject(nonfunction_family, first, fidelity_subject_coordinates)


def test_pytest_subject_collection_is_complete_before_any_test_occurrence():
    def item(subject):
        return SimpleNamespace(
            module=SimpleNamespace(FIDELITY_SUBJECT=subject),
            function=(
                test_pytest_subject_collection_is_complete_before_any_test_occurrence
            ),
            stash={},
        )

    valid = item("this_book_material_acquisition_witness")
    invalid = item("uncurated_subject_word")

    with pytest.raises(ValueError, match="absent from witness grammar"):
        measured.pytest_collection_modifyitems(None, None, [valid, invalid])

    assert valid.stash == invalid.stash == {}


def test_stable_catalog_is_separate_from_sparse_observation():
    measured.begin()
    try:
        measured._identity(ROOT, 7, "one-observed-function")
    finally:
        result = measured.finish()

    catalog, observation = measured._output_materials(result)

    assert len(catalog["python"]) > len(observation["python"])
    assert all(type(identity) is str for identity in catalog["python"])
    assert all("identity" not in coordinate for coordinate in observation["python"])
    assert all(
        coordinate["implementation_function_position"] < len(catalog["python"])
        for coordinate in observation["python"]
    )


def test_reference_pair_measurement_contains_each_preserved_function():
    result = measured.measurement()

    names = {identity.rsplit(":", 1)[-1] for identity in result["reference_pair"]}
    witness_method_names = set()
    for method in (
        ReferencePairComparison.references_from,
        ReferencePairComparison.references_to,
    ):
        pending = [method.__code__]
        while pending:
            code = pending.pop()
            witness_method_names.add(code.co_qualname)
            pending.extend(
                constant
                for constant in code.co_consts
                if isinstance(constant, CodeType)
            )

    assert names == witness_method_names | {
        "ReferencePairComparison",
        "ReferencePairComparison.__init__",
        "ReferencePairComparison.load",
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


def test_compiled_sql_invocation_locations_keep_observed_and_unobserved_counts():
    measured.begin()
    try:
        ReferencePairComparison()
    finally:
        result = measured.finish()

    observed = {
        identity
        for identity, coordinates in result["sql_invocations"].items()
        if coordinates["occurrence_count"] > 0
    }
    assert observed == {
        "scripts/reference_pair_comparison.py:13:"
        "ReferencePairComparison.__init__:8:executescript"
    }
    assert any(
        identity.endswith("ReferencePairComparison.load:12:execute")
        and coordinates["occurrence_count"] == 0
        for identity, coordinates in result["sql_invocations"].items()
    )
    assert result["sql_invocation_occurrences"] == tuple(observed)
    assert result["sql_statement_invocations"] == (0, 0, 0, 0, 0)


def test_fidelity_witness_subjects_cover_each_test_function_exactly_once():
    subjects: set[str] = set()
    for path in (ROOT / "tests").glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        test_functions = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        }
        constants = {
            target.id: node.value.value
            for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and type(node.value.value) is str
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        uniform = []
        families = []
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            assigned = {
                target.id
                for target in node.targets
                if isinstance(target, ast.Name)
            }
            if "FIDELITY_SUBJECT" in assigned:
                uniform.append(node.value)
            if "FIDELITY_SUBJECTS" in assigned:
                families.append(node.value)

        assert len(uniform) + len(families) == 1, path
        if uniform:
            value = uniform[0]
            subject = (
                value.value
                if isinstance(value, ast.Constant)
                else constants[value.id]
            )
            assert type(subject) is str and subject
            subjects.add(subject)
            continue

        family = families[0]
        assert isinstance(family, ast.Dict) and family.keys
        entered: list[str] = []
        for key, value in zip(family.keys, family.values):
            assert isinstance(key, ast.Constant) and type(key.value) is str
            assert isinstance(value, ast.Tuple)
            subjects.add(key.value)
            entered.extend(
                element.id for element in value.elts if isinstance(element, ast.Name)
            )
        assert set(entered) == test_functions, path
        assert len(entered) == len(test_functions), path

    fidelity_subject_coordinates = measured._fidelity_test_subjects()
    assert set(fidelity_subject_coordinates) == subjects
    assert next(iter(fidelity_subject_coordinates)).lower().count("standing") == 1
    assert tuple(fidelity_subject_coordinates)[-1] == "fidelity_witness_subject_completeness"


FIDELITY_SUBJECTS = {
    "measurement_occurrence_order": (
        test_observed_measurement_preserves_observation_order_without_sorting,
    ),
    "measurement_occurrence_boundary": (
        test_one_measurement_does_not_replace_an_active_measurement,
    ),
    "compiled_function_reference": (
        test_compiled_code_supplies_exact_identities,
        test_uninvoked_compiled_identity_remains_unobserved,
    ),
    "function_invocation_occurrence": (
        test_python_invocation_occurrence_is_measured,
    ),
    "function_reference_measurement_distinction": (
        test_stable_catalog_is_separate_from_sparse_observation,
    ),
    "reference_pair_measurement": (
        test_reference_pair_measurement_contains_each_preserved_function,
    ),
    "exact_supplied_material_occurrence": (
        test_sql_occurrence_preserves_exact_statement_material,
    ),
    "supplied_function_invocation": (
        test_existing_sql_trace_callback_receives_the_same_statement,
    ),
    "compiled_function_invocation_witness": (
        test_compiled_sql_invocation_locations_keep_observed_and_unobserved_counts,
    ),
    "fidelity_witness_occurrence": (
        test_one_pytest_occurrence_keeps_its_exact_witness_measurement,
    ),
    "fidelity_witness_subject": (
        test_pytest_subject_refuses_missing_crossed_or_unadmitted_families,
    ),
    "fidelity_witness_collection_boundary": (
        test_pytest_subject_collection_is_complete_before_any_test_occurrence,
    ),
    "fidelity_witness_subject_completeness": (
        test_fidelity_witness_subjects_cover_each_test_function_exactly_once,
    ),
}
