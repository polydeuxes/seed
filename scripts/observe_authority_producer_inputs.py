"""Observe what each Authority producer's value answers to.

Three producers take an input, so they were held apart from the context-free
ones to be varied at that input rather than at their source.  Before varying
anything, the question is what each input is: a coordinate of some recorded
occurrence, or a name the module already holds.

Each producer's call sites are read for what they supply.  A producer taking a
parameter that every caller fills with a module constant answers to no
occurrence, whatever its signature suggests.

One frame is followed and no more.  Where that leaves a local unresolved, the
remainder was traced by reading, and is written here as read rather than
measured so it can be checked:

    byte_measurement
        _source_assertion_authority(source) returns
        source.material["dimensions"]["authority"].  It carries an Authority
        already recorded on another occurrence forward rather than producing
        one, so what it answers to is whatever produced that occurrence.

Read with the source-side census, no producer found here takes its value from a
coordinate of the occurrence it is recorded on. The current findings are
emitted by this observer rather than frozen into its description.

Usage:
    .venv/bin/python scripts/observe_authority_producer_inputs.py
"""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

RUNTIME = Path(__file__).resolve().parents[1] / "seed_runtime"


def _supplied(node: ast.expr) -> str:
    """What one call site supplies for a parameter."""

    if isinstance(node, ast.Constant):
        return "a literal"
    if isinstance(node, ast.Name):
        return "a module name" if node.id.isupper() else f"a local {node.id}"
    if isinstance(node, ast.Attribute):
        return "an attribute"
    if isinstance(node, ast.Subscript):
        return "a coordinate read from material"
    if isinstance(node, ast.Call):
        return f"a call, {ast.unparse(node.func)}"
    return type(node).__name__


def _one_frame(module: str, local: str) -> list[str]:
    """What callers supply for a parameter of this exact name, one frame up.

    This follows one frame and no further.  A local that is not a parameter of
    the function it appears in is reported as unfollowed rather than guessed at.
    """

    tree = ast.parse((RUNTIME / module).read_text())
    holders = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and local
        in [a.arg for a in node.args.args] + [a.arg for a in node.args.kwonlyargs]
    ]
    if not holders:
        return ["not a parameter here, unfollowed"]
    supplied = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
        if name not in holders:
            continue
        for keyword in node.keywords:
            if keyword.arg == local:
                supplied.append(_supplied(keyword.value))
    return sorted(set(supplied)) or ["no caller supplies it by name, unfollowed"]


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    producers: dict[tuple[str, str], list[str]] = {}
    calls: dict[tuple[str, str], list[list[str]]] = {}
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and "authority" in node.name.lower():
                producers[(path.name, node.name)] = [
                    argument.arg for argument in node.args.args
                ] + [argument.arg for argument in node.args.kwonlyargs]
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if not name or "authority" not in name.lower():
                continue
            key = (path.name, name)
            if key in producers:
                calls.setdefault(key, []).append(
                    [_supplied(argument) for argument in node.args]
                )

    print("  every Authority producer, and what its callers supply:\n")
    for key in sorted(producers):
        module, name = key
        parameters = producers[key]
        sites = calls.get(key, [])
        if not parameters:
            reading = "takes nothing"
        elif not sites:
            reading = "no call site found in the runtime"
        else:
            supplied = {tuple(site) for site in sites}
            if any("material" in item for site in supplied for item in site):
                reading = "answers to a coordinate read from material"
            elif any(item.startswith("a local") for site in supplied for item in site):
                reading = "a local is supplied; followed one frame below"
            else:
                reading = "every caller supplies a module name or a literal"
        print(f"    {module}")
        print(f"      {name}({', '.join(parameters) or ''})")
        print(f"      {len(sites)} call sites, {reading}")
        for site in sites:
            print(f"        supplied: {', '.join(site)}")
        for site in sites:
            for item in site:
                if not item.startswith("a local "):
                    continue
                local = item.split("a local ", 1)[1]
                for onward in _one_frame(module, local):
                    print(f"        {local} <- {onward}")
    print(
        "\n  A producer whose every caller supplies a name the module already\n"
        "  holds answers to no occurrence, whatever its signature permits.  This\n"
        "  reads call sites; it does not say what a value ought to answer to."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
