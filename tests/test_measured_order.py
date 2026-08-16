from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_seed_measurements_preserve_observed_order_without_sorting():
    violations: list[tuple[str, int, str]] = []
    for directory in (ROOT / "seed_runtime", ROOT / "scripts"):
        for path in directory.glob("*.py"):
            tree = ast.parse(path.read_bytes(), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if isinstance(node.func, ast.Name) and node.func.id == "sorted":
                    violations.append(
                        (path.relative_to(ROOT).as_posix(), node.lineno, "sorted")
                    )
                if isinstance(node.func, ast.Attribute) and node.func.attr == "sort":
                    violations.append(
                        (path.relative_to(ROOT).as_posix(), node.lineno, "sort")
                    )

    assert violations == []
