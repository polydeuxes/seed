"""Explanatory attribution audit for emitted event visibility."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from seed_runtime.emitter_consumer_audit import (
    EmitterConsumerAudit,
    build_emitter_consumer_audit,
    _python_files,
)

AttributionStatus = Literal[
    "attributed", "dynamic", "indirect", "discovery_gap", "missing", "unknown"
]

WORKFLOW_PREFIXES = (
    "action_plan.",
    "pending_action.",
    "approval.",
    "execution_proposal.",
    "tool.",
)


@dataclass(frozen=True)
class EmitterAttributionItem:
    event: str
    emitter: str
    status: AttributionStatus
    reason: str
    consumers: tuple[str, ...]
    evidence: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "event": self.event,
            "emitter": self.emitter,
            "status": self.status,
            "reason": self.reason,
            "consumers": list(self.consumers),
            "evidence": list(self.evidence),
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
) -> EmitterAttributionAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    base = build_emitter_consumer_audit(repo_root)
    literal_refs, dynamic_refs = _implementation_evidence(repo_root)
    items: list[EmitterAttributionItem] = []
    for item in base.items:
        for event in item.emits:
            if item.emitter != "unknown":
                items.append(
                    EmitterAttributionItem(
                        event=event,
                        emitter=item.emitter,
                        status="attributed",
                        reason="direct event emission evidence is attributed by the emitter/consumer audit",
                        consumers=item.consumers,
                        evidence=tuple(e for e in item.evidence if e),
                    )
                )
                continue
            status, reason = _unknown_reason(
                event, literal_refs.get(event, ()), dynamic_refs
            )
            items.append(
                EmitterAttributionItem(
                    event=event,
                    emitter="unknown",
                    status=status,
                    reason=reason,
                    consumers=item.consumers,
                    evidence=tuple(literal_refs.get(event, ())) + tuple(dynamic_refs),
                )
            )
    return EmitterAttributionAudit(
        items=tuple(sorted(items, key=lambda i: (i.status, i.event))),
        metadata={
            "discovery": "Refines emitter/consumer audit rows with AST literal references, dynamic Event/append calls, and workflow-prefix visibility hints.",
            "scope": list(base.metadata.get("scope", [])),
        },
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
        lines += [f"Event: {item.event}", "", "Consumers:"]
        lines += [f"  {c}" for c in item.consumers] if item.consumers else ["  none"]
        lines += [
            "",
            f"Emitter: {item.emitter}",
            f"Status: {item.status}",
            f"Reason: {item.reason}",
            "",
        ]
    return "\n".join(lines).rstrip()


def _unknown_reason(
    event: str, refs: tuple[str, ...], dynamic_refs: tuple[str, ...]
) -> tuple[AttributionStatus, str]:
    if dynamic_refs and any(event.startswith(prefix) for prefix in WORKFLOW_PREFIXES):
        return (
            "dynamic",
            "workflow event has consumers, while emitter discovery also found dynamic event construction that cannot be attributed to a literal event kind",
        )
    if refs and any(
        "pending_actions.py" in ref or "action_plans.py" in ref for ref in refs
    ):
        return (
            "indirect",
            "event is visible through workflow helper or registration references, but current emit-call evidence does not attribute the helper path",
        )
    if refs:
        return (
            "discovery_gap",
            "event literal is present in implementation evidence and consumed, but no direct emit call is attributed by current discovery",
        )
    return (
        "missing",
        "event is consumed by implementation evidence, but no emitter literal was found in the scanned implementation scope",
    )


def _implementation_evidence(
    root: Path,
) -> tuple[dict[str, tuple[str, ...]], tuple[str, ...]]:
    literals: dict[str, set[str]] = {}
    dynamic: set[str] = set()
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
                literals.setdefault(node.value, set()).add(f"{rel}:{node.lineno}")
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == "Event":
                    if not any(
                        kw.arg == "kind" and isinstance(kw.value, ast.Constant)
                        for kw in node.keywords
                    ):
                        dynamic.add(f"{rel}:{node.lineno}")
                if isinstance(node.func, ast.Attribute) and node.func.attr in {
                    "append",
                    "append_many",
                }:
                    if not (node.args and isinstance(node.args[0], ast.Constant)):
                        dynamic.add(f"{rel}:{node.lineno}")
    return ({k: tuple(sorted(v)) for k, v in literals.items()}, tuple(sorted(dynamic)))
