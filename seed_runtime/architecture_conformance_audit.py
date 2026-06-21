"""Read-only architecture conformance audit."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.operational_graph import OperationalGraph, build_operational_graph

Classification = Literal[
    "aligned", "drift", "underspecified", "obsolete_design", "emergent_structure", "unknown"
]

ARCHITECTURE_TERMS: tuple[str, ...] = (
    "projection", "projections", "view", "views", "read model", "read models",
    "diagnostic", "diagnostics", "audit", "audits", "event", "events",
    "capability", "capabilities", "ownership", "observation", "observations",
    "authorization", "approval", "consumer", "emitter", "surface", "surfaces",
)
ARCHITECTURE_PATHS: tuple[str, ...] = (
    "seed.md", "docs/index.md", "docs/architectural_knowledge_map.md", "docs/README.md"
)

@dataclass(frozen=True)
class ArchitectureEvidence:
    subject: str
    source: str
    detail: str
    confidence: str = "reference"

    def to_json_dict(self) -> dict[str, str]:
        return {"subject": self.subject, "source": self.source, "detail": self.detail, "confidence": self.confidence}

@dataclass(frozen=True)
class OperationalEvidence:
    subject: str
    source: str
    detail: str
    confidence: str

    def to_json_dict(self) -> dict[str, str]:
        return {"subject": self.subject, "source": self.source, "detail": self.detail, "confidence": self.confidence}

@dataclass(frozen=True)
class ArchitectureConformanceFinding:
    subject: str
    classification: Classification
    architecture_evidence: tuple[ArchitectureEvidence, ...]
    operational_evidence: tuple[OperationalEvidence, ...]
    reason: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "classification": self.classification,
            "architecture_evidence": [e.to_json_dict() for e in self.architecture_evidence],
            "operational_evidence": [e.to_json_dict() for e in self.operational_evidence],
            "reason": self.reason,
        }

@dataclass(frozen=True)
class ArchitectureConformanceAudit:
    findings: tuple[ArchitectureConformanceFinding, ...]
    metadata: dict[str, Any]

    @property
    def summary(self) -> dict[str, Any]:
        return {"findings": len(self.findings), "classifications": dict(sorted(Counter(f.classification for f in self.findings).items())), **self.metadata}

    def to_json_dict(self) -> dict[str, Any]:
        return {"summary": self.summary, "findings": [f.to_json_dict() for f in self.findings], "metadata": dict(self.metadata)}


def build_architecture_conformance_audit(root: str | Path | None = None, *, architecture_evidence: tuple[ArchitectureEvidence, ...] | None = None, graph: OperationalGraph | None = None) -> ArchitectureConformanceAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    arch = architecture_evidence if architecture_evidence is not None else discover_architecture_evidence(repo_root)
    op_graph = graph if graph is not None else build_operational_graph(repo_root)
    operational = _operational_evidence(op_graph)
    subjects = sorted({e.subject for e in arch} | {e.subject for e in operational})
    findings = tuple(_finding(subject, tuple(e for e in arch if e.subject == subject), tuple(e for e in operational if e.subject == subject)) for subject in subjects)
    return ArchitectureConformanceAudit(findings, {"read_only": True, "writes_event_ledger": False, "mutates_cluster": False, "records_diagnostics": False})


def architecture_conformance_audit_json(audit: ArchitectureConformanceAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def discover_architecture_evidence(root: Path) -> tuple[ArchitectureEvidence, ...]:
    evidence: list[ArchitectureEvidence] = []
    for rel in ARCHITECTURE_PATHS:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        for term in ARCHITECTURE_TERMS:
            if term in lower:
                evidence.append(ArchitectureEvidence(_normalize(term), rel, f"architecture reference mentions {term!r}"))
    return tuple(sorted({(e.subject, e.source, e.detail): e for e in evidence}.values(), key=lambda e: (e.subject, e.source)))


def format_architecture_conformance_audit(audit: ArchitectureConformanceAudit) -> str:
    lines = ["Architecture Conformance Audit", "", f"Findings: {len(audit.findings)}", "Classifications:"]
    counts = audit.summary["classifications"]
    lines.extend([f"  {k}: {v}" for k, v in counts.items()] if counts else ["  none"])
    if not audit.findings:
        lines.extend(["", "No architecture or operational evidence was discovered."])
        return "\n".join(lines)
    for f in audit.findings:
        lines.extend(["", f"Subject: {f.subject}", f"Classification: {f.classification}", f"Reason: {f.reason}", "Architecture evidence:"])
        lines.extend([f"  {e.source}: {e.detail}" for e in f.architecture_evidence] or ["  none"])
        lines.append("Operational evidence:")
        lines.extend([f"  {e.source}: {e.detail} ({e.confidence})" for e in f.operational_evidence] or ["  none"])
    return "\n".join(lines)


def _operational_evidence(graph: OperationalGraph) -> tuple[OperationalEvidence, ...]:
    items: list[OperationalEvidence] = []
    for node in graph.nodes:
        subject = _normalize(node.label if node.type not in {"event"} else node.type)
        items.append(OperationalEvidence(subject, "operational_graph", f"node {node.id} classified as {node.classification}", "high" if not node.aggregate else "medium"))
    edge_counts = Counter(edge.type for edge in graph.edges)
    for edge_type, count in edge_counts.items():
        items.append(OperationalEvidence(_normalize(edge_type), "operational_graph", f"{count} {edge_type!r} relationships observed", "high"))
    return tuple(items)


def _finding(subject: str, arch: tuple[ArchitectureEvidence, ...], operational: tuple[OperationalEvidence, ...]) -> ArchitectureConformanceFinding:
    if arch and operational:
        if any(e.confidence == "low" for e in operational):
            return ArchitectureConformanceFinding(subject, "unknown", arch, operational, "Architecture and operation are both present, but operational evidence is low-confidence or indirect.")
        if _conflict(subject, arch, operational):
            return ArchitectureConformanceFinding(subject, "drift", arch, operational, "Architecture and operational evidence use conflicting relationship vocabulary for this subject.")
        return ArchitectureConformanceFinding(subject, "aligned", arch, operational, "Architecture and operational graph both contain evidence for this subject.")
    if operational:
        classification: Classification = "emergent_structure" if len(operational) > 1 else "underspecified"
        reason = "Operational graph shows recurring structure without architecture evidence." if classification == "emergent_structure" else "Operational graph shows behavior without architecture evidence."
        return ArchitectureConformanceFinding(subject, classification, arch, operational, reason)
    return ArchitectureConformanceFinding(subject, "obsolete_design", arch, operational, "Architecture describes this subject, but the operational graph did not observe it.")


def _conflict(subject: str, arch: tuple[ArchitectureEvidence, ...], operational: tuple[OperationalEvidence, ...]) -> bool:
    arch_text = " ".join(e.detail.lower() for e in arch)
    op_text = " ".join(e.detail.lower() for e in operational)
    return subject in {"projection", "view"} and "relationship" in op_text and "view" in arch_text


def _normalize(value: str) -> str:
    value = value.lower().replace("_", " ").replace("-", " ")
    aliases = {"projections": "projection", "views": "view", "read models": "read model", "diagnostics": "diagnostic", "audits": "audit", "events": "event", "capabilities": "capability", "observations": "observation", "surfaces": "surface", "emits": "emitter", "consumes": "consumer"}
    return aliases.get(value.strip(), value.strip())
