"""Reverse Fidelity sirens from live implementation back to machine grammar.

These tests are deliberately bounded by what the runtime declares. They do
not ask a hand-maintained list which implementation roads should be inspected.
Red means the implementation contains constitutional material the machine
grammar and its deterministic witnesses do not yet account for.
"""

from __future__ import annotations

import ast
from dataclasses import fields
from io import BytesIO, StringIO
import inspect
import json
import os
from pathlib import Path
import re

from seed_runtime.events import EventLedger
from seed_runtime.operator_checkpoint import open_operator_checkpoint
from seed_runtime.operator_command import AddressedOperatorCommand
from seed_runtime.operator_console import run_persistent_operator_console
from tests.test_book_lexical_admission import admitted_lexicon, scan_active_line


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "seed_runtime"
GRAMMAR = ROOT / "book_of_seed" / "grammar.json"


def _runtime_trees():
    for path in sorted(RUNTIME.glob("*.py")):
        yield path, ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


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


def _literal_dict_keys(tree: ast.Module):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                yield key.lineno, key.value


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


def _resolved_material_dict(value, *, line, named):
    if isinstance(value, ast.Dict):
        return value
    if not isinstance(value, ast.Name):
        return None
    candidates = [item for item in named.get(value.id, ()) if item[0] < line]
    return max(candidates, default=(None, None))[1]


def _resolved_dict_keys(
    value: ast.Dict, *, line: int, named, additions, source_name=None
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
            spread = _resolved_material_dict(nested, line=line, named=named)
            if spread is not None:
                found.update(
                    _resolved_dict_keys(
                        spread,
                        line=line,
                        named=named,
                        additions=additions,
                        source_name=nested.id if isinstance(nested, ast.Name) else None,
                    )
                )
    return found


def test_every_runtime_event_kind_declares_its_machine_grammar_responsibility():
    """A new event species cannot gain constitutional force from its name."""

    declared = _runtime_event_kinds()
    accounted = _runtime_event_kind_responsibilities()

    assert set(declared) == set(accounted), (
        "\nLive event kinds and machine-grammar responsibilities disagree."
        f"\n  only live: {sorted(set(declared) - set(accounted))}"
        f"\n  only responsibility declaration: {sorted(set(accounted) - set(declared))}"
    )


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


def test_runtime_record_vocabulary_has_constitutional_admission():
    """Event species and record coordinates require lexical admission."""

    violations = []
    admitted = admitted_lexicon()
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


def _event_materials():
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
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
                    material_expression, line=call.lineno, named=named_dicts
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
                if isinstance(kind, ast.Name):
                    value = constants.get(kind.id)
                elif isinstance(kind, ast.Constant) and isinstance(kind.value, str):
                    value = kind.value
                else:
                    value = None
                if value is None:
                    continue
                if _resolved_material_dict(
                    material, line=call.lineno, named=named_dicts
                ) is None:
                    yield path.name, call.lineno, value


def test_every_declared_event_append_exposes_its_material_to_the_sirens():
    assert list(_unread_event_materials()) == []


def test_every_edge_shaped_runtime_record_is_an_admitted_structural_edge():
    """Implementation-to-grammar closure for relation-shaped records."""

    admitted = set()
    for _path, tree in _runtime_trees():
        for name, value in _module_strings(tree).items():
            if any(
                family in name
                for family in (
                    "LOCALITY_EVIDENCE_KIND",
                    "PARTICIPATION_EVIDENCE_KIND",
                    "YIELD_EVIDENCE_KIND",
                )
            ) or name == "ASSERTION_LOCALITY_MOVEMENT_KIND":
                admitted.add(value)

    edge_shaped = set()
    for _path, _line, name, value, keys in _event_materials():
        if name.endswith("RELATED_KIND") or {"first_subject", "second_subject"} <= keys:
            edge_shaped.add(value)

    grammar_edges = set(
        json.loads(GRAMMAR.read_text(encoding="utf-8"))["structural_edges"]
    )
    assert grammar_edges == {"participation", "yield", "locality"}
    assert edge_shaped <= admitted, (
        "\nRuntime records assert an edge without an admitted structural-edge witness:"
        f"\n  {sorted(edge_shaped - admitted)}"
    )


def test_every_recorded_yield_result_names_its_occurrence_and_exact_evidence():
    required = {
        "responsible_act_evidence_identity",
        "yield_evidence_identity",
    }
    incomplete = []
    for path, line, _name, value, keys in _event_materials():
        if "yield_evidence_identity" not in keys:
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


def test_every_act_evidence_occurrence_carries_the_exact_act_physiology():
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


def test_recorded_representation_declares_each_exact_evidence_pointer():
    required = {
        "representation_reference",
        "representation_act_identity",
        "act_occurrence_identity",
        "responsible_act_evidence_identity",
        "locality_evidence_identity",
        "yield_evidence_identity",
        "emission_text",
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


def test_every_event_standing_claim_has_a_declared_grammar_responsibility():
    accounted = set(_runtime_event_kind_responsibilities())
    unaccounted = []
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
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
                    material, line=call.lineno, named=named_dicts
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


def test_command_implementation_receives_no_constitutional_write_capability():
    """The slash-command boundary may not hand an implementation the ledger."""

    names = {field.name for field in fields(AddressedOperatorCommand)}
    assert "ledger" not in names
    assert names == {
        "command_identity",
        "locality_identity",
        "addressed_at_representation_event_identity",
        "frame",
    }


def test_unestablished_material_authority_does_not_cross_the_filesystem_boundary(
    monkeypatch, tmp_path
):
    """An operator request alone is not Authority for a Seed-owned read."""

    material = tmp_path / "book.bin"
    material.write_bytes(b"book bytes")
    crossed = []
    real_lstat = os.lstat

    def record_crossing(path):
        crossed.append(path)
        return real_lstat(path)

    monkeypatch.setattr(os, "lstat", record_crossing)
    run_persistent_operator_console(
        ledger=EventLedger(),
        locality_identity="l",
        input_stream=BytesIO(b"/material " + os.fsencode(material) + b"\n"),
        output_stream=StringIO(),
    )

    assert crossed == []


def test_checkpoint_names_the_representation_it_addresses_not_an_emission():
    wording = inspect.getdoc(open_operator_checkpoint) or ""

    assert "exact Representation addressed by the command" in wording
    assert "exact emission addressed by the command" not in wording
