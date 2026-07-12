"""Explanatory attribution audit for emitted event visibility."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.emitter_consumer_audit import (
    EmitterConsumerAudit,
    EmitterConsumerItem,
    EmissionType,
    build_emitter_consumer_audit,
    _emitter_name,
    _python_files,
)

AttributionStatus = Literal[
    "attributed", "dynamic", "indirect", "discovery_gap", "missing", "unknown"
]
AttributionConfidence = Literal["high", "medium", "low", "none"]
EvidenceCategory = Literal[
    "direct_emitter",
    "event_constructor",
    "indirect_emitter",
    "projection_consumer",
    "diagnostic_reference",
    "inventory_reference",
    "test_reference",
    "string_reference",
    "unknown_reference",
]

WORKFLOW_PREFIXES = (
    "action_plan.",
    "pending_action.",
    "approval.",
    "execution_proposal.",
    "tool.",
)


@dataclass(frozen=True)
class ClassifiedEvidence:
    category: EvidenceCategory
    location: str

    def to_json_dict(self) -> dict[str, str]:
        return {"category": self.category, "location": self.location}


@dataclass(frozen=True)
class EmitterAttributionImplementationEvidence:
    literal_references: dict[str, tuple[ClassifiedEvidence, ...]]
    dynamic_event_construction: tuple[ClassifiedEvidence, ...]


@dataclass(frozen=True)
class UnknownEmitterAttribution:
    status: AttributionStatus
    reason: str
    emitter: str
    confidence: AttributionConfidence
    attribution_evidence: tuple[ClassifiedEvidence, ...]
    supporting_references: tuple[ClassifiedEvidence, ...]


@dataclass(frozen=True)
class EmitterAttributionItem:
    event: str
    emitter: str
    status: AttributionStatus
    reason: str
    consumers: tuple[str, ...]
    evidence: tuple[str, ...] = ()
    emission_type: EmissionType = "domain_emission"
    confidence: AttributionConfidence = "none"
    attribution_evidence: tuple[ClassifiedEvidence, ...] = ()
    supporting_references: tuple[ClassifiedEvidence, ...] = ()

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "event": self.event,
            "emitter": self.emitter,
            "status": self.status,
            "reason": self.reason,
            "consumers": list(self.consumers),
            "evidence": list(self.evidence),
            "emission_type": self.emission_type,
            "confidence": self.confidence,
            "attribution_evidence": [
                e.to_json_dict() for e in self.attribution_evidence
            ],
            "supporting_references": [
                e.to_json_dict() for e in self.supporting_references
            ],
        }


@dataclass(frozen=True)
class EmitterAttributionAudit:
    items: tuple[EmitterAttributionItem, ...]
    metadata: dict[str, Any]

    @property
    def summary(self) -> dict[str, int]:
        return {
            "items_scanned": len(self.items),
            "attributed": sum(i.status == "attributed" for i in self.items),
            "dynamic": sum(i.status == "dynamic" for i in self.items),
            "indirect": sum(i.status == "indirect" for i in self.items),
            "discovery_gap": sum(i.status == "discovery_gap" for i in self.items),
            "missing": sum(i.status == "missing" for i in self.items),
            "unknown": sum(i.status == "unknown" for i in self.items),
        }

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "items": [i.to_json_dict() for i in self.items],
            "metadata": dict(self.metadata),
        }


def build_emitter_attribution_audit(
    root: str | Path | None = None,
    *,
    include_rendered: bool = False,
) -> EmitterAttributionAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    base = build_emitter_consumer_audit(repo_root, include_rendered=include_rendered)
    implementation_evidence = _collect_emitter_attribution_implementation_evidence(repo_root)
    literal_refs = implementation_evidence.literal_references
    dynamic_refs = implementation_evidence.dynamic_event_construction
    items: list[EmitterAttributionItem] = []
    for item in base.items:
        known_emitter_rows = _known_emitter_attributed_rows(item)
        if known_emitter_rows:
            items.extend(known_emitter_rows)
            continue
        for event in item.emits:
            refs = literal_refs.get(event, ())
            attribution = _classify_unknown_emitter_attribution(
                event, refs, dynamic_refs
            )
            items.append(
                EmitterAttributionItem(
                    event=event,
                    emitter=attribution.emitter,
                    status=attribution.status,
                    reason=attribution.reason,
                    consumers=item.consumers,
                    evidence=tuple(e.location for e in attribution.attribution_evidence)
                    + tuple(e.location for e in attribution.supporting_references),
                    emission_type=item.emission_type,
                    confidence=attribution.confidence,
                    attribution_evidence=attribution.attribution_evidence,
                    supporting_references=attribution.supporting_references,
                )
            )
    return EmitterAttributionAudit(
        items=tuple(sorted(items, key=lambda i: (i.status, i.event))),
        metadata={
            "discovery": "Refines emitter/consumer audit rows with AST literal references, dynamic Event/append calls, and workflow-prefix visibility hints.",
            "include_rendered": include_rendered,
            "scope": list(base.metadata.get("scope", [])),
        },
    )


def _known_emitter_attributed_rows(
    item: EmitterConsumerItem,
) -> tuple[EmitterAttributionItem, ...]:
    if item.emitter == "unknown":
        return ()
    return tuple(
        EmitterAttributionItem(
            event=event,
            emitter=item.emitter,
            status="attributed",
            reason="direct event emission evidence is attributed by the emitter/consumer audit",
            consumers=item.consumers,
            evidence=tuple(e for e in item.evidence if e),
            emission_type=item.emission_type,
            confidence="high",
            attribution_evidence=tuple(
                ClassifiedEvidence("direct_emitter", e) for e in item.evidence if e
            ),
        )
        for event in item.emits
    )


def emitter_attribution_audit_json(audit: EmitterAttributionAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_emitter_attribution_audit(audit: EmitterAttributionAudit) -> str:
    lines = [
        "Emitter Attribution Audit",
        "",
        f"Items scanned: {audit.summary['items_scanned']}",
    ]
    for key in (
        "attributed",
        "dynamic",
        "indirect",
        "discovery_gap",
        "missing",
        "unknown",
    ):
        lines.append(f"{key.replace('_', ' ').title()}: {audit.summary[key]}")
    lines.append("")
    if not audit.items:
        lines.append(
            "No emitted outputs or consumed event literals were discovered from implementation evidence."
        )
        return "\n".join(lines)
    for item in audit.items:
        lines += [
            f"Event: {item.event}",
            f"Emission type: {item.emission_type}",
            "",
            "Consumers:",
        ]
        lines += [f"  {c}" for c in item.consumers] if item.consumers else ["  none"]
        lines += [
            "",
            f"Emitter: {item.emitter}",
            f"Status: {item.status}",
            f"Reason: {item.reason}",
            f"Confidence: {item.confidence}",
            "",
            "Attribution evidence:",
        ]
        lines += (
            [f"  {e.category}: {e.location}" for e in item.attribution_evidence]
            if item.attribution_evidence
            else ["  none"]
        )
        lines += [
            f"Supporting references: {len(item.supporting_references)}",
            "",
        ]
    return "\n".join(lines).rstrip()


def _classify_unknown_emitter_attribution(
    event: str,
    refs: tuple[ClassifiedEvidence, ...],
    dynamic_refs: tuple[ClassifiedEvidence, ...],
) -> UnknownEmitterAttribution:
    direct = tuple(ref for ref in refs if ref.category == "direct_emitter")
    indirect = tuple(ref for ref in refs if ref.category == "indirect_emitter")
    supporting = (
        tuple(ref for ref in refs if ref.category != "direct_emitter") + dynamic_refs
    )
    if direct:
        return UnknownEmitterAttribution(
            status="attributed",
            reason="direct emitter evidence was found; unrelated dynamic construction does not downgrade attribution",
            emitter=_emitter_name(direct[0].location.rsplit(":", 1)[0], event),
            confidence="high",
            attribution_evidence=direct,
            supporting_references=supporting,
        )
    non_consumer_refs = tuple(
        ref
        for ref in refs
        if ref.category not in {"projection_consumer", "diagnostic_reference"}
    )
    if (
        dynamic_refs
        and not non_consumer_refs
        and any(event.startswith(prefix) for prefix in WORKFLOW_PREFIXES)
    ):
        return UnknownEmitterAttribution(
            status="dynamic",
            reason="workflow event has consumers and only dynamic event construction evidence was found",
            emitter="unknown",
            confidence="low",
            attribution_evidence=dynamic_refs,
            supporting_references=refs,
        )
    if indirect:
        return UnknownEmitterAttribution(
            status="indirect",
            reason="event is visible through workflow helper or registration references, but current emit-call evidence does not attribute the helper path",
            emitter="unknown",
            confidence="medium",
            attribution_evidence=indirect,
            supporting_references=tuple(
                ref for ref in refs if ref.category != "indirect_emitter"
            )
            + dynamic_refs,
        )
    if refs:
        return UnknownEmitterAttribution(
            status="discovery_gap",
            reason="event literal is present in implementation evidence and consumed, but no direct emit call is attributed by current discovery",
            emitter="unknown",
            confidence="low",
            attribution_evidence=(),
            supporting_references=refs + dynamic_refs,
        )
    if dynamic_refs and any(event.startswith(prefix) for prefix in WORKFLOW_PREFIXES):
        return UnknownEmitterAttribution(
            status="dynamic",
            reason="workflow event has consumers and only dynamic event construction evidence was found",
            emitter="unknown",
            confidence="low",
            attribution_evidence=dynamic_refs,
            supporting_references=(),
        )
    return UnknownEmitterAttribution(
        status="missing",
        reason="event is consumed by implementation evidence, but no emitter literal was found in the scanned implementation scope",
        emitter="unknown",
        confidence="none",
        attribution_evidence=(),
        supporting_references=dynamic_refs,
    )


def _collect_emitter_attribution_implementation_evidence(
    root: Path,
) -> EmitterAttributionImplementationEvidence:
    literals: dict[str, set[ClassifiedEvidence]] = {}
    dynamic: set[ClassifiedEvidence] = set()
    for path in _python_files(root):
        source = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and "." in node.value
            ):
                literals.setdefault(node.value, set()).add(
                    ClassifiedEvidence(_reference_category(rel), f"{rel}:{node.lineno}")
                )
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "Event":
                    if not any(
                        kw.arg == "kind" and isinstance(kw.value, ast.Constant)
                        for kw in node.keywords
                    ):
                        dynamic.add(
                            ClassifiedEvidence(
                                "event_constructor", f"{rel}:{node.lineno}"
                            )
                        )
                if isinstance(node.func, ast.Attribute) and node.func.attr in {
                    "append",
                    "append_many",
                }:
                    if not (node.args and isinstance(node.args[0], ast.Constant)):
                        dynamic.add(
                            ClassifiedEvidence(
                                "event_constructor", f"{rel}:{node.lineno}"
                            )
                        )
    for path in _python_files(root):
        source = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if _is_direct_append_literal(node):
                literal = node.args[0].value
                literals.setdefault(literal, set()).add(
                    ClassifiedEvidence("direct_emitter", f"{rel}:{node.lineno}")
                )
    return EmitterAttributionImplementationEvidence(
        literal_references={
            k: tuple(sorted(v, key=lambda e: (e.category, e.location)))
            for k, v in literals.items()
        },
        dynamic_event_construction=tuple(
            sorted(dynamic, key=lambda e: (e.category, e.location))
        ),
    )


def _implementation_evidence(
    root: Path,
) -> tuple[dict[str, tuple[ClassifiedEvidence, ...]], tuple[ClassifiedEvidence, ...]]:
    evidence = _collect_emitter_attribution_implementation_evidence(root)
    return evidence.literal_references, evidence.dynamic_event_construction


def _is_direct_append_literal(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"append", "append_many"}
        and bool(node.args)
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        and "." in node.args[0].value
    )


def _reference_category(rel: str) -> EvidenceCategory:
    if rel.startswith("tests/") or rel.startswith("test_"):
        return "test_reference"
    if rel.endswith("diagnostic_inventory.py"):
        return "inventory_reference"
    if "audit" in rel or "diagnostic" in rel:
        return "diagnostic_reference"
    if rel in {"seed_runtime/state.py", "seed_runtime/projection_store.py"}:
        return "projection_consumer"
    if "action_plans.py" in rel or "pending_actions.py" in rel:
        return "indirect_emitter"
    return "string_reference"


def _unknown_attribution(
    event: str,
    refs: tuple[ClassifiedEvidence, ...],
    dynamic_refs: tuple[ClassifiedEvidence, ...],
) -> tuple[
    AttributionStatus,
    str,
    str,
    AttributionConfidence,
    tuple[ClassifiedEvidence, ...],
    tuple[ClassifiedEvidence, ...],
]:
    attribution = _classify_unknown_emitter_attribution(event, refs, dynamic_refs)
    return (
        attribution.status,
        attribution.reason,
        attribution.emitter,
        attribution.confidence,
        attribution.attribution_evidence,
        attribution.supporting_references,
    )
