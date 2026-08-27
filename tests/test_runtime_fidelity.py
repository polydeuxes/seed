"""Reverse Fidelity sirens from the live witness back to witness grammar.

These tests are deliberately bounded by what the runtime declares. They do
not ask a hand-maintained list which witnesses should be inspected.
Red means the witness contains constitutional material the witness
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

from seed_runtime.events import EventLedger
from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.operator_console import run_persistent_operator_console
from scripts.book_admission import (
    book_admission,
    witness_grammar_words,
    scan_active_line,
)


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "seed_runtime"
GRAMMAR = ROOT / "book_of_seed" / "witness_grammar.json"


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


def _declared_event_kind_book_clauses() -> dict[str, list[tuple[str, str]]]:
    found: dict[str, list[tuple[str, str]]] = {}
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
        for node in tree.body:
            if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Dict):
                continue
            if not any(
                isinstance(name, ast.Name)
                and name.id == "EVENT_KIND_BOOK_CLAUSES"
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


def _event_material_book_references() -> dict[str, list[tuple[str, str]]]:
    """Read constitutional ownership from each occurrence's exact material."""

    found: dict[str, list[tuple[str, str]]] = {}
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
                resolved = _resolved_material_dict(
                    material,
                    line=call.lineno,
                    named=named_dicts,
                    functions=functions,
                )
                if value is None or resolved is None:
                    continue
                book_reference = _resolved_string(
                    _dict_value(resolved, "book_reference"), constants
                )
                if book_reference is not None:
                    found.setdefault(value, []).append(
                        (path.name, book_reference)
                    )
    return {
        stream: sorted(set(references))
        for stream, references in found.items()
    }


def _runtime_event_kind_book_clauses() -> dict[str, list[tuple[str, str]]]:
    """Prefer carried Book references over storage-stream declarations."""

    declared = _declared_event_kind_book_clauses()
    carried = _event_material_book_references()
    return {
        stream: carried.get(stream, declarations)
        for stream, declarations in (declared | carried).items()
    }


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


def test_every_runtime_event_kind_declares_its_witness_grammar_book_clause():
    """A new event species cannot gain constitutional force from its name."""

    declared = _runtime_event_kinds()
    accounted = _runtime_event_kind_book_clauses()

    assert set(declared) == set(accounted), (
        "\nLive event kinds and witness-grammar Book clauses disagree."
        f"\n  only live: {sorted(set(declared) - set(accounted))}"
        f"\n  only Book-clause declaration: {sorted(set(accounted) - set(declared))}"
    )


def test_each_recorded_occurrence_reference_names_a_witness_grammar_clause():
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    accounted = _runtime_event_kind_book_clauses()
    clauses = set(
        grammar.get("book_coordinates", grammar.get("clause_coordinates", {}))
    )
    absent_clauses = {
        kind: values
        for kind, values in accounted.items()
        if any(clause not in clauses for _path, clause in values)
    }
    assert absent_clauses == {}, (
        f"occurrences name absent grammar clauses: {absent_clauses}"
    )


def _unadmitted_authored_event_material(path: Path, tree: ast.Module):
    admitted = book_admission()
    violations = set()
    for source, line, value in _authored_event_material_strings(path, tree):
        for word in re.findall(r"[A-Za-z]+", scan_active_line(value).lower()):
            if word not in admitted:
                violations.add((source, line, word, value))
    return sorted(violations)


def test_seed_authored_event_material_values_have_lexical_admission():
    violations = []
    for path, tree in _runtime_trees():
        violations.extend(_unadmitted_authored_event_material(path, tree))
    assert violations == [], "\n" + "\n".join(
        f"{path}:{line} [{word}] {value}"
        for path, line, word, value in violations
    )


def test_authored_value_admission_catches_an_unadmitted_word_without_naming_it():
    tree = ast.parse(
        'ledger.append(SOME_KIND, {"standing": "invented"})'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == [
        ("fixture.py", 1, "invented", "invented")
    ]


def test_authored_value_admission_crosses_a_local_material_function():
    tree = ast.parse(
        'def material():\n    return {"standing": "invented"}\n'
        'ledger.append(SOME_KIND, material())'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == [
        ("fixture.py", 2, "invented", "invented")
    ]


def test_authored_value_admission_binds_local_material_function_arguments():
    tree = ast.parse(
        'def material(*, standing):\n    return {"standing": standing}\n'
        'ledger.append(SOME_KIND, {"dimensions": material(standing="invented")})'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == [
        ("fixture.py", 3, "invented", "invented")
    ]


def test_opaque_supplied_material_is_not_seed_authored_language():
    tree = ast.parse(
        'ledger.append(SOME_KIND, {"standing": operator_material})'
    )
    assert _unadmitted_authored_event_material(Path("fixture.py"), tree) == []


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


def test_every_declared_event_occurrence_carries_its_material_to_the_sirens():
    assert list(_unread_event_materials()) == []


def test_every_relation_occurrence_carries_its_exact_relation_position():
    incomplete = []
    for path, line, _name, value, keys in _event_materials():
        if {"first_subject", "second_subject"} <= keys and "relation" not in keys:
            incomplete.append((path.name, line, value))

    assert incomplete == [], (
        "\nRuntime relation occurrences require first subject, exact relation "
        "content, and second subject:\n  "
        + "\n  ".join(f"{path}:{line} {value}" for path, line, value in incomplete)
    )


def test_witness_grammar_declares_the_exact_relations():
    coordinates = json.loads(GRAMMAR.read_text(encoding="utf-8"))["book_coordinates"]

    assert coordinates["02.Acts.A"]["Yield"]["relation"] == "yield"
    assert coordinates["06.Locality.A"]["Locality"]["relation"] == "locality"


def test_every_recorded_yield_result_names_its_occurrence_and_exact_occurrence():
    incomplete = []
    for path, line, _name, value, keys in _event_materials():
        if "yield_relation_identity" not in keys:
            continue
        occurrence_identities = {
            key
            for key in keys
            if key == "act_occurrence_identity" or key.endswith("_act_occurrence_identity")
        }
        missing = []
        if not occurrence_identities:
            missing.append("exact Act occurrence identity")
        if missing:
            incomplete.append((path.name, line, value, missing))

    assert incomplete == [], "\n" + "\n".join(
        f"{path}:{line} {kind} lacks {missing}"
        for path, line, kind, missing in incomplete
    )


def test_command_handler_receives_no_constitutional_write_capability():
    """The slash-command boundary may not hand a handler the ledger."""

    names = {field.name for field in fields(AddressedOperatorCommand)}
    assert "ledger" not in names
    assert names == {
        "locality_identity",
        "addressed_through_event_occurrence_identity",
        "frame",
    }
