"""Implementation-backed operational relationship graph."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.consumer_dependency_audit import CONSUMER_PATHS, build_consumer_audit
from seed_runtime.emitter_consumer_audit import build_emitter_consumer_audit

EvidenceKind = Literal["direct", "indirect", "reference"]
Confidence = Literal["high", "medium", "low"]


@dataclass(frozen=True)
class OperationalGraphNode:
    id: str
    type: str
    label: str

    def to_json_dict(self) -> dict[str, Any]:
        return {"id": self.id, "type": self.type, "label": self.label}


@dataclass(frozen=True)
class OperationalGraphEvidence:
    kind: EvidenceKind
    source: str
    detail: str

    def to_json_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "source": self.source, "detail": self.detail}


@dataclass(frozen=True)
class OperationalGraphEdge:
    source: str
    target: str
    type: str
    evidence: tuple[OperationalGraphEvidence, ...]
    confidence: Confidence

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "evidence": [item.to_json_dict() for item in self.evidence],
            "confidence": self.confidence,
        }


@dataclass(frozen=True)
class OperationalGraph:
    nodes: tuple[OperationalGraphNode, ...]
    edges: tuple[OperationalGraphEdge, ...]
    metadata: dict[str, Any]

    @property
    def summary(self) -> dict[str, Any]:
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "relationship_types": dict(Counter(edge.type for edge in self.edges)),
            "confidence_counts": dict(Counter(edge.confidence for edge in self.edges)),
        }

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "nodes": [node.to_json_dict() for node in self.nodes],
            "edges": [edge.to_json_dict() for edge in self.edges],
            "metadata": dict(self.metadata),
        }


def build_operational_graph(root: str | Path | None = None) -> OperationalGraph:
    """Build a normalized graph from existing implementation-backed audits."""

    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    nodes: dict[str, OperationalGraphNode] = {}
    edges: dict[tuple[str, str, str], OperationalGraphEdge] = {}

    def node(kind: str, label: str) -> str:
        node_id = f"{kind}:{label}"
        nodes.setdefault(node_id, OperationalGraphNode(node_id, kind, label))
        return node_id

    def add_edge(
        source: str,
        target: str,
        edge_type: str,
        evidence: tuple[OperationalGraphEvidence, ...],
        confidence: Confidence,
    ) -> None:
        if not evidence:
            return
        key = (source, target, edge_type)
        current = edges.get(key)
        if current is None:
            edges[key] = OperationalGraphEdge(
                source, target, edge_type, evidence, confidence
            )
            return
        merged_evidence = tuple(dict.fromkeys([*current.evidence, *evidence]))
        edges[key] = OperationalGraphEdge(
            source,
            target,
            edge_type,
            merged_evidence,
            _stronger(current.confidence, confidence),
        )

    emitter_audit = build_emitter_consumer_audit(repo_root)
    for item in emitter_audit.items:
        emitter_id = node("emitter", item.emitter)
        for event_name in item.emits:
            event_id = node("event", event_name)
            direct = tuple(
                OperationalGraphEvidence("direct", source, "event emission literal")
                for source in item.evidence
            )
            add_edge(emitter_id, event_id, "emits", direct, "high")
            for consumer in item.consumers:
                consumer_id = node("surface", consumer)
                add_edge(
                    event_id,
                    consumer_id,
                    "consumes",
                    (
                        OperationalGraphEvidence(
                            "indirect",
                            "emitter_consumer_audit",
                            f"{consumer} consumes {event_name}",
                        ),
                    ),
                    "medium",
                )

    consumer_audit = build_consumer_audit(repo_root)
    for item in consumer_audit.items:
        for consumer in item.consumers:
            item_id = node(item.kind, item.item)
            consumer_id = node("surface", consumer)
            evidence_sources = CONSUMER_PATHS.get(consumer, ())
            evidence = tuple(
                OperationalGraphEvidence(
                    "reference",
                    source,
                    f"{consumer} source group references {item.item}",
                )
                for source in evidence_sources
            )
            add_edge(item_id, consumer_id, "consumes", evidence, "low")

    return OperationalGraph(
        nodes=tuple(sorted(nodes.values(), key=lambda item: item.id)),
        edges=tuple(
            sorted(
                edges.values(), key=lambda item: (item.source, item.type, item.target)
            )
        ),
        metadata={
            "discovery": "Composed from implementation-backed emitter/consumer and consumer dependency audits; edges without evidence are omitted.",
            "read_only": True,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        },
    )


def operational_graph_json(graph: OperationalGraph) -> dict[str, Any]:
    return graph.to_json_dict()


def format_operational_graph(graph: OperationalGraph) -> str:
    lines = [
        "Operational Graph",
        "",
        f"Nodes: {graph.summary['nodes']}",
        f"Edges: {graph.summary['edges']}",
        "",
        "Relationship types:",
    ]
    relationship_types = graph.summary["relationship_types"]
    lines.extend(
        [f"  {name}: {count}" for name, count in sorted(relationship_types.items())]
        if relationship_types
        else ["  none"]
    )
    lines.extend(["", "Confidence counts:"])
    confidence_counts = graph.summary["confidence_counts"]
    lines.extend(
        [f"  {name}: {count}" for name, count in sorted(confidence_counts.items())]
        if confidence_counts
        else ["  none"]
    )
    if not graph.edges:
        lines.extend(
            ["", "No implementation-backed operational relationships were discovered."]
        )
    return "\n".join(lines)


def _stronger(left: Confidence, right: Confidence) -> Confidence:
    order = {"low": 0, "medium": 1, "high": 2}
    return left if order[left] >= order[right] else right
