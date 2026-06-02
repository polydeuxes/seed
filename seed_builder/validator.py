"""Validation checks for untrusted toolkit candidates."""

from __future__ import annotations

import ast
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from seed_runtime.registry import ManifestError, load_toolkit_manifest
from seed_runtime.schema import validate_schema_value

FORBIDDEN_IMPORTS = {"os", "subprocess", "socket", "shutil", "pathlib"}


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    message: str


@dataclass(frozen=True)
class ValidationReport:
    candidate_id: str
    checks: list[CheckResult]

    @property
    def ok(self) -> bool:
        return all(check.ok for check in self.checks)


class ToolkitValidator:
    def __init__(self, *, test_timeout_seconds: float = 10.0) -> None:
        self.test_timeout_seconds = test_timeout_seconds

    def validate(self, candidate_id: str, artifact_path: str | Path) -> ValidationReport:
        path = Path(artifact_path)
        checks = [
            self._check_manifest(path),
            self._check_schemas(path),
            self._check_implementation_refs(path),
            self._check_forbidden_imports(path),
            self._run_candidate_tests(path),
        ]
        return ValidationReport(candidate_id=candidate_id, checks=checks)

    def _check_manifest(self, path: Path) -> CheckResult:
        try:
            load_toolkit_manifest(path / "toolkit.yaml")
        except (ManifestError, FileNotFoundError, ValueError) as exc:
            return CheckResult("manifest", False, str(exc))
        return CheckResult("manifest", True, "manifest is loadable")

    def _check_schemas(self, path: Path) -> CheckResult:
        try:
            toolkit = load_toolkit_manifest(path / "toolkit.yaml")
            for tool in toolkit.tools:
                validate_schema_value(tool.input_schema, self._example_for(tool.input_schema))
                validate_schema_value(tool.output_schema, self._example_for(tool.output_schema))
        except (ManifestError, ValueError) as exc:
            return CheckResult("schemas", False, str(exc))
        return CheckResult("schemas", True, "schemas accept generated examples")

    def _check_implementation_refs(self, path: Path) -> CheckResult:
        try:
            toolkit = load_toolkit_manifest(path / "toolkit.yaml")
        except (ManifestError, FileNotFoundError, ValueError) as exc:
            return CheckResult("implementation_refs", False, str(exc))
        for tool in toolkit.tools:
            if ":" not in tool.implementation:
                return CheckResult("implementation_refs", False, f"{tool.name} implementation is not module:function")
            module_name, function_name = tool.implementation.split(":", 1)
            module_path = path / f"{module_name.replace('.', '/')}.py"
            if not module_path.exists():
                return CheckResult("implementation_refs", False, f"{module_path.name} missing")
            try:
                tree = ast.parse(module_path.read_text())
            except SyntaxError as exc:
                return CheckResult("implementation_refs", False, f"{module_path.name} has invalid Python: {exc.msg}")
            if not any(isinstance(node, ast.FunctionDef) and node.name == function_name for node in tree.body):
                return CheckResult("implementation_refs", False, f"{function_name} missing in {module_path.name}")
        return CheckResult("implementation_refs", True, "implementation references resolve")

    def _check_forbidden_imports(self, path: Path) -> CheckResult:
        for py_file in path.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError as exc:
                return CheckResult("forbidden_imports", False, f"{py_file.name} has invalid Python: {exc.msg}")
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = {alias.name.split(".")[0] for alias in node.names}
                elif isinstance(node, ast.ImportFrom):
                    names = {str(node.module).split(".")[0]}
                else:
                    continue
                forbidden = names & FORBIDDEN_IMPORTS
                if forbidden:
                    return CheckResult("forbidden_imports", False, f"{py_file.name} imports {sorted(forbidden)}")
        return CheckResult("forbidden_imports", True, "no forbidden imports")

    def _run_candidate_tests(self, path: Path) -> CheckResult:
        tests_dir = path / "tests"
        if not tests_dir.exists():
            return CheckResult("tests", False, "tests directory missing")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", str(tests_dir)],
                cwd=path,
                text=True,
                capture_output=True,
                timeout=self.test_timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            return CheckResult("tests", False, f"candidate tests timed out after {exc.timeout} seconds")
        if proc.returncode != 0:
            return CheckResult("tests", False, proc.stdout + proc.stderr)
        return CheckResult("tests", True, proc.stdout.strip())

    def _example_for(self, schema: dict) -> object:
        schema_type = schema.get("type")
        if schema_type == "object":
            return {key: self._example_for(subschema) for key, subschema in schema.get("properties", {}).items() if key in schema.get("required", [])}
        if schema_type == "string":
            return "example"
        if schema_type == "boolean":
            return True
        if schema_type == "integer":
            return 1
        if schema_type == "number":
            return 1.0
        if schema_type == "array":
            return []
        return None
