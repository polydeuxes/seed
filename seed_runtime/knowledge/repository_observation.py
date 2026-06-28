"""Deterministic repository artifact extraction helpers.

This module intentionally works only on caller-provided Python source text. It
never reads files, scans repositories, imports modules, uses LLMs, reconciles
claims, or integrates with runtime/tool execution.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass

from seed_runtime.knowledge.self_model_alignment import RepositoryArtifactFact
from seed_runtime.structure_observation import STRUCTURE_OBSERVATION_OWNER


@dataclass(frozen=True)
class RepositoryArtifactObservationAdapterBoundary:
    """Implementation-local adapter boundary for Python repository artifacts."""

    parent_owner: str = STRUCTURE_OBSERVATION_OWNER
    adapter_owner: str = "Repository Artifact Observation Adapter"
    read_only: bool = True
    structural_extraction: bool = True
    preserves_evidence: bool = True
    python_parsing: bool = True
    module_observation: bool = True
    class_observation: bool = True
    function_observation: bool = True
    method_observation: bool = True
    repository_artifact_record_construction: bool = True
    interprets_content: bool = False
    owns_responsibility_recovery: bool = False
    owns_lexicon: bool = False
    writes_event_ledger: bool = False
    mutates_repository: bool = False
    mutates_cluster: bool = False


REPOSITORY_ARTIFACT_OBSERVATION_ADAPTER_BOUNDARY = (
    RepositoryArtifactObservationAdapterBoundary()
)


class RepositoryArtifactObservationAdapter:
    """Observe Python repository artifact structure from caller-provided text."""

    boundary = REPOSITORY_ARTIFACT_OBSERVATION_ADAPTER_BOUNDARY

    def extract(
        self,
        source_path: str,
        text: str,
    ) -> list[RepositoryArtifactFact]:
        """Extract structural artifact facts from caller-provided Python source text.

        Extraction is intentionally tiny and deterministic. It always emits a module
        fact for ``source_path`` and, when the text parses as Python, emits facts for
        observed top-level class definitions, top-level function definitions,
        top-level async function definitions, direct class methods, and top-level
        imports. It does not read from disk or infer architecture/ownership.
        """

        facts = [_module_fact(source_path)]

        try:
            tree = ast.parse(text, filename=source_path)
        except SyntaxError:
            return [_module_fact(source_path, parse_failed=True)]

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                facts.append(_class_fact(source_path, node.name))
                facts.extend(_method_facts(source_path, node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                facts.append(_function_fact(source_path, node.name))
            elif isinstance(node, ast.Import):
                facts.extend(_import_facts(source_path, node))
            elif isinstance(node, ast.ImportFrom):
                facts.extend(_import_from_facts(source_path, node))

        return facts


def extract_repository_artifact_facts(
    source_path: str,
    text: str,
) -> list[RepositoryArtifactFact]:
    """Extract structural artifact facts using the repository artifact adapter."""

    return RepositoryArtifactObservationAdapter().extract(source_path, text)


def _module_fact(
    source_path: str,
    *,
    parse_failed: bool = False,
) -> RepositoryArtifactFact:
    fact = f"Module/file {source_path} exists."
    if parse_failed:
        fact = f"{fact} Python source could not be parsed; only the module/file fact was emitted."
    return RepositoryArtifactFact(
        fact=fact,
        artifact_kind="module",
        path=source_path,
        symbol=None,
    )


def _class_fact(source_path: str, symbol: str) -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=f"Class {symbol} exists in {source_path}.",
        artifact_kind="class",
        path=source_path,
        symbol=symbol,
    )


def _function_fact(source_path: str, symbol: str) -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=f"Function {symbol} exists in {source_path}.",
        artifact_kind="function",
        path=source_path,
        symbol=symbol,
    )


def _method_fact(
    source_path: str,
    *,
    class_symbol: str,
    method_symbol: str,
) -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=f"Class {class_symbol} defines method {method_symbol} in {source_path}.",
        artifact_kind="method",
        path=source_path,
        symbol=method_symbol,
        parent_symbol=class_symbol,
    )


def _import_fact(source_path: str, symbol: str) -> RepositoryArtifactFact:
    return RepositoryArtifactFact(
        fact=f"Import {symbol} exists in {source_path}.",
        artifact_kind="import",
        path=source_path,
        symbol=symbol,
    )


def _method_facts(
    source_path: str,
    node: ast.ClassDef,
) -> list[RepositoryArtifactFact]:
    return [
        _method_fact(
            source_path,
            class_symbol=node.name,
            method_symbol=child.name,
        )
        for child in node.body
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def _import_facts(
    source_path: str,
    node: ast.Import,
) -> list[RepositoryArtifactFact]:
    return [_import_fact(source_path, alias.name) for alias in node.names]


def _import_from_facts(
    source_path: str,
    node: ast.ImportFrom,
) -> list[RepositoryArtifactFact]:
    module = _import_from_module(node)
    return [
        _import_fact(source_path, _join_import_symbol(module, alias.name))
        for alias in node.names
    ]


def _import_from_module(node: ast.ImportFrom) -> str:
    relative_prefix = "." * node.level
    return f"{relative_prefix}{node.module or ''}"


def _join_import_symbol(module: str, name: str) -> str:
    if not module:
        return name
    return f"{module}.{name}"
