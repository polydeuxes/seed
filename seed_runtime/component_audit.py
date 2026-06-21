"""Read-only component role audit built from repository visibility evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.architecture_conformance_audit import ARCHITECTURE_PATHS
from seed_runtime.consumer_dependency_audit import build_consumer_audit
from seed_runtime.operational_graph import build_operational_graph

ComponentStatus = Literal[
    "active", "dormant", "unreachable", "partially_consumed", "superseded", "unknown"
]

_BOUNDARY = {"read_only": True, "writes_event_ledger": False, "mutates_cluster": False}
_SCAN_SUFFIXES = {".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json"}
_SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache"}


@dataclass(frozen=True)
class ComponentAudit:
    component: str
    status: ComponentStatus
    definitions: tuple[str, ...]
    references: tuple[str, ...]
    tests: tuple[str, ...]
    consumers: tuple[str, ...]
    operational_graph: dict[str, Any]
    architecture_evidence: tuple[str, ...]
    overlap: tuple[str, ...]
    evidence: tuple[str, ...]
    unresolved_questions: tuple[str, ...]
    boundary: dict[str, bool]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "component": self.component,
            "status": self.status,
            "definitions": list(self.definitions),
            "references": list(self.references),
            "tests": list(self.tests),
            "consumers": list(self.consumers),
            "operational_graph": self.operational_graph,
            "architecture_evidence": list(self.architecture_evidence),
            "overlap": list(self.overlap),
            "evidence": list(self.evidence),
            "unresolved_questions": list(self.unresolved_questions),
            "boundary": dict(self.boundary),
        }


def build_component_audit(component: str, root: str | Path | None = None) -> ComponentAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    needle = component.strip()
    lowered = needle.lower()
    aliases = _component_aliases(lowered)
    files = list(_iter_files(repo_root))
    references = tuple(_relative(repo_root, p) for p in files if any(_contains(p, alias) for alias in aliases))
    tests = tuple(path for path in references if path.startswith("tests/"))
    definitions = tuple(
        path
        for path in references
        if not path.startswith("tests/")
        and any(_definition_like(repo_root / path, alias) for alias in aliases)
    )
    consumers = _consumers(needle, repo_root)
    operational_graph = _operational_graph_evidence(needle, repo_root)
    architecture_evidence = tuple(
        path for path in references if path in ARCHITECTURE_PATHS or path.startswith("docs/")
    )
    overlap = _overlap(lowered, references)
    evidence = _status_evidence(definitions, references, tests, consumers, operational_graph, architecture_evidence)
    status = _classify(definitions, tests, consumers, operational_graph, references)
    unresolved = _unresolved(status, consumers, operational_graph)
    return ComponentAudit(
        component=needle,
        status=status,
        definitions=definitions,
        references=references,
        tests=tests,
        consumers=consumers,
        operational_graph=operational_graph,
        architecture_evidence=architecture_evidence,
        overlap=overlap,
        evidence=evidence,
        unresolved_questions=unresolved,
        boundary=dict(_BOUNDARY),
    )


def component_audit_json(audit: ComponentAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_component_audit(audit: ComponentAudit) -> str:
    lines = ["Component Audit", "", "Component:", f"  {audit.component}", "", "Status:", f"  {audit.status}"]
    for title, values in (
        ("Definitions", audit.definitions), ("References", audit.references), ("Tests", audit.tests),
        ("Consumers", audit.consumers), ("Architecture Evidence", audit.architecture_evidence),
        ("Possible Overlap", audit.overlap), ("Evidence", audit.evidence),
    ):
        lines.extend(["", f"{title}:"])
        lines.extend([f"  {v}" for v in values] or ["  none found"])
    lines.extend(["", "Operational Graph:"])
    if audit.operational_graph.get("observed"):
        lines.append(f"  observed ({audit.operational_graph.get('match_count')} matches)")
        lines.extend(f"  {m}" for m in audit.operational_graph.get("matches", []))
    else:
        lines.append("  not observed")
    lines.extend([
        "", "Boundary:",
        "  read-only; no lifecycle decision made",
        "  writes_event_ledger=false",
        "  mutates_cluster=false",
        "", "Unresolved Questions:",
    ])
    lines.extend([f"  {q}" for q in audit.unresolved_questions] or ["  none"])
    return "\n".join(lines)


def _component_aliases(lowered: str) -> tuple[str, ...]:
    aliases = {lowered}
    if lowered.endswith("_selector"):
        aliases.add(lowered.removesuffix("_selector") + "_selection")
    if lowered.endswith("_selection"):
        aliases.add(lowered.removesuffix("_selection") + "_selector")
    return tuple(sorted(aliases))


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in _SCAN_SUFFIXES:
            yield path


def _contains(path: Path, lowered: str) -> bool:
    try:
        return lowered in path.read_text(encoding="utf-8").lower() or lowered in path.name.lower()
    except UnicodeDecodeError:
        return False


def _definition_like(path: Path, lowered: str) -> bool:
    name = path.stem.lower()
    if lowered in name or lowered.replace("_", "-") in path.name.lower():
        return True
    if path.suffix != ".py":
        return False
    text = path.read_text(encoding="utf-8").lower()
    return f"def {lowered}" in text or f"class {lowered}" in text


def _consumers(component: str, root: Path) -> tuple[str, ...]:
    audit = build_consumer_audit(root, diagnostic_filter=component)
    found = []
    for item in audit.items:
        if item.item == component:
            found.extend(item.consumers)
    return tuple(sorted(set(found)))


def _operational_graph_evidence(component: str, root: Path) -> dict[str, Any]:
    graph = build_operational_graph(root)
    lowered = component.lower()
    matches = []
    for node in graph.nodes:
        if lowered in node.id.lower() or lowered in node.label.lower():
            matches.append(f"node {node.id}")
    for edge in graph.edges:
        text = " ".join([edge.source, edge.target, edge.type, *(e.detail for e in edge.evidence)])
        if lowered in text.lower():
            matches.append(f"edge {edge.source} -> {edge.target} ({edge.type})")
    return {"observed": bool(matches), "match_count": len(matches), "matches": matches[:20]}


def _overlap(lowered: str, references: tuple[str, ...]) -> tuple[str, ...]:
    terms = {"selection_path", "reference_selection", "reasoning_path", "context_selection"}
    return tuple(sorted(t for t in terms if t != lowered and any(t in r for r in references)))


def _classify(defs, tests, consumers, graph, refs) -> ComponentStatus:
    if defs and consumers and tests:
        return "active"
    if defs and graph.get("observed") and (tests or consumers):
        return "active"
    if defs and (tests or consumers or graph.get("observed")):
        return "partially_consumed"
    if defs and refs:
        return "dormant"
    if defs:
        return "unreachable"
    return "unknown"


def _status_evidence(defs, refs, tests, consumers, graph, arch) -> tuple[str, ...]:
    return tuple(x for x in (
        f"definitions_found={len(defs)}", f"references_found={len(refs)}", f"tests_found={len(tests)}",
        f"consumers_found={len(consumers)}", f"operational_graph_observed={str(bool(graph.get('observed'))).lower()}",
        f"architecture_evidence_found={len(arch)}",
    ))


def _unresolved(status, consumers, graph) -> tuple[str, ...]:
    questions = []
    if not consumers:
        questions.append("Does any current runtime path consume this component?")
    if not graph.get("observed"):
        questions.append("Should this component appear in operational graph evidence, or is absence expected?")
    if status == "unknown":
        questions.append("Is the requested component name the repository's implementation name?")
    return tuple(questions)


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()
