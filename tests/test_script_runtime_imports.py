from __future__ import annotations

import ast
import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def test_each_script_seed_runtime_import_resolves():
    unresolved = []
    for path in sorted(SCRIPTS.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.startswith("seed_runtime")
            ):
                continue
            try:
                module = importlib.import_module(node.module)
            except ModuleNotFoundError:
                unresolved.append((path.name, node.lineno, node.module, None))
                continue
            for name in node.names:
                if name.name == "*":
                    continue
                if not hasattr(module, name.name):
                    unresolved.append(
                        (path.name, node.lineno, node.module, name.name)
                    )

    assert unresolved == []
