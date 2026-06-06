#!/usr/bin/env python3
"""Generate Seed architecture diagrams from AST-readable ownership metadata.

This generator intentionally parses source files with ``ast`` only. It must not
import Seed runtime modules, because generated architecture docs should describe
runtime ownership without executing runtime code.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "docs" / "generated" / "architecture"
GRAPH_PATH = OUTPUT_DIR / "architecture_graph.json"
MERMAID_PATH = OUTPUT_DIR / "runtime_ownership.mmd"
DOT_PATH = OUTPUT_DIR / "runtime_ownership.dot"
BANNER = "generated; do not edit"

SOURCE_FILES = [
    Path("seed_runtime/runtime.py"),
    Path("seed_runtime/tool_needs.py"),
    Path("seed_runtime/execution.py"),
    Path("seed_runtime/registry.py"),
    Path("seed_runtime/capability_catalog.py"),
    Path("seed_runtime/state.py"),
    Path("seed_runtime/projection_store.py"),
    Path("seed_runtime/events.py"),
]

SYNTHETIC_NODES: dict[str, dict[str, str]] = {
    "ToolRecommendationService": {
        "owner": "provider_recommendation_ranking",
        "layer": "runtime_service",
        "summary": "Ranks capability provider recommendations for tool needs.",
    },
    "RegisteredOperation": {
        "owner": "registered_tool_implementation",
        "layer": "execution",
        "summary": "A registered toolkit function that ToolExecutor may execute.",
    },
    "ProviderRecommendation": {
        "owner": "capability_metadata",
        "layer": "catalog",
        "summary": "A non-executable provider suggestion from capability metadata.",
    },
    "HandoffCandidate": {
        "owner": "capability_metadata",
        "layer": "catalog",
        "summary": "A non-executable handoff or backend operation suggestion.",
    },
    "GraphValidator": {
        "owner": "state_projection_validation",
        "layer": "state",
        "summary": "Validates projected graph relationships and entity types.",
    },
    "State": {
        "owner": "projected_state_model",
        "layer": "state",
        "summary": "Inspectable current state derived from events.",
    },
}


@dataclass
class ClassScan:
    name: str
    file: str
    lineno: int
    metadata: dict[str, Any] = field(default_factory=dict)
    calls: list[dict[str, str]] = field(default_factory=list)


def main() -> None:
    scans = [scan for source in SOURCE_FILES for scan in _scan_file(REPO_ROOT / source, source)]
    graph = _build_graph(scans)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n")
    MERMAID_PATH.write_text(_render_mermaid(graph))
    DOT_PATH.write_text(_render_dot(graph))


def _scan_file(path: Path, relative_path: Path) -> list[ClassScan]:
    tree = ast.parse(path.read_text(), filename=str(relative_path))
    classes: list[ClassScan] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        metadata = _extract_seed_arch(node)
        classes.append(
            ClassScan(
                name=node.name,
                file=relative_path.as_posix(),
                lineno=node.lineno,
                metadata=metadata,
                calls=_extract_self_calls(node),
            )
        )
    return classes


def _extract_seed_arch(node: ast.ClassDef) -> dict[str, Any]:
    for stmt in node.body:
        value: ast.AST | None = None
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name) and target.id == "__seed_arch__":
                    value = stmt.value
                    break
        elif isinstance(stmt, ast.AnnAssign):
            if isinstance(stmt.target, ast.Name) and stmt.target.id == "__seed_arch__":
                value = stmt.value
        if value is not None:
            literal = ast.literal_eval(value)
            if not isinstance(literal, dict):
                raise TypeError(f"{node.name}.__seed_arch__ must be a dict")
            return literal
    return {}


def _extract_self_calls(node: ast.ClassDef) -> list[dict[str, str]]:
    calls: list[dict[str, str]] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        attr = child.func
        parts: list[str] = []
        while isinstance(attr, ast.Attribute):
            parts.append(attr.attr)
            attr = attr.value
        if isinstance(attr, ast.Name) and attr.id == "self" and parts:
            calls.append({"receiver": ".".join(reversed(parts[1:])), "method": parts[0]})
    return sorted(calls, key=lambda item: (item["receiver"], item["method"]))


def _build_graph(scans: list[ClassScan]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    for scan in scans:
        if not scan.metadata:
            continue
        nodes[scan.name] = {
            "id": scan.name,
            "kind": "class",
            "file": scan.file,
            "line": scan.lineno,
            "owner": scan.metadata.get("owner", "unspecified"),
            "layer": scan.metadata.get("layer", "unspecified"),
            "summary": scan.metadata.get("summary", ""),
            "events": list(scan.metadata.get("events", [])),
            "routes": list(scan.metadata.get("routes", [])),
            "ast_calls": scan.calls,
        }
        for edge in scan.metadata.get("edges", []):
            if "to" not in edge or "label" not in edge:
                raise ValueError(f"{scan.name} edge must include to and label: {edge!r}")
            edges.append(_normalize_edge(scan.name, edge))
        for route in scan.metadata.get("routes", []):
            if "target" not in route or "label" not in route:
                raise ValueError(f"{scan.name} route must include target and label: {route!r}")

    for edge in edges:
        for endpoint in (edge["from"], edge["to"]):
            if endpoint not in nodes:
                synthetic = SYNTHETIC_NODES.get(endpoint, {})
                nodes[endpoint] = {
                    "id": endpoint,
                    "kind": "external" if synthetic else "referenced",
                    "file": None,
                    "line": None,
                    "owner": synthetic.get("owner", "referenced"),
                    "layer": synthetic.get("layer", "referenced"),
                    "summary": synthetic.get("summary", "Referenced by architecture metadata."),
                    "events": [],
                    "routes": [],
                    "ast_calls": [],
                }

    return {
        "banner": BANNER,
        "source": "Python AST scan of selected seed_runtime files; runtime modules are not imported.",
        "sources": [path.as_posix() for path in SOURCE_FILES],
        "nodes": [nodes[key] for key in sorted(nodes)],
        "edges": sorted(_dedupe_edges(edges), key=lambda edge: (edge["from"], edge["to"], edge["label"], edge.get("path") or "")),
    }


def _normalize_edge(source: str, edge: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "from": source,
        "to": str(edge["to"]),
        "label": str(edge["label"]),
    }
    if edge.get("path") is not None:
        normalized["path"] = str(edge["path"])
    if edge.get("kind") is not None:
        normalized["kind"] = str(edge["kind"])
    return normalized


def _dedupe_edges(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str, str, str, str]] = set()
    result: list[dict[str, Any]] = []
    for edge in edges:
        key = (
            edge["from"],
            edge["to"],
            edge["label"],
            edge.get("path", ""),
            edge.get("kind", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(edge)
    return result


def _render_mermaid(graph: dict[str, Any]) -> str:
    lines = [f"%% {BANNER}", "flowchart LR"]
    for node in graph["nodes"]:
        node_id = _diagram_id(node["id"])
        label = f"{node['id']}\\nowner: {node['owner']}"
        lines.append(f"  {node_id}[\"{_escape_mermaid(label)}\"]")
    lines.append("")
    for edge in graph["edges"]:
        label = edge["label"]
        if edge.get("path"):
            label = f"{label} ({edge['path']})"
        lines.append(
            f"  {_diagram_id(edge['from'])} -->|{_escape_mermaid(label)}| {_diagram_id(edge['to'])}"
        )
    return "\n".join(lines) + "\n"


def _render_dot(graph: dict[str, Any]) -> str:
    lines = [f"// {BANNER}", "digraph runtime_ownership {", "  rankdir=LR;"]
    for node in graph["nodes"]:
        label = f"{node['id']}\\nowner: {node['owner']}"
        lines.append(f"  {_dot_id(node['id'])} [label={json.dumps(label)}];")
    for edge in graph["edges"]:
        label = edge["label"]
        if edge.get("path"):
            label = f"{label} ({edge['path']})"
        lines.append(
            f"  {_dot_id(edge['from'])} -> {_dot_id(edge['to'])} [label={json.dumps(label)}];"
        )
    lines.append("}")
    return "\n".join(lines) + "\n"


def _diagram_id(value: str) -> str:
    return re.sub(r"\W+", "_", value).strip("_")


def _dot_id(value: str) -> str:
    return json.dumps(_diagram_id(value))


def _escape_mermaid(value: str) -> str:
    return value.replace('"', "'").replace("|", "/")


if __name__ == "__main__":
    main()
