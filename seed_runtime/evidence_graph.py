"""Read-only Evidence Graph projection helpers.

The Evidence Graph is derived from projected :class:`seed_runtime.state.State`.
It never reads the event ledger, appends events, executes runtime behavior, calls
providers, evaluates policy, executes tools, or persists a separate evidence DB.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

from seed_runtime.evidence import Evidence
from seed_runtime.facts import Fact, FactSupport
from seed_runtime.state import State

EvidenceType = Literal[
    "user_input",
    "runtime_decision",
    "tool_result",
    "observation",
    "projection",
    "unknown",
]
EvidenceRelationship = Literal["supports", "contradicts", "mentions", "derived_from"]
EvidenceGraphReferenceStanding = Literal[
    "unresolved_evidence_reference", "derivation_reference"
]

EVIDENCE_TYPES: frozenset[str] = frozenset(
    {
        "user_input",
        "runtime_decision",
        "tool_result",
        "observation",
        "projection",
        "unknown",
    }
)
EVIDENCE_RELATIONSHIPS: frozenset[str] = frozenset(
    {"supports", "contradicts", "mentions", "derived_from"}
)


@dataclass(frozen=True)
class EvidenceNode:
    evidence_id: str
    evidence_type: EvidenceType
    summary: str
    source_event_id: str | None
    source_run_id: str | None
    confidence: float
    created_at: datetime | None


@dataclass(frozen=True)
class EvidenceLink:
    source_evidence_id: str
    target_fact_id: str
    relationship: EvidenceRelationship
    strength: float


@dataclass(frozen=True)
class EvidenceGraphReference:
    reference_id: str
    standing: EvidenceGraphReferenceStanding
    summary: str
    referencing_fact_id: str | None = None
    source_fact_id: str | None = None


@dataclass(frozen=True)
class FactEvidenceView:
    fact_id: str
    subject: str
    predicate: str
    object: Any
    confidence: float
    evidence: list[EvidenceNode] = field(default_factory=list)
    represented_graph_references: list[EvidenceGraphReference] = field(
        default_factory=list
    )
    supporting_event_ids: list[str] = field(default_factory=list)
    explanation: str = ""


@dataclass(frozen=True)
class EvidenceGraph:
    evidence_nodes: list[EvidenceNode] = field(default_factory=list)
    evidence_links: list[EvidenceLink] = field(default_factory=list)
    fact_evidence: list[FactEvidenceView] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceSummary:
    evidence_count: int
    linked_fact_count: int
    unsupported_fact_count: int
    average_confidence: float
    last_event_id: str | None
    projection_version: str


def build_evidence_graph(state: State) -> EvidenceGraph:
    """Build a deterministic read-only evidence graph from projected State."""

    nodes_by_id: dict[str, EvidenceNode] = {}
    links_by_key: dict[tuple[str, str, str], EvidenceLink] = {}
    views: list[FactEvidenceView] = []

    for fact in _ordered_facts(state):
        fact_nodes, fact_references = _evidence_graph_material_for_fact(state, fact)
        for node in fact_nodes:
            nodes_by_id.setdefault(node.evidence_id, node)
            links_by_key.setdefault(
                (node.evidence_id, fact.id, "supports"),
                EvidenceLink(
                    source_evidence_id=node.evidence_id,
                    target_fact_id=fact.id,
                    relationship="supports",
                    strength=_link_strength(fact, node),
                ),
            )
        views.append(_fact_view(fact, fact_nodes, fact_references))

    return EvidenceGraph(
        evidence_nodes=sorted(nodes_by_id.values(), key=_node_key),
        evidence_links=sorted(links_by_key.values(), key=_link_key),
        fact_evidence=views,
    )


def build_fact_evidence_view(state: State, fact_id: str) -> FactEvidenceView | None:
    """Return one fact evidence view by fact id without mutating State."""

    fact = state.facts.get(fact_id)
    if fact is None:
        return None
    nodes, references = _evidence_graph_material_for_fact(state, fact)
    return _fact_view(fact, nodes, references)


def build_evidence_summary(state: State) -> EvidenceSummary:
    """Return aggregate counts for the read-only Evidence Graph projection."""

    graph = build_evidence_graph(state)
    linked_fact_ids = {link.target_fact_id for link in graph.evidence_links}
    unsupported = [view for view in graph.fact_evidence if not view.evidence]
    average = (
        round(
            sum(node.confidence for node in graph.evidence_nodes)
            / len(graph.evidence_nodes),
            6,
        )
        if graph.evidence_nodes
        else 0.0
    )
    return EvidenceSummary(
        evidence_count=len(graph.evidence_nodes),
        linked_fact_count=len(linked_fact_ids),
        unsupported_fact_count=len(unsupported),
        average_confidence=average,
        last_event_id=state.last_event_id,
        projection_version=state.projection_version,
    )


def find_evidence_graph_material_for_fact(
    state: State, subject: str, predicate: str, object: Any | None = None
) -> list[FactEvidenceView]:
    """Find Evidence Graph fact views matching a subject/predicate/object query."""

    matches = []
    for view in build_evidence_graph(state).fact_evidence:
        if view.subject != subject or view.predicate != predicate:
            continue
        if object is not None and _stable_value(view.object) != _stable_value(object):
            continue
        matches.append(view)
    return matches


def unsupported_fact_views(state: State) -> list[FactEvidenceView]:
    """Return deterministic fact views that have no supporting evidence."""

    return [
        view for view in build_evidence_graph(state).fact_evidence if not view.evidence
    ]


def _evidence_graph_material_for_fact(
    state: State, fact: Fact
) -> tuple[list[EvidenceNode], list[EvidenceGraphReference]]:
    nodes: dict[str, EvidenceNode] = {}
    references: dict[tuple[str, str, str | None, str | None], EvidenceGraphReference] = {}

    def add_fact_material(material_fact: Fact) -> None:
        for evidence_id in material_fact.evidence_ids:
            evidence = state.evidence.get(evidence_id)
            if evidence is not None:
                nodes.setdefault(evidence.id, _node_from_evidence(evidence))
            else:
                reference = _unresolved_reference(material_fact, evidence_id)
                references.setdefault(
                    (
                        reference.standing,
                        reference.reference_id,
                        reference.referencing_fact_id,
                        reference.source_fact_id,
                    ),
                    reference,
                )

    add_fact_material(fact)
    if not fact.evidence_ids and fact.source_fact_id:
        reference = EvidenceGraphReference(
            reference_id=fact.source_fact_id,
            standing="derivation_reference",
            summary=f"derived from source fact {fact.source_fact_id}",
            referencing_fact_id=fact.id,
            source_fact_id=fact.source_fact_id,
        )
        references.setdefault(
            (
                reference.standing,
                reference.reference_id,
                reference.referencing_fact_id,
                reference.source_fact_id,
            ),
            reference,
        )

    for support in _supports_for_fact(state, fact):
        for supporting_fact_id in support.supporting_fact_ids:
            supporting_fact = state.facts.get(supporting_fact_id)
            if supporting_fact is None:
                continue
            add_fact_material(supporting_fact)
            if (
                not supporting_fact.evidence_ids
                and supporting_fact.id == fact.id
                and fact.source_fact_id
            ):
                reference = EvidenceGraphReference(
                    reference_id=fact.source_fact_id,
                    standing="derivation_reference",
                    summary=f"derived from source fact {fact.source_fact_id}",
                    referencing_fact_id=fact.id,
                    source_fact_id=fact.source_fact_id,
                )
                references.setdefault(
                    (
                        reference.standing,
                        reference.reference_id,
                        reference.referencing_fact_id,
                        reference.source_fact_id,
                    ),
                    reference,
                )

    return sorted(nodes.values(), key=_node_key), sorted(
        references.values(), key=_reference_key
    )


def _supports_for_fact(state: State, fact: Fact) -> list[FactSupport]:
    return [
        support
        for support in state.fact_supports
        if fact.id in support.supporting_fact_ids
        or (
            support.subject == fact.subject_id
            and support.predicate == fact.predicate
            and _stable_value(support.value) == _stable_value(fact.value)
            and support.dimensions == fact.dimensions
        )
    ]


def _node_from_evidence(evidence: Evidence) -> EvidenceNode:
    return EvidenceNode(
        evidence_id=evidence.id,
        evidence_type=_evidence_type(evidence),
        summary=_evidence_summary(evidence),
        source_event_id=_source_event_id(evidence),
        source_run_id=_source_run_id(evidence),
        confidence=evidence.confidence,
        created_at=evidence.observed_at,
    )


def _unresolved_reference(fact: Fact, evidence_id: str) -> EvidenceGraphReference:
    return EvidenceGraphReference(
        reference_id=evidence_id,
        standing="unresolved_evidence_reference",
        summary=f"unresolved evidence reference for {fact.subject_id} {fact.predicate} {_stable_value(fact.value)}",
        referencing_fact_id=fact.id,
    )


def _fact_view(
    fact: Fact, nodes: list[EvidenceNode], references: list[EvidenceGraphReference]
) -> FactEvidenceView:
    supporting_ids = sorted(
        {
            item
            for node in nodes
            for item in [node.source_event_id, node.evidence_id]
            if item
        }
    )
    return FactEvidenceView(
        fact_id=fact.id,
        subject=fact.subject_id,
        predicate=fact.predicate,
        object=fact.value,
        confidence=fact.confidence,
        evidence=nodes,
        represented_graph_references=references,
        supporting_event_ids=supporting_ids,
        explanation=_explanation(fact, nodes, references),
    )


def _explanation(
    fact: Fact, nodes: list[EvidenceNode], references: list[EvidenceGraphReference]
) -> str:
    if not nodes:
        if references:
            return (
                "Seed has this fact in projected State with represented references, "
                "but no resolved supporting evidence is linked."
            )
        return "Seed has this fact in projected State, but no supporting evidence is linked."
    type_counts: dict[str, int] = {}
    for node in nodes:
        type_counts[node.evidence_type] = type_counts.get(node.evidence_type, 0) + 1
    types = ", ".join(f"{count} {kind}" for kind, count in sorted(type_counts.items()))
    return (
        f"Seed believes this fact because it is supported by {len(nodes)} evidence "
        f"record{'s' if len(nodes) != 1 else ''} ({types})."
    )


def _evidence_type(evidence: Evidence) -> EvidenceType:
    kind = evidence.kind.lower()
    source = evidence.source.lower()
    if kind == "observation" or source.startswith("observation:"):
        return "observation"
    if kind in {"tool_result", "tool", "tool_call"} or source.startswith("tool:"):
        return "tool_result"
    if kind in {"runtime_decision", "decision"}:
        return "runtime_decision"
    if kind in {"projection", "inference"}:
        return "projection"
    if kind in {"user_input", "user"} or source.startswith("user"):
        return "user_input"
    return "unknown"


def _source_type_to_evidence_type(source_type: str) -> EvidenceType:
    if source_type == "user":
        return "user_input"
    if source_type == "provider":
        return "tool_result"
    if source_type == "discovery":
        return "observation"
    if source_type == "inferred":
        return "projection"
    return "unknown"


def _evidence_summary(evidence: Evidence) -> str:
    payload = evidence.payload
    if all(key in payload for key in ("subject", "predicate", "value")):
        return f"{payload['subject']} {payload['predicate']} {_stable_value(payload['value'])}"
    if "summary" in payload:
        return str(payload["summary"])
    if "tool_name" in payload:
        return f"tool result from {payload['tool_name']}"
    return f"{evidence.kind} from {evidence.source}"


def _source_event_id(evidence: Evidence) -> str | None:
    for key in ("source_event_id", "event_id", "observation_id", "decision_event_id"):
        value = evidence.payload.get(key)
        if value:
            return str(value)
    return evidence.id


def _source_run_id(evidence: Evidence) -> str | None:
    for key in ("source_run_id", "run_id", "runtime_run_id"):
        value = evidence.payload.get(key)
        if value:
            return str(value)
    return None


def _link_strength(fact: Fact, node: EvidenceNode) -> float:
    return round(min(float(fact.confidence), float(node.confidence)), 6)


def _ordered_facts(state: State) -> list[Fact]:
    return sorted(
        state.facts.values(),
        key=lambda fact: (
            fact.subject_id,
            fact.predicate,
            _stable_value(fact.value),
            fact.id,
        ),
    )


def _node_key(node: EvidenceNode) -> tuple[str, str]:
    return (node.evidence_type, node.evidence_id)


def _reference_key(reference: EvidenceGraphReference) -> tuple[str, str, str, str]:
    return (
        reference.standing,
        reference.reference_id,
        reference.referencing_fact_id or "",
        reference.source_fact_id or "",
    )


def _link_key(link: EvidenceLink) -> tuple[str, str, str]:
    return (link.target_fact_id, link.relationship, link.source_evidence_id)


def _stable_value(value: Any) -> str:
    if isinstance(value, (dict, list, tuple)):
        import json

        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)
