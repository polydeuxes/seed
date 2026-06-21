"""Read-only architecture conformance audit."""

from __future__ import annotations

from collections import Counter
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.operational_graph import OperationalGraph, build_operational_graph

Classification = Literal[
    "aligned", "drift", "underspecified", "obsolete_design", "emergent_structure", "unknown"
]
RealizationAssessment = Literal["directly_realized", "indirectly_realized", "partially_realized", "not_observed", "unknown"]
Significance = Literal[
    "architectural_concept",
    "operational_structure",
    "workflow_structure",
    "visibility_structure",
    "schema_detail",
    "observation_detail",
    "leaf_node",
    "unknown",
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
ARCHITECTURAL_CONCEPTS: frozenset[str] = frozenset(
    {
        "action plan",
        "approval",
        "authorization",
        "capability",
        "operational graph",
        "ownership",
        "pressure",
        "privilege",
        "projection",
    }
)
SCHEMA_DETAIL_TERMS: frozenset[str] = frozenset(
    {
        "address assignment method",
        "cpu count",
        "kernel version",
        "mount options",
        "user uid",
    }
)
WORKFLOW_TERMS: frozenset[str] = frozenset(
    {"consumer", "emitter", "event", "approval", "action plan"}
)
VISIBILITY_TERMS: frozenset[str] = frozenset(
    {"audit", "diagnostic", "observation", "operational graph", "surface", "view"}
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
class ConceptRealization:
    concept: str
    assessment: RealizationAssessment
    realizations: tuple[OperationalEvidence, ...]
    supporting_evidence: tuple[str, ...]
    reason: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "concept": self.concept,
            "assessment": self.assessment,
            "realizations": [e.to_json_dict() for e in self.realizations],
            "supporting_evidence": list(self.supporting_evidence),
            "reason": self.reason,
        }

@dataclass(frozen=True)
class ArchitectureConformanceFinding:
    subject: str
    classification: Classification
    significance: Significance
    architecture_evidence: tuple[ArchitectureEvidence, ...]
    operational_evidence: tuple[OperationalEvidence, ...]
    reason: str

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "classification": self.classification,
            "significance": self.significance,
            "architecture_evidence": [e.to_json_dict() for e in self.architecture_evidence],
            "operational_evidence": [e.to_json_dict() for e in self.operational_evidence],
            "reason": self.reason,
        }

@dataclass(frozen=True)
class ArchitectureConformanceAudit:
    findings: tuple[ArchitectureConformanceFinding, ...]
    concept_realizations: tuple[ConceptRealization, ...]
    metadata: dict[str, Any]

    @property
    def summary(self) -> dict[str, Any]:
        return {
            "findings": len(self.findings),
            "classifications": dict(sorted(Counter(f.classification for f in self.findings).items())),
            "significance": dict(sorted(Counter(f.significance for f in self.findings).items())),
            "architecturally_significant": sum(
                1
                for f in self.findings
                if f.significance
                in {"architectural_concept", "operational_structure", "workflow_structure", "visibility_structure"}
            ),
            "schema_detail_findings": sum(
                1 for f in self.findings if f.significance in {"schema_detail", "observation_detail", "leaf_node"}
            ),
            "concept_realizations": len(self.concept_realizations),
            "realization_assessments": dict(sorted(Counter(r.assessment for r in self.concept_realizations).items())),
            **self.metadata,
        }

    def to_json_dict(self) -> dict[str, Any]:
        return {"summary": self.summary, "findings": [f.to_json_dict() for f in self.findings], "concept_realizations": [r.to_json_dict() for r in self.concept_realizations], "metadata": dict(self.metadata)}


def build_architecture_conformance_audit(root: str | Path | None = None, *, architecture_evidence: tuple[ArchitectureEvidence, ...] | None = None, graph: OperationalGraph | None = None) -> ArchitectureConformanceAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    arch = architecture_evidence if architecture_evidence is not None else discover_architecture_evidence(repo_root)
    op_graph = graph if graph is not None else build_operational_graph(repo_root)
    operational = _operational_evidence(op_graph)
    realizations = _concept_realizations(arch, operational)
    subjects = sorted({e.subject for e in arch} | {e.subject for e in operational})
    findings = tuple(
        sorted(
            (
                _finding(
                    subject,
                    tuple(e for e in arch if e.subject == subject),
                    tuple(e for e in operational if e.subject == subject),
                )
                for subject in subjects
            ),
            key=_finding_sort_key,
        )
    )
    return ArchitectureConformanceAudit(findings, realizations, {"read_only": True, "writes_event_ledger": False, "mutates_cluster": False, "records_diagnostics": False})


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
    significance = audit.summary["significance"]
    lines.append("Significance:")
    lines.extend([f"  {k}: {v}" for k, v in significance.items()] if significance else ["  none"])
    lines.extend(
        [
            "Significance groups:",
            f"  architecturally significant: {audit.summary['architecturally_significant']}",
            f"  schema/detail findings: {audit.summary['schema_detail_findings']}",
        ]
    )
    if audit.concept_realizations:
        lines.extend(["", "Concept Realizations:"])
        for item in audit.concept_realizations:
            lines.extend(["", f"Concept: {item.concept}", f"Assessment: {item.assessment}", f"Reason: {item.reason}", "Operational realizations:"])
            lines.extend([f"  {e.subject} — {e.source}: {e.detail} ({e.confidence})" for e in item.realizations] or ["  none"])
            lines.append("Supporting evidence:")
            lines.extend([f"  {e}" for e in item.supporting_evidence] or ["  none"])
    if not audit.findings:
        lines.extend(["", "No architecture or operational evidence was discovered."])
        return "\n".join(lines)
    for f in audit.findings:
        lines.extend(["", f"Subject: {f.subject}", f"Classification: {f.classification}", f"Significance: {f.significance}", f"Reason: {f.reason}", "Architecture evidence:"])
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


def _concept_realizations(arch: tuple[ArchitectureEvidence, ...], operational: tuple[OperationalEvidence, ...]) -> tuple[ConceptRealization, ...]:
    concepts = sorted({e.subject for e in arch})
    return tuple(_concept_realization(concept, tuple(e for e in operational if _realizes(concept, e))) for concept in concepts)


def _concept_realization(concept: str, matches: tuple[OperationalEvidence, ...]) -> ConceptRealization:
    if not matches:
        return ConceptRealization(concept, "not_observed", (), (), "No operational structure was found with direct or lexical evidence for this architecture concept.")
    direct = tuple(e for e in matches if e.subject == concept)
    if direct and all(e.confidence != "low" for e in direct):
        return ConceptRealization(concept, "directly_realized", direct, _support(direct), "Operational vocabulary contains the architecture concept directly.")
    if all(e.confidence == "low" for e in matches):
        return ConceptRealization(concept, "unknown", matches, _support(matches), "Only low-confidence operational evidence is available for this architecture concept.")
    full_token = tuple(e for e in matches if _concept_tokens(concept) <= _concept_tokens(e.subject + " " + e.detail))
    if full_token:
        return ConceptRealization(concept, "indirectly_realized", full_token, _support(full_token), "The architecture term is absent as a node, but implementation-backed operational structures carry the same concept vocabulary.")
    return ConceptRealization(concept, "partially_realized", matches, _support(matches), "Operational evidence overlaps the architecture concept, but does not cover the full concept vocabulary.")


def _realizes(concept: str, evidence: OperationalEvidence) -> bool:
    concept_tokens = _concept_tokens(concept)
    evidence_tokens = _concept_tokens(evidence.subject + " " + evidence.detail)
    return bool(concept_tokens & evidence_tokens)


def _concept_tokens(value: str) -> set[str]:
    tokens = set()
    for token in re.findall(r"[a-z0-9]+", _normalize(value)):
        if token in {"node", "classified", "as", "concrete", "aggregate", "relationship", "relationships", "observed"}:
            continue
        if token.endswith("ies") and len(token) > 4:
            token = token[:-3] + "y"
        elif token.endswith("s") and len(token) > 3:
            token = token[:-1]
        tokens.add(token)
    return tokens


def _support(evidence: tuple[OperationalEvidence, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(f"{e.source}: {e.detail}" for e in evidence))


def _finding(subject: str, arch: tuple[ArchitectureEvidence, ...], operational: tuple[OperationalEvidence, ...]) -> ArchitectureConformanceFinding:
    significance = _significance(subject, arch, operational)
    if arch and operational:
        if any(e.confidence == "low" for e in operational):
            return ArchitectureConformanceFinding(subject, "unknown", significance, arch, operational, "Architecture and operation are both present, but operational evidence is low-confidence or indirect.")
        if _conflict(subject, arch, operational):
            return ArchitectureConformanceFinding(subject, "drift", significance, arch, operational, "Architecture and operational evidence use conflicting relationship vocabulary for this subject.")
        return ArchitectureConformanceFinding(subject, "aligned", significance, arch, operational, "Architecture and operational graph both contain evidence for this subject.")
    if operational:
        classification: Classification = "emergent_structure" if len(operational) > 1 else "underspecified"
        reason = _missing_architecture_reason(classification, significance)
        return ArchitectureConformanceFinding(subject, classification, significance, arch, operational, reason)
    return ArchitectureConformanceFinding(subject, "obsolete_design", significance, arch, operational, "Architecture describes this subject, but the operational graph did not observe it.")


def _missing_architecture_reason(classification: Classification, significance: Significance) -> str:
    if significance in {"schema_detail", "observation_detail", "leaf_node"}:
        return "Operational graph shows a schema, catalog, observation, or leaf detail that architecture is not expected to enumerate exhaustively."
    if classification == "emergent_structure":
        return "Operational graph shows recurring structure without architecture evidence."
    return "Operational graph shows an architecturally relevant structure without architecture evidence."


def _significance(subject: str, arch: tuple[ArchitectureEvidence, ...], operational: tuple[OperationalEvidence, ...]) -> Significance:
    if subject in ARCHITECTURAL_CONCEPTS:
        return "architectural_concept"
    if subject in SCHEMA_DETAIL_TERMS:
        return "schema_detail"
    if subject in WORKFLOW_TERMS:
        return "workflow_structure"
    if subject in VISIBILITY_TERMS:
        return "visibility_structure"
    op_text = " ".join(e.detail.lower() for e in operational)
    if "observation_predicate" in op_text or "observation predicate" in op_text:
        return "observation_detail"
    if any(token in subject for token in (" uid", " count", " version", " options", " method")):
        return "schema_detail"
    if arch and operational:
        return "operational_structure"
    if operational:
        if len(operational) > 1:
            return "operational_structure"
        return "leaf_node"
    return "unknown"


def _finding_sort_key(finding: ArchitectureConformanceFinding) -> tuple[int, str, str]:
    rank = {
        "architectural_concept": 0,
        "operational_structure": 1,
        "workflow_structure": 2,
        "visibility_structure": 3,
        "unknown": 4,
        "schema_detail": 5,
        "observation_detail": 6,
        "leaf_node": 7,
    }
    return (rank[finding.significance], finding.classification, finding.subject)


def _conflict(subject: str, arch: tuple[ArchitectureEvidence, ...], operational: tuple[OperationalEvidence, ...]) -> bool:
    arch_text = " ".join(e.detail.lower() for e in arch)
    op_text = " ".join(e.detail.lower() for e in operational)
    return subject in {"projection", "view"} and "relationship" in op_text and "view" in arch_text


def _normalize(value: str) -> str:
    value = value.lower().replace("_", " ").replace("-", " ")
    aliases = {"projections": "projection", "views": "view", "read models": "read model", "diagnostics": "diagnostic", "audits": "audit", "events": "event", "capabilities": "capability", "observations": "observation", "surfaces": "surface", "emits": "emitter", "consumes": "consumer"}
    return aliases.get(value.strip(), value.strip())
