"""Reverse Fidelity sirens from live implementation back to machine grammar.

These tests are deliberately closed over what the runtime declares.  They do
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

from seed_runtime.events import EventLedger
from seed_runtime.operator_checkpoint import open_operator_checkpoint
from seed_runtime.operator_command import OperatorCommandContext
from seed_runtime.operator_console import run_persistent_operator_console
from seed_runtime.operator_material_command import (
    MATERIAL_TARGET_READ_KIND,
    OperatorMaterialCommand,
)
from tests.test_book_lexical_contamination import COMPILED, scan_active_line


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
    for path, tree in _runtime_trees():
        for name, value in _module_strings(tree).items():
            if name.endswith("_KIND"):
                found.setdefault(value, []).append(f"{path.name}:{name}")
    return found


def _literal_dict_keys(tree: ast.Module):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key in node.keys:
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                yield key.lineno, key.value


def test_every_runtime_event_kind_declares_its_machine_grammar_responsibility():
    """A new event species cannot gain constitutional force from its name."""

    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    declared = _runtime_event_kinds()
    accounted = grammar["implementation_witness"].get("event_kinds", {})

    assert set(declared) == set(accounted), (
        "\nLive event kinds and machine-grammar responsibilities disagree."
        f"\n  only live: {sorted(set(declared) - set(accounted))}"
        f"\n  only grammar: {sorted(set(accounted) - set(declared))}"
    )


def test_runtime_record_vocabulary_passes_the_constitutional_exclusion_gate():
    """Event species and record coordinates cannot hide retired vocabulary."""

    violations = []
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
            for pattern, label in COMPILED:
                if pattern.search(scanned):
                    violations.append((path.name, line, label, value))

    assert violations == [], "\n" + "\n".join(
        f"{path}:{line} [{label}] {value}"
        for path, line, label, value in violations
    )


def _event_payloads():
    for path, tree in _runtime_trees():
        constants = _module_strings(tree)
        for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
            kind = None
            payload = None
            if isinstance(call.func, ast.Attribute) and call.func.attr == "append":
                if len(call.args) >= 3:
                    kind, payload = call.args[0], call.args[2]
            elif isinstance(call.func, ast.Name) and call.func.id == "Event":
                named = {item.arg: item.value for item in call.keywords}
                kind, payload = named.get("kind"), named.get("payload")
            if not isinstance(payload, ast.Dict):
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
                yield path, call.lineno, name, value, payload


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
    for _path, _line, name, value, payload in _event_payloads():
        keys = {
            key.value
            for key in payload.keys
            if isinstance(key, ast.Constant) and isinstance(key.value, str)
        }
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


def test_no_bare_standing_value_bypasses_standing_physiology():
    """A status string cannot receive the constitutional Standing coordinate."""

    required = {
        "responsibility",
        "authority",
        "evidence_scope",
        "scope_locality",
        "occurrence_preservation",
    }
    bare = []
    for path, tree in _runtime_trees():
        for node in (item for item in ast.walk(tree) if isinstance(item, ast.Dict)):
            keys = {
                key.value
                for key in node.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            }
            if "standing" in keys and not required <= keys:
                bare.append((path.name, node.lineno, sorted(keys)))

    assert bare == [], "\n" + "\n".join(
        f"{path}:{line} bare Standing beside {keys}"
        for path, line, keys in bare
    )


def test_command_implementation_receives_no_constitutional_write_capability():
    """The slash-command boundary may not hand an implementation the ledger."""

    assert "ledger" not in {field.name for field in fields(OperatorCommandContext)}


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

    monkeypatch.setattr("seed_runtime.operator_material_command.os.lstat", record_crossing)
    run_persistent_operator_console(
        ledger=EventLedger(),
        workspace_id="w",
        locality_id="l",
        input_stream=BytesIO(b"/material " + os.fsencode(material) + b"\n"),
        output_stream=StringIO(),
    )

    assert crossed == []


def test_filesystem_read_reconstructs_the_complete_act_and_yield_physiology(tmp_path):
    """Any Seed-owned read must carry the machine grammar's exact Act road."""

    material = tmp_path / "book.bin"
    material.write_bytes(b"book bytes")
    ledger = EventLedger()
    run_persistent_operator_console(
        ledger=ledger,
        workspace_id="w",
        locality_id="l",
        input_stream=BytesIO(b"/material " + os.fsencode(material) + b"\n"),
        output_stream=StringIO(),
        material_command=OperatorMaterialCommand(),
    )
    read = next(event for event in ledger.list("w") if event.kind == MATERIAL_TARGET_READ_KIND)
    occurrence = read.payload.get("act_occurrence_id")

    assert isinstance(occurrence, str) and occurrence
    evidence = [
        event
        for event in ledger.list("w")
        if event.payload.get("act_occurrence_id") == occurrence
        and event.payload.get("act")
        and event.payload.get("responsibility")
        and event.payload.get("responsible_boundary")
    ]
    yielded = [
        event
        for event in ledger.list("w")
        if event.payload.get("dimensions", {}).get("act_occurrence_id") == occurrence
        and event.payload.get("yield_commitment")
    ]
    assert evidence
    assert yielded
    assert read.payload.get("yield_evidence_id") == yielded[0].id


def test_checkpoint_names_the_representation_it_addresses_not_an_emission():
    wording = inspect.getdoc(open_operator_checkpoint) or ""

    assert "exact Representation addressed by the command" in wording
    assert "exact emission addressed by the command" not in wording
