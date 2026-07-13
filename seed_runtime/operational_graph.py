"""Implementation-backed operational relationship graph."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.consumer_dependency_audit import (
    CONSUMER_PATHS,
    ConsumerAudit,
    build_consumer_audit,
)
from seed_runtime.emitter_consumer_audit import (
    EmitterConsumerAudit,
    build_emitter_consumer_audit,
)

EvidenceKind = Literal["direct", "indirect", "reference"]
Confidence = Literal["high", "medium", "low"]
NodeClassification = Literal[
    "concrete_surface",
    "aggregate_surface",
    "concrete_emitter",
    "aggregate_emitter",
    "concrete_projection",
    "aggregate_projection",
    "concrete_diagnostic",
    "aggregate_diagnostic",
    "concrete_event",
    "aggregate_event",
    "concrete_observation_predicate",
    "aggregate_observation_predicate",
    "concrete_node",
    "aggregate_node",
]

IMPORTANT_SURFACES = {
    "operational_story",
    "pressure_audit",
    "correlation_audit",
    "investigation_path",
    "capability_needs",
    "capability_candidates",
    "capability_status",
    "ownership_discrepancies",
    "diagnostics",
    "read_models",
    "views",
}


@dataclass(frozen=True)
class OperationalGraphNode:
    id: str
    type: str
    label: str
    classification: NodeClassification

    @property
    def aggregate(self) -> bool:
        return self.classification.startswith("aggregate_")

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "classification": self.classification,
            "taxonomy": "aggregate" if self.aggregate else "concrete",
            "aggregate": self.aggregate,
        }


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
        return _operational_graph_node_id(nodes, kind, label)

    def add_edge(
        source: str,
        target: str,
        edge_type: str,
        evidence: tuple[OperationalGraphEvidence, ...],
        confidence: Confidence,
    ) -> None:
        _add_operational_graph_edge(
            edges, source, target, edge_type, evidence, confidence
        )

    _compose_emitter_consumer_audit_graph(
        build_emitter_consumer_audit(repo_root), node=node, add_edge=add_edge
    )
    _compose_consumer_dependency_audit_graph(
        build_consumer_audit(repo_root), node=node, add_edge=add_edge
    )

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


def _operational_graph_node_id(
    nodes: dict[str, OperationalGraphNode], kind: str, label: str
) -> str:
    node_id = f"{kind}:{label}"
    nodes.setdefault(
        node_id,
        OperationalGraphNode(node_id, kind, label, _node_classification(kind, label)),
    )
    return node_id


def _add_operational_graph_edge(
    edges: dict[tuple[str, str, str], OperationalGraphEdge],
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
        edges[key] = OperationalGraphEdge(source, target, edge_type, evidence, confidence)
        return
    merged_evidence = tuple(dict.fromkeys([*current.evidence, *evidence]))
    edges[key] = OperationalGraphEdge(
        source,
        target,
        edge_type,
        merged_evidence,
        _stronger(current.confidence, confidence),
    )


def _compose_emitter_consumer_audit_graph(
    audit: EmitterConsumerAudit,
    *,
    node: Any,
    add_edge: Any,
) -> None:
    for item in audit.items:
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


def _compose_consumer_dependency_audit_graph(
    audit: ConsumerAudit,
    *,
    node: Any,
    add_edge: Any,
) -> None:
    for item in audit.items:
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


def operational_graph_json(graph: OperationalGraph) -> dict[str, Any]:
    return graph.to_json_dict()


def build_operational_graph_confidence(
    root: str | Path | None = None,
    confidence: Confidence | None = None,
    exclude_aggregate: bool = False,
) -> dict[str, Any]:
    """Summarize why operational graph edge confidence was assigned."""

    graph = build_operational_graph(root)
    nodes = {node.id: node for node in graph.nodes}
    graph_edges = _filter_aggregate_operational_graph_edges(
        graph.edges, nodes, exclude_aggregate=exclude_aggregate
    )
    selected = ("high", "medium", "low") if confidence is None else (confidence,)
    tiers = {
        tier: _confidence_tier_summary(tier, graph_edges, graph) for tier in selected
    }

    important_low = _important_low_confidence_edge_examples(graph_edges)
    return {
        "summary": {
            **{
                **graph.summary,
                "edges": len(graph_edges),
                "relationship_types": dict(Counter(edge.type for edge in graph_edges)),
                "confidence_counts": dict(
                    Counter(edge.confidence for edge in graph_edges)
                ),
            },
            "total_graph_edges": len(graph.edges),
            "excluded_aggregate_edges": len(graph.edges) - len(graph_edges),
            "exclude_aggregate": exclude_aggregate,
            "read_only": True,
            "writes_event_ledger": False,
            "mutates_cluster": False,
            "filtered_confidence": confidence,
        },
        "tiers": tiers,
        "taxonomy": build_operational_graph_taxonomy(root),
        "important_low_confidence_edges": important_low,
        "metadata": dict(graph.metadata),
    }


def _important_low_confidence_edge_examples(
    graph_edges: tuple[OperationalGraphEdge, ...]
) -> list[dict[str, Any]]:
    return [
        _edge_example(edge, include_importance=True)
        for edge in sorted(graph_edges, key=_edge_sort_key)
        if edge.confidence == "low" and _importance(edge)
    ][:10]


def _filter_aggregate_operational_graph_edges(
    edges: tuple[OperationalGraphEdge, ...],
    nodes: dict[str, OperationalGraphNode],
    *,
    exclude_aggregate: bool,
) -> tuple[OperationalGraphEdge, ...]:
    if not exclude_aggregate:
        return edges
    return tuple(
        edge
        for edge in edges
        if not (
            (nodes.get(edge.source) and nodes[edge.source].aggregate)
            or (nodes.get(edge.target) and nodes[edge.target].aggregate)
        )
    )


def _confidence_tier_summary(
    tier: Confidence,
    graph_edges: tuple[OperationalGraphEdge, ...],
    graph: OperationalGraph,
) -> dict[str, Any]:
    edges = [edge for edge in graph_edges if edge.confidence == tier]
    evidence_counts = Counter(item.kind for edge in edges for item in edge.evidence)
    type_counts = Counter(edge.type for edge in edges)
    return {
        "edge_count": len(edges),
        "relationship_types": dict(sorted(type_counts.items())),
        "evidence_categories": dict(sorted(evidence_counts.items())),
        "uncertainty_causes": _uncertainty_causes(edges, graph),
        "uncertainty_categories": _uncertainty_categories(edges, graph),
        "confidence_interpretation": _confidence_interpretation(edges, graph),
        "reason": _confidence_reason(tier),
        "potential_confidence_improvement": _confidence_improvement(tier),
        "representative_examples": [
            _edge_example(edge) for edge in sorted(edges, key=_edge_sort_key)[:3]
        ],
    }


def operational_graph_confidence_json(analysis: dict[str, Any]) -> dict[str, Any]:
    return analysis


def build_operational_graph_taxonomy(root: str | Path | None = None) -> dict[str, Any]:
    """Summarize operational graph node taxonomy without mutating state."""

    graph = build_operational_graph(root)
    classification_counts = Counter(node.classification for node in graph.nodes)
    type_counts = Counter(node.type for node in graph.nodes)
    degree = Counter()
    for edge in graph.edges:
        degree[edge.source] += 1
        degree[edge.target] += 1
    aggregate_nodes = [node for node in graph.nodes if node.aggregate]
    return {
        "summary": {
            "nodes": len(graph.nodes),
            "aggregate_nodes": len(aggregate_nodes),
            "concrete_nodes": len(graph.nodes) - len(aggregate_nodes),
            "edges": len(graph.edges),
            "read_only": True,
            "writes_event_ledger": False,
            "mutates_cluster": False,
        },
        "node_types": dict(sorted(type_counts.items())),
        "classifications": dict(sorted(classification_counts.items())),
        "aggregate_connectivity": [
            {
                "id": node.id,
                "type": node.type,
                "label": node.label,
                "classification": node.classification,
                "degree": degree[node.id],
            }
            for node in sorted(
                aggregate_nodes, key=lambda item: (-degree[item.id], item.id)
            )
        ],
        "metadata": dict(graph.metadata),
    }


def operational_graph_taxonomy_json(analysis: dict[str, Any]) -> dict[str, Any]:
    return analysis


def format_operational_graph_taxonomy(analysis: dict[str, Any]) -> str:
    lines = [
        "Operational Graph Taxonomy",
        "",
        f"Nodes: {analysis['summary']['nodes']}",
        f"Aggregate nodes: {analysis['summary']['aggregate_nodes']}",
        f"Concrete nodes: {analysis['summary']['concrete_nodes']}",
        "",
        "Node classifications:",
    ]
    lines.extend(_count_lines(analysis["classifications"]))
    lines.extend(["", "Aggregate nodes by connectivity:"])
    aggregate = analysis["aggregate_connectivity"][:10]
    if aggregate:
        for node in aggregate:
            lines.append(f"  {node['id']} ({node['classification']}): {node['degree']}")
    else:
        lines.append("  none")
    return "\n".join(lines)


def format_operational_graph_confidence(analysis: dict[str, Any]) -> str:
    lines = ["Operational Graph Confidence", ""]
    if not analysis["summary"]["edges"]:
        return "\n".join(
            [
                *lines,
                "No implementation-backed operational relationships were discovered.",
            ]
        )
    for tier in ("high", "medium", "low"):
        data = analysis["tiers"].get(tier)
        if data is None:
            continue
        lines.extend(
            [
                f"{tier.title()} Confidence",
                "",
                f"Edges: {data['edge_count']}",
                "Relationship types:",
            ]
        )
        lines.extend(_count_lines(data["relationship_types"]))
        lines.append("Common evidence:")
        lines.extend(_count_lines(data["evidence_categories"]))
        lines.append("Uncertainty causes:")
        lines.extend(_count_lines(data.get("uncertainty_causes", {})))
        interpretation = data.get("confidence_interpretation", {})
        lines.append("Caused primarily by:")
        lines.append(
            f"  aggregate targets: {interpretation.get('aggregate_target_edges', 0)}"
        )
        lines.append("Operational relationship uncertainty:")
        lines.append(
            f"  {interpretation.get('operational_relationship_uncertainty_edges', 0)}"
        )
        lines.append("Uncertainty categories:")
        lines.extend(_count_lines(data.get("uncertainty_categories", {})))
        lines.extend(
            [
                f"Reason: {data['reason']}",
                "Potential confidence improvement: "
                f"{data['potential_confidence_improvement']}",
                "Representative examples:",
            ]
        )
        examples = data["representative_examples"]
        if examples:
            for example in examples:
                lines.append(
                    f"  {example['source']} -> {example['target']} ({example['type']})"
                )
                lines.append(
                    f"    evidence: {', '.join(example['evidence_categories'])}"
                )
        else:
            lines.append("  none")
        lines.append("")

    important = analysis["important_low_confidence_edges"]
    lines.append("Operationally relevant low-confidence edges:")
    if important:
        for example in important:
            lines.append(
                f"  {example['source']} -> {example['target']} ({example['type']})"
            )
            lines.append(f"    importance: {', '.join(example['importance'])}")
    else:
        lines.append("  none")
    return "\n".join(lines).rstrip()


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


def _node_classification(kind: str, label: str) -> NodeClassification:
    if kind == "surface":
        return (
            "aggregate_surface" if _is_aggregate_surface(label) else "concrete_surface"
        )
    if kind == "emitter":
        return "concrete_emitter"
    if kind == "diagnostic":
        return "concrete_diagnostic"
    if kind == "event":
        return "concrete_event"
    if kind == "observation_predicate":
        return "concrete_observation_predicate"
    if "projection" in kind or label in {
        "projection_builders",
        "projection builders",
        "read_models",
        "read models",
        "state_build",
    }:
        return (
            "aggregate_projection"
            if _is_aggregate_surface(label)
            else "concrete_projection"
        )
    return "aggregate_node" if _is_aggregate_surface(label) else "concrete_node"


def _is_aggregate_surface(label: str) -> bool:
    return label in {
        *CONSUMER_PATHS.keys(),
        "projection builders",
        "read models",
        "diagnostics and audits",
        "CLI surfaces",
    }


def _uncertainty_causes(
    edges: list[OperationalGraphEdge], graph: OperationalGraph
) -> dict[str, int]:
    nodes = {node.id: node for node in graph.nodes}
    counts: Counter[str] = Counter()
    for edge in edges:
        if nodes.get(edge.target) and nodes[edge.target].aggregate:
            counts["aggregate_target"] += 1
        if nodes.get(edge.source) and nodes[edge.source].aggregate:
            counts["aggregate_source"] += 1
        kinds = {item.kind for item in edge.evidence}
        if kinds == {"reference"}:
            counts["reference_only_evidence"] += 1
        if kinds == {"indirect"}:
            counts["indirect_only_discovery"] += 1
        if not any(item.source and ":" in item.source for item in edge.evidence):
            counts["missing_line_attribution"] += 1
    return dict(sorted(counts.items()))


def _uncertainty_categories(
    edges: list[OperationalGraphEdge], graph: OperationalGraph
) -> dict[str, int]:
    nodes = {node.id: node for node in graph.nodes}
    counts: Counter[str] = Counter()
    for edge in edges:
        source = nodes.get(edge.source)
        target = nodes.get(edge.target)
        has_aggregate_endpoint = bool(
            (source and source.aggregate) or (target and target.aggregate)
        )
        kinds = {item.kind for item in edge.evidence}
        if has_aggregate_endpoint:
            counts["taxonomy_uncertainty"] += 1
        elif edge.confidence == "low" or kinds == {"indirect"}:
            counts["relationship_uncertainty"] += 1
        if not any(item.source and ":" in item.source for item in edge.evidence):
            counts["attribution_uncertainty"] += 1
        if kinds == {"reference"}:
            counts["reference_only_uncertainty"] += 1
    return dict(sorted(counts.items()))


def _confidence_interpretation(
    edges: list[OperationalGraphEdge], graph: OperationalGraph
) -> dict[str, int]:
    nodes = {node.id: node for node in graph.nodes}
    aggregate_target_edges = 0
    aggregate_endpoint_edges = 0
    relationship_uncertainty_edges = 0
    for edge in edges:
        source = nodes.get(edge.source)
        target = nodes.get(edge.target)
        has_aggregate_endpoint = bool(
            (source and source.aggregate) or (target and target.aggregate)
        )
        if target and target.aggregate:
            aggregate_target_edges += 1
        if has_aggregate_endpoint:
            aggregate_endpoint_edges += 1
        elif edge.confidence == "low":
            relationship_uncertainty_edges += 1
    return {
        "aggregate_target_edges": aggregate_target_edges,
        "aggregate_endpoint_edges": aggregate_endpoint_edges,
        "operational_relationship_uncertainty_edges": relationship_uncertainty_edges,
    }


def _stronger(left: Confidence, right: Confidence) -> Confidence:
    order = {"low": 0, "medium": 1, "high": 2}
    return left if order[left] >= order[right] else right


def _confidence_reason(tier: str) -> str:
    return {
        "high": "relationship has direct emitter evidence",
        "medium": "relationship has indirect helper evidence",
        "low": "relationship is inferred from reference-only or consumer-only evidence",
    }[tier]


def _confidence_improvement(tier: str) -> str:
    return {
        "high": "already directly supported; corroborating consumers may improve resilience",
        "medium": "discover direct consumer or emitter evidence for this relationship",
        "low": "direct emitter evidence or bidirectional implementation evidence not yet discovered",
    }[tier]


def _edge_sort_key(edge: OperationalGraphEdge) -> tuple[str, str, str]:
    return (edge.source, edge.type, edge.target)


def _edge_example(
    edge: OperationalGraphEdge, include_importance: bool = False
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source": edge.source,
        "target": edge.target,
        "type": edge.type,
        "confidence": edge.confidence,
        "evidence_categories": sorted({item.kind for item in edge.evidence}),
        "evidence": [item.to_json_dict() for item in edge.evidence[:3]],
        "reason": _confidence_reason(edge.confidence),
        "potential_confidence_improvement": _confidence_improvement(edge.confidence),
    }
    if include_importance:
        result["importance"] = _importance(edge)
    return result


def _importance(edge: OperationalGraphEdge) -> list[str]:
    labels = {
        edge.source.removeprefix("surface:"),
        edge.target.removeprefix("surface:"),
    }
    return sorted(surface for surface in IMPORTANT_SURFACES if surface in labels)


def _count_lines(counts: dict[str, int]) -> list[str]:
    return (
        [f"  {name}: {count}" for name, count in counts.items()]
        if counts
        else ["  none"]
    )
