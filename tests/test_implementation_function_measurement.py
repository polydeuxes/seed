from __future__ import annotations

from pathlib import Path
import sqlite3
import subprocess
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


def test_one_pytest_occurrence_keeps_its_exact_fidelity_distinction():
    def exact_function():
        pass

    item = SimpleNamespace(
        nodeid="tests/exact.py::test_one_occurrence",
        stash={},
        module=SimpleNamespace(
            PYTEST_ADMISSION=(exact_function,),
            FIDELITY_DISTINCTIONS={
                ("book_coordinates", "01.Source.C"): (exact_function,)
            }
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
    assert occurrence["fidelity_distinction_reference"] == [
        "book_coordinates",
        "01.Source.C",
    ]
    assert "test_subject" not in occurrence
    assert "witness_for" not in occurrence
    assert "distinct_from" not in occurrence
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


def test_pytest_distinction_refuses_duplicate_or_invalid_references():
    def first():
        pass

    def second():
        pass

    grammar = measured._witness_grammar()
    no_admission = SimpleNamespace()
    ordinary = SimpleNamespace(PYTEST_ADMISSION=(second,))
    exact = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): (first,)
        }
    )
    repeated = SimpleNamespace(
        PYTEST_ADMISSION=(first, second),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): (first,),
            ("book_coordinates", "02.Acts.A"): (first, second),
        }
    )
    missing = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "missing"): (first,)
        }
    )
    scalar = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={"01.Source.C": (first,)},
    )
    list_distinctions = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS=[
            (("book_coordinates", "01.Source.C"), (first,))
        ]
    )
    functions_list = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): [first]
        }
    )
    nonfunction_distinction = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): ("first",)
        }
    )
    explicit_witness_material = SimpleNamespace(
        PYTEST_ADMISSION=(second,),
        WITNESS_MATERIAL_TESTS=(second,)
    )
    unreferenced = SimpleNamespace(
        PYTEST_ADMISSION=(first, second),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): (first,)
        }
    )
    crossed = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): (first,)
        },
        WITNESS_MATERIAL_TESTS=(first,),
    )
    repeated_witness_material = SimpleNamespace(
        PYTEST_ADMISSION=(second,),
        WITNESS_MATERIAL_TESTS=(second, second)
    )
    malformed_witness_material = SimpleNamespace(
        PYTEST_ADMISSION=(second,),
        WITNESS_MATERIAL_TESTS=[second]
    )
    repeated_admission = SimpleNamespace(PYTEST_ADMISSION=(first, first))
    malformed_admission = SimpleNamespace(PYTEST_ADMISSION=[first])
    fidelity_without_admission = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        FIDELITY_DISTINCTIONS={
            ("book_coordinates", "01.Source.C"): (second,)
        },
    )
    witness_without_admission = SimpleNamespace(
        PYTEST_ADMISSION=(first,),
        WITNESS_MATERIAL_TESTS=(second,),
    )

    with pytest.raises(TypeError, match="exact pytest admission functions"):
        measured._pytest_uptake(no_admission, first, grammar)
    assert measured._pytest_uptake(ordinary, second, grammar) is (
        measured._NO_PYTEST_UPTAKE
    )
    assert measured._pytest_uptake(exact, first, grammar) == {
        "fidelity_distinction_reference": [
            "book_coordinates",
            "01.Source.C",
        ]
    }
    with pytest.raises(ValueError, match="entered Fidelity distinctions twice"):
        measured._pytest_uptake(repeated, first, grammar)
    with pytest.raises(ValueError, match="absent from current book coordinates"):
        measured._pytest_uptake(missing, first, grammar)
    with pytest.raises(TypeError, match="exact Fidelity distinction reference"):
        measured._pytest_uptake(scalar, first, grammar)
    with pytest.raises(TypeError, match="exact Fidelity distinctions"):
        measured._pytest_uptake(list_distinctions, first, grammar)
    with pytest.raises(TypeError, match="exact Fidelity distinctions"):
        measured._pytest_uptake(functions_list, first, grammar)
    with pytest.raises(TypeError, match="exact Fidelity distinction functions"):
        measured._pytest_uptake(nonfunction_distinction, first, grammar)
    assert measured._pytest_uptake(
        explicit_witness_material, second, grammar
    ) is measured._WITNESS_MATERIAL_UPTAKE
    assert measured._pytest_uptake(unreferenced, second, grammar) is (
        measured._NO_PYTEST_UPTAKE
    )
    with pytest.raises(ValueError, match="crossed Fidelity and Witness Material"):
        measured._pytest_uptake(crossed, first, grammar)
    with pytest.raises(ValueError, match="Witness Material tests twice"):
        measured._pytest_uptake(repeated_witness_material, second, grammar)
    with pytest.raises(TypeError, match="exact Witness Material test functions"):
        measured._pytest_uptake(malformed_witness_material, second, grammar)
    with pytest.raises(ValueError, match="entered admission twice"):
        measured._pytest_uptake(repeated_admission, first, grammar)
    with pytest.raises(TypeError, match="exact pytest admission functions"):
        measured._pytest_uptake(malformed_admission, first, grammar)
    with pytest.raises(ValueError, match="Fidelity uptake requires pytest admission"):
        measured._pytest_uptake(fidelity_without_admission, first, grammar)
    with pytest.raises(
        ValueError, match="Witness Material uptake requires pytest admission"
    ):
        measured._pytest_uptake(witness_without_admission, first, grammar)


def test_pytest_distinction_collection_refuses_a_stale_reference_before_occurrence():
    def item(reference):
        function = (
            test_pytest_distinction_collection_refuses_a_stale_reference_before_occurrence
        )
        return SimpleNamespace(
            module=SimpleNamespace(
                PYTEST_ADMISSION=(function,),
                FIDELITY_DISTINCTIONS={reference: (function,)},
            ),
            function=function,
            stash={},
        )

    valid = item(("book_coordinates", "01.Source.C"))
    invalid = item(("book_coordinates", "missing"))

    with pytest.raises(ValueError, match="absent from current book coordinates"):
        measured.pytest_collection_modifyitems(None, None, [valid, invalid])

    assert valid.stash == invalid.stash == {}


def test_pytest_distinction_collection_refuses_an_ownerless_function():
    function = test_pytest_distinction_collection_refuses_an_ownerless_function
    another_function = lambda: None
    first = SimpleNamespace(
        nodeid=(
            "tests/test_implementation_function_measurement.py::"
            "test_pytest_distinction_collection_refuses_an_ownerless_function"
        ),
        module=SimpleNamespace(
            __name__="tests.test_implementation_function_measurement",
            PYTEST_ADMISSION=(another_function,),
        ),
        function=function,
        stash={},
    )
    second = SimpleNamespace(
        nodeid="tests/another.py::test_another_ownerless_function",
        module=SimpleNamespace(
            __name__="tests.another",
            PYTEST_ADMISSION=(another_function,),
        ),
        function=lambda: None,
        stash={},
    )

    with pytest.raises(ValueError, match="no exact admission") as refusal:
        measured.pytest_collection_modifyitems(None, None, [first, second])

    assert first.nodeid in str(refusal.value)
    assert second.nodeid in str(refusal.value)
    assert first.stash == second.stash == {}


def test_admitted_implementation_test_has_no_seed_uptake():
    function = test_admitted_implementation_test_has_no_seed_uptake
    item = SimpleNamespace(
        nodeid="tests/implementation.py::test_admitted_implementation",
        module=SimpleNamespace(PYTEST_ADMISSION=(function,)),
        function=function,
        stash={},
    )

    measured.pytest_collection_modifyitems(None, None, [item])
    assert item.stash[measured._PYTEST_UPTAKE] is measured._NO_PYTEST_UPTAKE

    measured.begin()
    try:
        fidelity_occurrence_count = len(measured._pytest_occurrences)
        material_occurrence_count = len(measured._witness_material_occurrences)
        protocol = measured.pytest_runtest_protocol(item, None)
        next(protocol)
        measured._identity(ROOT, 8, "inside-admitted-implementation-test")
        with pytest.raises(StopIteration):
            next(protocol)
    finally:
        measured.finish()

    assert len(measured._pytest_occurrences) == fidelity_occurrence_count
    assert len(measured._witness_material_occurrences) == material_occurrence_count


def test_witness_material_occurrence_has_no_fidelity_uptake():
    function = test_witness_material_occurrence_has_no_fidelity_uptake
    item = SimpleNamespace(
        nodeid="tests/material.py::test_one_witness_material_occurrence",
        module=SimpleNamespace(
            PYTEST_ADMISSION=(
                function,
                test_pytest_distinction_collection_refuses_a_stale_reference_before_occurrence,
            ),
            FIDELITY_DISTINCTIONS={
                ("book_coordinates", "01.Source.C"): (
                    test_pytest_distinction_collection_refuses_a_stale_reference_before_occurrence,
                ),
            },
            WITNESS_MATERIAL_TESTS=(function,),
        ),
        function=function,
        stash={},
    )
    measured.pytest_collection_modifyitems(None, None, [item])
    assert item.stash[measured._PYTEST_UPTAKE] is (
        measured._WITNESS_MATERIAL_UPTAKE
    )

    measured.begin()
    try:
        fidelity_occurrence_count = len(measured._pytest_occurrences)
        material_occurrence_count = len(measured._witness_material_occurrences)
        protocol = measured.pytest_runtest_protocol(item, None)
        next(protocol)
        measured._identity(ROOT, 9, "inside-witness-material-occurrence")
        with pytest.raises(StopIteration):
            next(protocol)
    finally:
        result = measured.finish()

    assert len(measured._pytest_occurrences) == fidelity_occurrence_count
    assert len(measured._witness_material_occurrences) == (
        material_occurrence_count + 1
    )
    occurrence = result["witness_material"][-1]
    assert occurrence["pytest_identity"] == item.nodeid
    assert not {
        "fidelity_distinction_reference",
        "test_subject",
        "witness_for",
        "distinct_from",
    } & set(occurrence)
    identity = next(
        identity
        for identity in occurrence["python"]
        if identity.endswith(":_identity")
    )
    assert occurrence["python"][identity]["occurrence_count"] == 1

    catalog, observation = measured._output_materials(result)
    output_occurrence = observation["witness_material"][-1]
    assert output_occurrence["pytest_identity"] == item.nodeid
    assert not {
        "fidelity_distinction_reference",
        "test_subject",
        "witness_for",
        "distinct_from",
    } & set(output_occurrence)
    output_coordinate = next(
        coordinate
        for coordinate in output_occurrence["python"]
        if catalog["python"][
            coordinate["implementation_function_position"]
        ].endswith(":_identity")
    )
    assert output_coordinate["occurrence_count"] == 1


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


def test_fidelity_distinctions_resolve_current_book_coordinates():
    grammar = measured._witness_grammar()
    assert measured._fidelity_distinction_coordinates(
        grammar,
        ("book_coordinates", "01.Source.C", "subjects", 2),
    ) == {
        "fidelity_distinction_reference": [
            "book_coordinates",
            "01.Source.C",
            "subjects",
            2,
        ],
    }
    entered: list[object] = []
    for reference, functions in FIDELITY_DISTINCTIONS.items():
        assert measured._fidelity_distinction_coordinates(grammar, reference) == {
            "fidelity_distinction_reference": list(reference)
        }
        entered.extend(functions)

    assert set(entered) == set(PYTEST_ADMISSION)
    assert len(entered) == len(PYTEST_ADMISSION)


def test_complete_pytest_admission_collects_without_implicit_uptake():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--collect-only",
            "-p",
            "scripts.implementation_function_measurement",
            "--",
        ],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr


PYTEST_ADMISSION = (
    test_compiled_code_supplies_exact_identities,
    test_observed_measurement_preserves_observation_order_without_sorting,
    test_python_invocation_occurrence_is_measured,
    test_uninvoked_compiled_identity_remains_unobserved,
    test_one_measurement_does_not_replace_an_active_measurement,
    test_one_pytest_occurrence_keeps_its_exact_fidelity_distinction,
    test_pytest_distinction_refuses_duplicate_or_invalid_references,
    test_pytest_distinction_collection_refuses_a_stale_reference_before_occurrence,
    test_pytest_distinction_collection_refuses_an_ownerless_function,
    test_admitted_implementation_test_has_no_seed_uptake,
    test_witness_material_occurrence_has_no_fidelity_uptake,
    test_stable_catalog_is_separate_from_sparse_observation,
    test_reference_pair_measurement_contains_each_preserved_function,
    test_sql_occurrence_preserves_exact_statement_material,
    test_existing_sql_trace_callback_receives_the_same_statement,
    test_compiled_sql_invocation_locations_keep_observed_and_unobserved_counts,
    test_fidelity_distinctions_resolve_current_book_coordinates,
    test_complete_pytest_admission_collects_without_implicit_uptake,
)


FIDELITY_DISTINCTIONS = {
    ("book_coordinates", "01.Source.C"): (
        test_compiled_code_supplies_exact_identities,
        test_observed_measurement_preserves_observation_order_without_sorting,
        test_python_invocation_occurrence_is_measured,
        test_uninvoked_compiled_identity_remains_unobserved,
        test_one_measurement_does_not_replace_an_active_measurement,
        test_one_pytest_occurrence_keeps_its_exact_fidelity_distinction,
        test_pytest_distinction_refuses_duplicate_or_invalid_references,
        test_pytest_distinction_collection_refuses_a_stale_reference_before_occurrence,
        test_pytest_distinction_collection_refuses_an_ownerless_function,
        test_admitted_implementation_test_has_no_seed_uptake,
        test_witness_material_occurrence_has_no_fidelity_uptake,
        test_stable_catalog_is_separate_from_sparse_observation,
        test_reference_pair_measurement_contains_each_preserved_function,
        test_sql_occurrence_preserves_exact_statement_material,
        test_existing_sql_trace_callback_receives_the_same_statement,
        test_compiled_sql_invocation_locations_keep_observed_and_unobserved_counts,
        test_fidelity_distinctions_resolve_current_book_coordinates,
        test_complete_pytest_admission_collects_without_implicit_uptake,
    )
}
