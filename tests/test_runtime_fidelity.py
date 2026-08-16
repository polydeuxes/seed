"""Reverse Fidelity sirens from the live witness back to machine grammar.

These tests are deliberately bounded by what the runtime declares. They do
not ask a hand-maintained list which witnesses should be inspected.
Red means the witness contains constitutional material the machine
grammar and its deterministic witnesses do not yet account for.
"""

from __future__ import annotations

import ast
from dataclasses import fields
from io import BytesIO, StringIO
import inspect
import json
from pathlib import Path
import re

import pytest

from seed_runtime.events import EventLedger
from seed_runtime.operator_checkpoint import (
    record_standing_boundary_reference_responsibility_assignment,
)
from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.operator_console import run_persistent_operator_console
from tests.test_book_admission import (
    book_admission,
    machine_grammar_words,
    scan_active_line,
)


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "seed_runtime"
GRAMMAR = ROOT / "book_of_seed" / "grammar.json"


def _runtime_trees():
    for path in sorted(RUNTIME.glob("*.py")):
        yield path, ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _runtime_imports(tree: ast.Module) -> set[str]:
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "seed_runtime":
                imported.update(name.name.split(".", 1)[0] for name in node.names)
            elif node.module.startswith("seed_runtime."):
                imported.add(node.module.split(".", 2)[1])
        elif isinstance(node, ast.Import):
            for name in node.names:
                if name.name.startswith("seed_runtime."):
                    imported.add(name.name.split(".", 2)[1])
    return imported


@pytest.mark.subject("live_seed_function_path")
def test_each_runtime_module_participates_in_live_process_imports():
    imports = {
        path.stem: _runtime_imports(tree)
        for path, tree in _runtime_trees()
    }
    participating = {"process_entry"}
    pending = ["process_entry"]
    while pending:
        module = pending.pop()
        for imported in imports.get(module, ()):
            if imported in imports and imported not in participating:
                participating.add(imported)
                pending.append(imported)

    active_modules = set(imports) - {"__init__"}
    assert active_modules == participating, (
        "\nRuntime modules outside the live process import graph:\n  "
        + "\n  ".join(sorted(active_modules - participating))
    )


def _module_strings(tree: ast.Module) -> dict[str, str]:
    declared = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
            continue
        if not isinstance(node.value.value, str):
            continue
        for name in node.targets:
            if isinstance(name, ast.Name):
                declared[name.id] = node.value.value
    return declared


def _module_functions(tree: ast.Module):
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _runtime_event_kinds() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path, line, name, value, _keys in _event_materials():
        found.setdefault(value, []).append(f"{path.name}:{line}:{name}")
    return found


def _runtime_event_kind_responsibilities() -> dict[str, list[tuple[str, str]]]:
    found: dict[str, list[tuple[str, str]]] = {}
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
        for node in tree.body:
            if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
                continue
            if not any(
                isinstance(name, ast.Name)
                and name.id == "EVENT_KIND_RESPONSIBILITIES"
                for name in node.targets
            ):
                continue
            for key, value in zip(node.value.keys, node.value.values):
                kind = constants.get(key.id) if isinstance(key, ast.Name) else None
                clause = (
                    value.value
                    if isinstance(value, ast.Constant) and isinstance(value.value, str)
                    else None
                )
                if kind is not None and clause is not None:
                    found.setdefault(kind, []).append((path.name, clause))
    return found


def _dict_value(node: ast.Dict, coordinate: str) -> ast.expr | None:
    for key, value in zip(node.keys, node.values):
        if isinstance(key, ast.Constant) and key.value == coordinate:
            return value
    return None


def _resolved_string(value, constants: dict[str, str]) -> str | None:
    if isinstance(value, ast.Name):
        return constants.get(value.id)
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    return None


def _assertion_responsibilities(
    path: Path, tree: ast.Module
) -> dict[str, list[tuple[str, int]]]:
    constants = _module_strings(tree)
    found: dict[str, list[tuple[str, int]]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        subject_kind = _dict_value(node, "subject_kind")
        if _resolved_string(subject_kind, constants) != "assertion":
            continue
        dimensions = _dict_value(node, "dimensions")
        if not isinstance(dimensions, ast.Dict):
            continue
        responsibility = _dict_value(dimensions, "responsibility")
        value = _resolved_string(responsibility, constants)
        if value is not None:
            found.setdefault(value, []).append((path.name, node.lineno))
    return found


def _runtime_assertion_responsibilities() -> dict[str, list[tuple[str, int]]]:
    found: dict[str, list[tuple[str, int]]] = {}
    for path, tree in _runtime_trees():
        for responsibility, locations in _assertion_responsibilities(
            path, tree
        ).items():
            found.setdefault(responsibility, []).extend(locations)
    return found


def _unresolved_assertion_responsibilities(
    path: Path, tree: ast.Module
) -> list[tuple[str, int]]:
    constants = _module_strings(tree)
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        subject_kind = _dict_value(node, "subject_kind")
        resolved_kind = _resolved_string(subject_kind, constants)
        if subject_kind is not None and resolved_kind is None:
            found.append((path.name, node.lineno))
            continue
        if resolved_kind != "assertion":
            continue
        dimensions = _dict_value(node, "dimensions")
        responsibility = (
            _dict_value(dimensions, "responsibility")
            if isinstance(dimensions, ast.Dict)
            else None
        )
        if _resolved_string(responsibility, constants) is None:
            found.append((path.name, node.lineno))
    return found


def _assertion_responsibility_clauses(
    path: Path, tree: ast.Module
) -> dict[str, list[tuple[str, str]]]:
    found: dict[str, list[tuple[str, str]]] = {}
    constants = _module_strings(tree)
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
            continue
        if not any(
            isinstance(name, ast.Name)
            and name.id == "ASSERTION_RESPONSIBILITIES"
            for name in node.targets
        ):
            continue
        for key, value in zip(node.value.keys, node.value.values):
            responsibility = _resolved_string(key, constants)
            clause = _resolved_string(value, constants)
            if responsibility is not None and clause is not None:
                found.setdefault(responsibility, []).append((path.name, clause))
    return found


def _runtime_assertion_responsibility_clauses() -> dict[
    str, list[tuple[str, str]]
]:
    found: dict[str, list[tuple[str, str]]] = {}
    for path, tree in _runtime_trees():
        for responsibility, declarations in _assertion_responsibility_clauses(
            path, tree
        ).items():
            found.setdefault(responsibility, []).extend(declarations)
    return found


def _literal_dict_keys(tree: ast.Module):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                yield key.lineno, key.value


def _coordinate_substitutions(path: Path, tree: ast.Module):
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        by_expression = {}
        for key, value in zip(node.keys, node.values):
            if not (
                isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and not isinstance(
                    value,
                    (ast.Constant, ast.List, ast.Tuple, ast.Set, ast.Dict),
                )
            ):
                continue
            expression = ast.dump(value, include_attributes=False)
            by_expression.setdefault(expression, []).append(key.value)
        found.extend(
            (path.name, node.lineno, tuple(coordinates))
            for coordinates in by_expression.values()
            if len(coordinates) > 1
        )
    return found


def _scope_nodes(scope):
    pending = list(scope.body)
    while pending:
        node = pending.pop()
        yield node
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)
        ):
            continue
        pending.extend(ast.iter_child_nodes(node))


def _scopes(tree: ast.Module):
    yield tree
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            yield node


def _named_dicts(scope):
    found = {}
    for node in _scope_nodes(scope):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if not isinstance(value, ast.Dict):
            continue
        names = node.targets if isinstance(node, ast.Assign) else [node.target]
        for name in names:
            if isinstance(name, ast.Name):
                found.setdefault(name.id, []).append((node.lineno, value))
    return found


def _named_values(scope):
    found = {}
    for node in _scope_nodes(scope):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        names = node.targets if isinstance(node, ast.Assign) else [node.target]
        for name in names:
            if isinstance(name, ast.Name):
                found.setdefault(name.id, []).append((node.lineno, node.value))
    return found


def _resolved_named_value(name: str, *, line: int, named):
    candidates = [item for item in named.get(name, ()) if item[0] < line]
    return max(candidates, default=(None, None))[1]


def _local_call_bindings(call: ast.Call, function) -> dict[str, list[tuple[int, ast.AST]]]:
    parameters = [*function.args.posonlyargs, *function.args.args]
    found = {
        parameter.arg: [(0, supplied)]
        for parameter, supplied in zip(parameters, call.args)
    }
    found.update(
        {
            keyword.arg: [(0, keyword.value)]
            for keyword in call.keywords
            if keyword.arg is not None
        }
    )
    return found


def _authored_strings(value, *, line: int, named, functions=None, resolving=()):
    if isinstance(value, ast.Constant):
        if isinstance(value.value, str):
            yield value.lineno, value.value
        return
    if isinstance(value, ast.Name):
        if value.id in resolving:
            return
        resolved = _resolved_named_value(value.id, line=line, named=named)
        if resolved is not None:
            yield from _authored_strings(
                resolved,
                line=line,
                named=named,
                functions=functions,
                resolving=(*resolving, value.id),
            )
        return
    if isinstance(value, ast.Dict):
        for nested in value.values:
            yield from _authored_strings(
                nested,
                line=line,
                named=named,
                functions=functions,
                resolving=resolving,
            )
        return
    if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
        for nested in value.elts:
            yield from _authored_strings(
                nested,
                line=line,
                named=named,
                functions=functions,
                resolving=resolving,
            )
        return
    if isinstance(value, ast.JoinedStr):
        for nested in value.values:
            if isinstance(nested, ast.Constant) and isinstance(nested.value, str):
                yield nested.lineno, nested.value
        return
    if isinstance(value, (ast.BinOp, ast.IfExp)):
        for nested in ast.iter_child_nodes(value):
            yield from _authored_strings(
                nested,
                line=line,
                named=named,
                functions=functions,
                resolving=resolving,
            )
        return
    if (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name)
        and value.func.id in {"dict", "list", "set", "tuple"}
    ):
        for nested in value.args:
            yield from _authored_strings(
                nested,
                line=line,
                named=named,
                functions=functions,
                resolving=resolving,
            )
        for keyword in value.keywords:
            yield from _authored_strings(
                keyword.value,
                line=line,
                named=named,
                functions=functions,
                resolving=resolving,
            )
        return
    if not (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name)
        and functions
        and value.func.id in functions
        and value.func.id not in resolving
    ):
        return
    function = functions[value.func.id]
    function_named = {name: list(values) for name, values in named.items()}
    for name, values in _named_values(function).items():
        function_named.setdefault(name, []).extend(values)
    function_named.update(_local_call_bindings(value, function))
    function_dicts = _named_dicts(function)
    for node in _scope_nodes(function):
        if not isinstance(node, ast.Return):
            continue
        returned = _resolved_material_dict(
            node.value,
            line=node.lineno,
            named=function_dicts,
            functions=functions,
            resolving=(*resolving, value.func.id),
        )
        if returned is not None:
            yield from _authored_strings(
                returned,
                line=line,
                named=function_named,
                functions=functions,
                resolving=(*resolving, value.func.id),
            )


def _authored_event_material_strings(path: Path, tree: ast.Module):
    module_named = _named_values(tree)
    functions = _module_functions(tree)
    for scope in _scopes(tree):
        named = {name: list(values) for name, values in module_named.items()}
        if scope is not tree:
            for name, values in _named_values(scope).items():
                named.setdefault(name, []).extend(values)
        named_dicts = _named_dicts(scope)
        for call in (
            node for node in _scope_nodes(scope) if isinstance(node, ast.Call)
        ):
            material = None
            if isinstance(call.func, ast.Attribute) and call.func.attr == "append":
                if len(call.args) >= 2:
                    material = call.args[1]
            elif isinstance(call.func, ast.Name) and call.func.id == "Event":
                keywords = {item.arg: item.value for item in call.keywords}
                material = keywords.get("material")
            resolved = _resolved_material_dict(
                material,
                line=call.lineno,
                named=named_dicts,
                functions=functions,
            )
            if resolved is None:
                continue
            for line, authored in _authored_strings(
                resolved,
                line=call.lineno,
                named=named,
                functions=functions,
            ):
                yield path.name, line, authored


def _named_dict_additions(scope):
    found = {}
    for node in _scope_nodes(scope):
        if not isinstance(node, ast.Assign):
            continue
        targets = node.targets
        for target in targets:
            if not (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and isinstance(target.slice, ast.Constant)
                and isinstance(target.slice.value, str)
            ):
                continue
            found.setdefault(target.value.id, []).append(
                (node.lineno, target.slice.value)
            )
    return found


def _resolved_material_dict(
    value, *, line, named, functions=None, resolving=()
):
    if isinstance(value, ast.Dict):
        return value
    if isinstance(value, ast.Name):
        candidates = [item for item in named.get(value.id, ()) if item[0] < line]
        return max(candidates, default=(None, None))[1]
    if not (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Name)
        and functions
        and value.func.id in functions
        and value.func.id not in resolving
    ):
        return None
    function = functions[value.func.id]
    returned = []
    function_named = _named_dicts(function)
    for node in ast.walk(function):
        if not isinstance(node, ast.Return):
            continue
        resolved = _resolved_material_dict(
            node.value,
            line=node.lineno,
            named=function_named,
            functions=functions,
            resolving=(*resolving, value.func.id),
        )
        if resolved is not None:
            returned.append(resolved)
    if not returned:
        return None
    return ast.Dict(
        keys=[key for result in returned for key in result.keys],
        values=[nested for result in returned for nested in result.values],
    )


def _resolved_dict_keys(
    value: ast.Dict, *, line: int, named, additions, functions, source_name=None
) -> set[str]:
    found = set()
    if source_name is not None:
        found.update(
            key for added_line, key in additions.get(source_name, ()) if added_line < line
        )
    for key, nested in zip(value.keys, value.values):
        if isinstance(key, ast.Constant) and isinstance(key.value, str):
            found.add(key.value)
        elif key is None:
            spread = _resolved_material_dict(
                nested, line=line, named=named, functions=functions
            )
            if spread is not None:
                found.update(
                    _resolved_dict_keys(
                        spread,
                        line=line,
                        named=named,
                        additions=additions,
                        functions=functions,
                        source_name=nested.id if isinstance(nested, ast.Name) else None,
                    )
                )
    return found


def _unresolved_dict_spreads(value, *, line, named, functions):
    for key, nested in zip(value.keys, value.values):
        if key is not None:
            continue
        spread = _resolved_material_dict(
            nested, line=line, named=named, functions=functions
        )
        if spread is None:
            yield nested.lineno
            continue
        yield from _unresolved_dict_spreads(
            spread,
            line=line,
            named=named,
            functions=functions,
        )


@pytest.mark.subject("unresolved_event_material_visibility")
def test_unresolved_event_material_expansion_remains_visible():
    tree = ast.parse('{"identity": result_identity, **supplied_material}')
    material = tree.body[0].value

    assert list(
        _unresolved_dict_spreads(
            material,
            line=1,
            named={},
            functions={},
        )
    ) == [1]


@pytest.mark.subject("event_kind_grammar_responsibility")
def test_every_runtime_event_kind_declares_its_machine_grammar_responsibility():
    """A new event species cannot gain constitutional force from its name."""

    declared = _runtime_event_kinds()
    accounted = _runtime_event_kind_responsibilities()

    assert set(declared) == set(accounted), (
        "\nLive event kinds and machine-grammar responsibilities disagree."
        f"\n  only live: {sorted(set(declared) - set(accounted))}"
        f"\n  only responsibility declaration: {sorted(set(accounted) - set(declared))}"
    )


@pytest.mark.subject("event_kind_responsibility_clause")
def test_each_event_kind_responsibility_names_one_machine_grammar_clause():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    accounted = _runtime_event_kind_responsibilities()
    duplicate = {
        kind: values for kind, values in accounted.items() if len(values) != 1
    }
    assert duplicate == {}, f"event species declare several responsibilities: {duplicate}"
    clauses = set(grammar["clauses"])
    unknown = {
        kind: values[0]
        for kind, values in accounted.items()
        if values[0][1] not in clauses
    }
    assert unknown == {}, f"event species name absent grammar clauses: {unknown}"


@pytest.mark.subject("assertion_responsibility_clause_declarations")
def test_each_live_assertion_responsibility_has_one_clause_declaration():
    live = _runtime_assertion_responsibilities()
    accounted = _runtime_assertion_responsibility_clauses()
    unresolved = [
        location
        for path, tree in _runtime_trees()
        for location in _unresolved_assertion_responsibilities(path, tree)
    ]

    assert unresolved == [], f"unresolved nested Assertion responsibility: {unresolved}"
    assert set(live) == set(accounted), (
        "\nLive nested Assertion responsibilities and clause declarations disagree."
        f"\n  only live: {sorted(set(live) - set(accounted))}"
        f"\n  only declaration: {sorted(set(accounted) - set(live))}"
    )
    duplicate = {
        responsibility: values
        for responsibility, values in accounted.items()
        if len(values) != 1
    }
    assert duplicate == {}, (
        "nested Assertion responsibilities name several clauses: "
        f"{duplicate}"
    )


@pytest.mark.subject("assertion_responsibility_machine_clause")
def test_each_assertion_responsibility_names_one_machine_grammar_clause():
    machine_clauses = {
        identity.decode("ascii")
        for identity in re.findall(
            rb'^    "([0-9]+\.[A-Za-z]+\.[A-Za-z0-9.]+)": \{$',
            GRAMMAR.read_bytes(),
            re.M,
        )
    }
    accounted = _runtime_assertion_responsibility_clauses()
    unknown = {
        responsibility: values[0]
        for responsibility, values in accounted.items()
        if len(values) == 1 and values[0][1] not in machine_clauses
    }

    assert unknown == {}, f"nested Assertion names absent grammar clauses: {unknown}"


@pytest.mark.subject("assertion_responsibility_subject_distinction")
def test_nested_assertion_responsibility_discovery_does_not_depend_on_its_name():
    tree = ast.parse(
        """
UNEXPECTED = "a responsibility not known to the siren"
material = {
    "dimensions": {"responsibility": UNEXPECTED},
    "subject_kind": "assertion",
}
"""
    )

    assert _assertion_responsibilities(Path("adversary.py"), tree) == {
        "a responsibility not known to the siren": [("adversary.py", 3)]
    }


@pytest.mark.subject("assertion_responsibility_coordinate_resolution")
def test_nested_assertion_responsibility_discovery_refuses_an_opaque_coordinate():
    tree = ast.parse(
        """
def supplied():
    return "not statically established"
material = {
    "dimensions": {"responsibility": supplied()},
    "subject_kind": "assertion",
}
"""
    )

    assert _unresolved_assertion_responsibilities(
        Path("adversary.py"), tree
    ) == [("adversary.py", 4)]


@pytest.mark.subject("assertion_responsibility_duplicate_declarations")
def test_nested_assertion_clause_declarations_preserve_duplicates():
    tree = ast.parse(
        """
RESPONSIBILITY = "one exact responsibility"
ASSERTION_RESPONSIBILITIES = {RESPONSIBILITY: "01.Standing.D.1"}
ASSERTION_RESPONSIBILITIES = {RESPONSIBILITY: "02.Acts.A"}
"""
    )

    assert _assertion_responsibility_clauses(Path("adversary.py"), tree) == {
        "one exact responsibility": [
            ("adversary.py", "01.Standing.D.1"),
            ("adversary.py", "02.Acts.A"),
        ]
    }


@pytest.mark.subject("assertion_event_responsibility_distinction")
def test_nested_assertion_clause_is_not_an_event_kind_responsibility():
    event_clauses = {
        clause
        for declarations in _runtime_event_kind_responsibilities().values()
        for _path, clause in declarations
    }
    assertion_clauses = {
        clause
        for declarations in _runtime_assertion_responsibility_clauses().values()
        for _path, clause in declarations
    }

    assert "01.Standing.D.1" not in event_clauses
    assert "01.Standing.D.1" in assertion_clauses


@pytest.mark.subject("witness_machine_clause_distinction")
def test_witness_and_machine_grammar_account_for_the_same_clauses():
    event_clauses = {
        values[0][1]
        for values in _runtime_event_kind_responsibilities().values()
        if len(values) == 1
    }
    assertion_clauses = {
        values[0][1]
        for values in _runtime_assertion_responsibility_clauses().values()
        if len(values) == 1
    }
    machine = json.loads(GRAMMAR.read_text(encoding="utf-8"))["clauses"]
    machine_clauses = set(machine)
    declared_without_event_species = {
        identity
        for identity, clause in machine.items()
        if "witness" in clause
    }
    implemented_clauses = event_clauses | assertion_clauses

    assert implemented_clauses <= machine_clauses
    assert machine_clauses - implemented_clauses == declared_without_event_species


@pytest.mark.subject("event_record_coordinate_vocabulary_admission")
def test_runtime_record_vocabulary_has_constitutional_admission():
    """Event species and record coordinates require lexical admission."""

    violations = []
    admitted = book_admission()
    for path, tree in _runtime_trees():
        material = [
            (node.lineno, node.value.value)
            for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            and any(
                isinstance(name, ast.Name) and name.id.endswith("_KIND")
                for name in node.targets
            )
        ]
        material.extend(_literal_dict_keys(tree))
        for line, value in material:
            scanned = scan_active_line(value)
            for word in re.findall(r"[A-Za-z]+", scanned.lower()):
                if word not in admitted:
                    violations.append((path.name, line, word, value))

    assert violations == [], "\n" + "\n".join(
        f"{path}:{line} [{word}] {value}"
        for path, line, word, value in violations
    )


def _unadmitted_authored_event_material(path: Path, tree: ast.Module):
    admitted = book_admission()
    violations = set()
    for source, line, value in _authored_event_material_strings(path, tree):
        for word in re.findall(r"[A-Za-z]+", scan_active_line(value).lower()):
            if word not in admitted:
                violations.add((source, line, word, value))
    return sorted(violations)


@pytest.mark.subject("seed_event_material_vocabulary_admission")
def test_seed_authored_event_material_values_have_lexical_admission():
    violations = []
    for path, tree in _runtime_trees():
        violations.extend(_unadmitted_authored_event_material(path, tree))
    assert violations == [], "\n" + "\n".join(
        f"{path}:{line} [{word}] {value}"
        for path, line, word, value in violations
    )


def _runtime_record_words() -> set[str]:
    found = set()
    for path, tree in _runtime_trees():
        values = [
            node.value.value
            for node in tree.body
            if isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            and any(
                isinstance(name, ast.Name) and name.id.endswith("_KIND")
                for name in node.targets
            )
        ]
        values.extend(value for _line, value in _literal_dict_keys(tree))
        values.extend(
            value
            for _source, _line, value in _authored_event_material_strings(path, tree)
        )
        found.update(
            word
            for value in values
            for word in re.findall(r"[A-Za-z]+", scan_active_line(value).lower())
        )
    return found


@pytest.mark.subject("event_record_machine_grammar_vocabulary")
def test_runtime_record_words_are_machine_grammar_words():
    assert _runtime_record_words() <= machine_grammar_words()


@pytest.mark.subject("event_material_vocabulary_admission")
def test_authored_value_admission_catches_an_unadmitted_word_without_naming_it():
    tree = ast.parse(
        'ledger.append(SOME_KIND, {"standing": "invented"})'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == [
        ("fixture.py", 1, "invented", "invented")
    ]


@pytest.mark.subject("event_material_vocabulary_admission")
def test_authored_value_admission_crosses_a_local_material_function():
    tree = ast.parse(
        'def material():\n    return {"standing": "invented"}\n'
        'ledger.append(SOME_KIND, material())'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == [
        ("fixture.py", 2, "invented", "invented")
    ]


@pytest.mark.subject("event_material_vocabulary_admission")
def test_authored_value_admission_binds_local_material_function_arguments():
    tree = ast.parse(
        'def material(*, standing):\n    return {"standing": standing}\n'
        'ledger.append(SOME_KIND, {"dimensions": material(standing="invented")})'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == [
        ("fixture.py", 3, "invented", "invented")
    ]


@pytest.mark.subject("supplied_material_seed_vocabulary_distinction")
def test_opaque_supplied_material_is_not_seed_authored_language():
    tree = ast.parse(
        'ledger.append(SOME_KIND, {"standing": operator_material})'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == []


@pytest.mark.subject("coordinate_reference_distinction")
def test_runtime_coordinates_do_not_substitute_one_reference_for_several_coordinates():
    substitutions = []
    for path, tree in _runtime_trees():
        substitutions.extend(_coordinate_substitutions(path, tree))
    assert substitutions == [], "\n" + "\n".join(
        f"{path}:{line} one reference supplies {list(coordinates)}"
        for path, line, coordinates in substitutions
    )


@pytest.mark.subject("coordinate_reference_distinction")
def test_coordinate_substitution_siren_detects_one_shared_reference():
    tree = ast.parse(
        'dimensions = {"identity": result_identity, "content": result_identity}'
    )
    assert _coordinate_substitutions(Path("fixture.py"), tree) == [
        ("fixture.py", 1, ("identity", "content"))
    ]


def _event_materials():
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
        functions = _module_functions(tree)
        for scope in _scopes(tree):
            named_dicts = _named_dicts(scope)
            additions = _named_dict_additions(scope)
            for call in (
                node for node in _scope_nodes(scope) if isinstance(node, ast.Call)
            ):
                kind = None
                material = None
                if isinstance(call.func, ast.Attribute) and call.func.attr == "append":
                    if len(call.args) >= 2:
                        kind, material = call.args[0], call.args[1]
                elif isinstance(call.func, ast.Name) and call.func.id == "Event":
                    keywords = {item.arg: item.value for item in call.keywords}
                    kind, material = keywords.get("kind"), keywords.get("material")
                material_expression = material
                material = _resolved_material_dict(
                    material_expression,
                    line=call.lineno,
                    named=named_dicts,
                    functions=functions,
                )
                if material is None:
                    continue
                if isinstance(kind, ast.Name):
                    value = constants.get(kind.id)
                    name = kind.id
                elif isinstance(kind, ast.Constant) and isinstance(kind.value, str):
                    value = kind.value
                    name = "literal"
                else:
                    continue
                if value is not None:
                    yield (
                        path,
                        call.lineno,
                        name,
                        value,
                        _resolved_dict_keys(
                            material,
                            line=call.lineno,
                            named=named_dicts,
                            additions=additions,
                            functions=functions,
                            source_name=(
                                material_expression.id
                                if isinstance(material_expression, ast.Name)
                                else None
                            ),
                        ),
                    )


def _unread_event_materials():
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
        functions = _module_functions(tree)
        for scope in _scopes(tree):
            named_dicts = _named_dicts(scope)
            for call in (
                node for node in _scope_nodes(scope) if isinstance(node, ast.Call)
            ):
                kind = None
                material = None
                if (
                    isinstance(call.func, ast.Attribute)
                    and call.func.attr == "append"
                    and len(call.args) >= 2
                ):
                    kind, material = call.args[0], call.args[1]
                elif isinstance(call.func, ast.Name) and call.func.id == "Event":
                    keywords = {item.arg: item.value for item in call.keywords}
                    kind, material = keywords.get("kind"), keywords.get("material")
                if kind is None or material is None:
                    continue
                if isinstance(kind, ast.Name):
                    value = constants.get(kind.id)
                elif isinstance(kind, ast.Constant) and isinstance(kind.value, str):
                    value = kind.value
                else:
                    value = None
                if value is None:
                    continue
                resolved = _resolved_material_dict(
                    material,
                    line=call.lineno,
                    named=named_dicts,
                    functions=functions,
                )
                if resolved is None or list(
                    _unresolved_dict_spreads(
                        resolved,
                        line=call.lineno,
                        named=named_dicts,
                        functions=functions,
                    )
                ):
                    yield path.name, call.lineno, value


@pytest.mark.subject("event_occurrence_material_inspection")
def test_every_declared_event_occurrence_carries_its_material_to_the_sirens():
    assert list(_unread_event_materials()) == []


@pytest.mark.subject("event_record_relation_admission")
def test_every_relation_shaped_runtime_record_is_an_admitted_relation():
    admitted = set()
    for _path, tree in _runtime_trees():
        for name, value in _module_strings(tree).items():
            if any(
                family in name
                for family in (
                    "LOCALITY_EVIDENCE_KIND",
                    "PARTICIPATION_EVIDENCE_KIND",
                    "RECORDED_EVIDENCE_OF_YIELD_RELATION_KIND",
                )
            ) or name == "ASSERTION_LOCALITY_MOVEMENT_KIND":
                admitted.add(value)

    relation_shaped = set()
    for _path, _line, name, value, keys in _event_materials():
        if name.endswith("RELATED_KIND") or {"first_subject", "second_subject"} <= keys:
            relation_shaped.add(value)

    assert relation_shaped <= admitted, (
        "\nRuntime records assert a relation without an admitted relation witness:"
        f"\n  {sorted(relation_shaped - admitted)}"
    )


@pytest.mark.subject("machine_relation_declarations")
def test_machine_grammar_declares_the_four_exact_relations():
    grammar_relations = set(
        json.loads(GRAMMAR.read_text(encoding="utf-8"))["relations"]
    )

    assert grammar_relations == {
        "participation",
        "yield",
        "locality",
        "carried_by",
    }


@pytest.mark.subject("yield_result_occurrence_evidence")
def test_every_recorded_yield_result_names_its_occurrence_and_exact_evidence():
    required = {
        "responsible_act_evidence_identity",
        "evidence_of_yield_relation_identity",
    }
    incomplete = []
    for path, line, _name, value, keys in _event_materials():
        if "evidence_of_yield_relation_identity" not in keys:
            continue
        occurrence_identities = {
            key
            for key in keys
            if key == "act_occurrence_identity" or key.endswith("_act_occurrence_identity")
        }
        missing = sorted(required - keys)
        if not occurrence_identities:
            missing.append("exact Act occurrence identity")
        if missing:
            incomplete.append((path.name, line, value, missing))

    assert incomplete == [], "\n" + "\n".join(
        f"{path}:{line} {kind} lacks {missing}"
        for path, line, kind, missing in incomplete
    )


@pytest.mark.subject("act_evidence_responsibility_boundary_occurrence_authority_scope")
def test_every_act_evidence_occurrence_names_responsibility_boundary_act_occurrence_authority_and_evidence_scope():
    required = {
        "responsibility",
        "responsible_boundary",
        "authority",
        "evidence_scope",
    }
    incomplete = []
    for path, line, name, value, keys in _event_materials():
        if not (name.endswith("ACT_EVIDENCE_KIND") or value.endswith("act_evidenced")):
            continue
        act_identities = {
            key for key in keys if key == "downstream_act_identity" or key.endswith("_act_identity")
        }
        occurrence_identities = {
            key
            for key in keys
            if key == "act_occurrence_identity" or key.endswith("_act_occurrence_identity")
        }
        missing = sorted(required - keys)
        if not act_identities:
            missing.append("exact Act identity")
        if not occurrence_identities:
            missing.append("exact Act occurrence identity")
        if missing:
            incomplete.append((path.name, line, value, missing))

    assert incomplete == [], "\n" + "\n".join(
        f"{path}:{line} {kind} lacks {missing}"
        for path, line, kind, missing in incomplete
    )


@pytest.mark.subject("representation_exact_evidence_references")
def test_recorded_representation_declares_each_exact_evidence_pointer():
    required = {
        "result_identity",
        "representation_act_identity",
        "act_occurrence_identity",
        "responsible_act_evidence_identity",
        "locality_evidence_identity",
        "evidence_of_yield_relation_identity",
    }
    records = [
        (path.name, line, keys)
        for path, line, _name, value, keys in _event_materials()
        if value == "operator.representation.recorded"
    ]
    assert records
    assert [
        (path, line, sorted(required - keys))
        for path, line, keys in records
        if required - keys
    ] == []


def _standing_values(node) -> list[str]:
    found = []
    if isinstance(node, ast.Dict):
        for key, value in zip(node.keys, node.values):
            if (
                isinstance(key, ast.Constant)
                and key.value == "standing"
                and isinstance(value, ast.Constant)
                and isinstance(value.value, str)
            ):
                found.append(value.value)
            found.extend(_standing_values(value))
    elif isinstance(node, ast.Call):
        for keyword in node.keywords:
            if (
                keyword.arg == "standing"
                and isinstance(keyword.value, ast.Constant)
                and isinstance(keyword.value.value, str)
            ):
                found.append(keyword.value.value)
            found.extend(_standing_values(keyword.value))
    elif isinstance(node, (ast.List, ast.Tuple)):
        for item in node.elts:
            found.extend(_standing_values(item))
    return found


@pytest.mark.subject("event_standing_grammar_responsibility")
def test_every_event_standing_claim_has_a_declared_grammar_responsibility():
    accounted = set(_runtime_event_kind_responsibilities())
    unaccounted = []
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
        functions = _module_functions(tree)
        for scope in _scopes(tree):
            named_dicts = _named_dicts(scope)
            for call in (
                node for node in _scope_nodes(scope) if isinstance(node, ast.Call)
            ):
                if not (
                    isinstance(call.func, ast.Attribute)
                    and call.func.attr == "append"
                    and len(call.args) >= 2
                ):
                    continue
                kind, material = call.args[0], call.args[1]
                value = constants.get(kind.id) if isinstance(kind, ast.Name) else None
                if isinstance(kind, ast.Constant) and isinstance(kind.value, str):
                    value = kind.value
                material = _resolved_material_dict(
                    material,
                    line=call.lineno,
                    named=named_dicts,
                    functions=functions,
                )
                if value is None or material is None:
                    continue
                standings = _standing_values(material)
                if standings and value not in accounted:
                    unaccounted.append((path.name, call.lineno, value, standings))

    assert unaccounted == [], "\n" + "\n".join(
        f"{path}:{line} {kind} carries Standing {standings} without grammar responsibility"
        for path, line, kind, standings in unaccounted
    )


@pytest.mark.subject("operator_request_write_exclusion")
def test_command_handler_receives_no_constitutional_write_capability():
    """The slash-command boundary may not hand a handler the ledger."""

    names = {field.name for field in fields(AddressedOperatorCommand)}
    assert "ledger" not in names
    assert names == {
        "command_identity",
        "locality_identity",
        "addressed_at_representation_event_identity",
        "frame",
    }


@pytest.mark.subject("standing_boundary_reference_representation_emission_distinction")
def test_checkpoint_names_the_representation_it_addresses_not_an_emission():
    wording = inspect.getdoc(
        record_standing_boundary_reference_responsibility_assignment
    ) or ""

    assert "exact addressed Representation" in wording
    assert "exact addressed emission" not in wording
