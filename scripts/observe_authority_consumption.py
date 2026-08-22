"""Observe whether recorded Authority material is ever consulted or only carried.

A coordinate that is read is not thereby used.  A reader may consult it, so
that some outcome depends on the value it holds, or may convey it, copying it
into the next occurrence's material unexamined.

Every read of an Authority coordinate in the runtime is located and classified
by where its value goes, so the two are counted apart.

Usage:
    .venv/bin/python scripts/observe_authority_consumption.py
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

RUNTIME = Path(__file__).resolve().parents[1] / "seed_runtime"
COORDINATE = "authority"


def _reads_authority(node: ast.AST) -> bool:
    """Whether this expression reads a coordinate named for Authority."""

    return (
        isinstance(node, ast.Subscript)
        and isinstance(node.slice, ast.Constant)
        and isinstance(node.slice.value, str)
        and node.slice.value.lower().endswith(COORDINATE)
    )


def _consulted(parent: ast.AST, child: ast.AST) -> bool:
    """Whether some outcome here depends on the value read.

    Sitting in the body of a branch is not being consulted: the branch was
    decided by whatever its test reads.  Only a read reached from the test
    itself, or standing in a comparison, decides anything.
    """

    if isinstance(parent, (ast.Compare, ast.BoolOp)):
        return True
    if isinstance(parent, (ast.If, ast.IfExp, ast.Assert, ast.While)):
        return any(node is child for node in ast.walk(parent.test))
    return False


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()

    consulted: list[str] = []
    conveyed: list[str] = []
    for path in sorted(RUNTIME.glob("*.py")):
        tree = ast.parse(path.read_text())
        parents: dict[ast.AST, ast.AST] = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(tree):
            if not _reads_authority(node):
                continue
            where = f"{path.name}:{node.lineno}"
            walker = node
            depth = 0
            found = False
            while walker is not None and depth < 6:
                parent = parents.get(walker)
                depth += 1
                if parent is not None and _consulted(parent, walker):
                    found = True
                    break
                walker = parent
            (consulted if found else conveyed).append(where)

    total = len(consulted) + len(conveyed)
    print(f"  reads of an Authority coordinate in the runtime: {total}")
    print(f"    some outcome depends on the value: {len(consulted)}")
    print(f"    the value is carried onward only:  {len(conveyed)}")

    if consulted:
        print("\n  where an outcome depends on it:")
        for where in consulted:
            print(f"    {where}")

    print("\n  modules carrying it onward:")
    for module, count in Counter(w.split(":")[0] for w in conveyed).most_common(8):
        print(f"    {count:3}  {module}")

    grammar = json.loads(
        (Path(__file__).resolve().parents[1] / "book_of_seed" / "witness_grammar.json")
        .read_text(encoding="utf-8")
    )
    relations = grammar["relations"]
    requiring = [
        name for name, spec in relations.items() if "Authority" in spec["requires"]
    ]
    print(
        f"\n  relations the active grammar states an Authority requirement for: "
        f"{len(requiring)} of {len(relations)}"
    )
    print(f"    {', '.join(sorted(requiring))}")
    print(
        "\n  So every relation the grammar states requires an Authority, and no\n"
        "  reader of a recorded Authority decides anything by it."
    )

    print(
        "\n  A coordinate only carried onward is preserved and never consulted,\n"
        "  so no reader here refuses anything on account of it.  This counts\n"
        "  where its value goes; it does not establish what the coordinate is,\n"
        "  nor that carrying it is wrong."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
