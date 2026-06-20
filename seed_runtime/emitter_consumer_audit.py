"""Implementation-backed emitter/consumer visibility audit."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

RelationshipStatus = Literal["consumed", "orphaned", "partially_consumed", "unknown"]

SCAN_PATHS = ("seed_runtime", "scripts")
CONSUMER_GROUPS = {
    "projection builders": (
        "seed_runtime/state.py",
        "seed_runtime/projection_store.py",
    ),
    "read models": (
        "seed_runtime/state_views.py",
        "seed_runtime/context_views.py",
        "seed_runtime/state_summary_views.py",
        "seed_runtime/facts.py",
    ),
    "diagnostics and audits": ("seed_runtime",),
    "CLI surfaces": ("scripts/seed_local.py",),
    "action workflows": (
        "seed_runtime/action_plans.py",
        "seed_runtime/pending_actions.py",
        "seed_runtime/handoff_plans.py",
    ),
}


@dataclass(frozen=True)
class EmitterConsumerItem:
    emitter: str
    emits: tuple[str, ...]
    consumers: tuple[str, ...]
    status: RelationshipStatus
    evidence: tuple[str, ...] = ()

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "emitter": self.emitter,
            "emits": list(self.emits),
            "consumers": list(self.consumers),
            "status": self.status,
            "evidence": list(self.evidence),
        }


@dataclass(frozen=True)
class EmitterConsumerAudit:
    items: tuple[EmitterConsumerItem, ...]
    metadata: dict[str, Any]

    @property
    def summary(self) -> dict[str, int]:
        return {
            "items_scanned": len(self.items),
            "consumed": sum(item.status == "consumed" for item in self.items),
            "orphaned": sum(item.status == "orphaned" for item in self.items),
            "partially_consumed": sum(
                item.status == "partially_consumed" for item in self.items
            ),
            "unknown": sum(item.status == "unknown" for item in self.items),
        }

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "items": [i.to_json_dict() for i in self.items],
            "metadata": dict(self.metadata),
        }


def build_emitter_consumer_audit(
    root: str | Path | None = None,
) -> EmitterConsumerAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    py_files = _python_files(repo_root)
    emitted: dict[str, set[str]] = {}
    evidence: dict[tuple[str, str], set[str]] = {}
    consumed: dict[str, set[str]] = {}

    for path in py_files:
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        rel = path.relative_to(repo_root).as_posix()
        for visitor_item in _discover_file(tree, rel):
            kind, name, line = visitor_item
            if kind == "emit":
                emitter = _emitter_name(rel, name)
                emitted.setdefault(emitter, set()).add(name)
                evidence.setdefault((emitter, name), set()).add(f"{rel}:{line}")
            elif kind == "consume":
                consumed.setdefault(name, set()).add(_consumer_name(rel))

    items: list[EmitterConsumerItem] = []
    for emitter, outputs in emitted.items():
        consumers = sorted(
            {c for output in outputs for c in consumed.get(output, set())}
        )
        consumed_outputs = sum(1 for output in outputs if consumed.get(output))
        status: RelationshipStatus
        if not outputs:
            status = "unknown"
        elif consumed_outputs == len(outputs):
            status = "consumed"
        elif consumed_outputs == 0:
            status = "orphaned"
        else:
            status = "partially_consumed"
        items.append(
            EmitterConsumerItem(
                emitter=emitter,
                emits=tuple(sorted(outputs)),
                consumers=tuple(consumers),
                status=status,
                evidence=tuple(
                    sorted(
                        e
                        for output in outputs
                        for e in evidence.get((emitter, output), set())
                    )
                ),
            )
        )

    # Visible consumers whose emitter is not visible in scanned implementation.
    all_emitted = {output for outputs in emitted.values() for output in outputs}
    for output, consumers in consumed.items():
        if output not in all_emitted:
            items.append(
                EmitterConsumerItem(
                    emitter="unknown",
                    emits=(output,),
                    consumers=tuple(sorted(consumers)),
                    status="unknown",
                    evidence=(),
                )
            )

    return EmitterConsumerAudit(
        items=tuple(sorted(items, key=lambda i: (i.status, i.emitter, i.emits))),
        metadata={
            "discovery": "AST scan of event ledger append literals, Event(...) kind literals, and event.kind comparisons; grouped by implementation path.",
            "scope": list(SCAN_PATHS),
        },
    )


def emitter_consumer_audit_json(audit: EmitterConsumerAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_emitter_consumer_audit(audit: EmitterConsumerAudit) -> str:
    lines = [
        "Emitter/Consumer Audit",
        "",
        f"Items scanned: {audit.summary['items_scanned']}",
        f"Consumed: {audit.summary['consumed']}",
        f"Orphaned: {audit.summary['orphaned']}",
        f"Partially consumed: {audit.summary['partially_consumed']}",
        f"Unknown: {audit.summary['unknown']}",
        "",
    ]
    if not audit.items:
        lines.append(
            "No emitted outputs or consumers were discovered from implementation evidence."
        )
        return "\n".join(lines)
    for item in audit.items:
        lines += [f"Emitter: {item.emitter}", "", "Emits:"]
        lines += [f"  {output}" for output in item.emits]
        lines += ["", "Consumers:"]
        lines += (
            [f"  {consumer}" for consumer in item.consumers]
            if item.consumers
            else ["  none"]
        )
        lines += ["", f"Status: {item.status}", ""]
    return "\n".join(lines).rstrip()


def _python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for scan_path in SCAN_PATHS:
        base = root / scan_path
        if base.is_file() and base.suffix == ".py":
            files.append(base)
        elif base.exists():
            files.extend(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)
    return sorted(set(files))


def _discover_file(tree: ast.AST, rel: str) -> Iterable[tuple[str, str, int]]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            literal = _event_emit_literal(node)
            if literal:
                yield ("emit", literal, node.lineno)
        if isinstance(node, ast.Compare):
            for literal in _event_consume_literals(node):
                yield ("consume", literal, node.lineno)


def _event_emit_literal(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Attribute) and node.func.attr in {
        "append",
        "append_many",
    }:
        if (
            node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            and "." in node.args[0].value
        ):
            return node.args[0].value
    if isinstance(node.func, ast.Name) and node.func.id == "Event":
        for kw in node.keywords:
            if (
                kw.arg == "kind"
                and isinstance(kw.value, ast.Constant)
                and isinstance(kw.value.value, str)
            ):
                return kw.value.value
    return None


def _event_consume_literals(node: ast.Compare) -> tuple[str, ...]:
    left_is_kind = isinstance(node.left, ast.Attribute) and node.left.attr == "kind"
    if not left_is_kind:
        return ()
    values: list[str] = []
    for comparator in node.comparators:
        if (
            isinstance(comparator, ast.Constant)
            and isinstance(comparator.value, str)
            and "." in comparator.value
        ):
            values.append(comparator.value)
        elif isinstance(comparator, (ast.Set, ast.Tuple, ast.List)):
            values.extend(
                e.value
                for e in comparator.elts
                if isinstance(e, ast.Constant)
                and isinstance(e.value, str)
                and "." in e.value
            )
    return tuple(values)


def _emitter_name(rel: str, output: str) -> str:
    if output.startswith("action_plan."):
        return "action_plan"
    if output.startswith("fact."):
        return "fact emitter"
    if output.startswith("observation."):
        return "observation provider"
    if output.startswith("evidence."):
        return "evidence emitter"
    return rel.rsplit("/", 1)[-1].removesuffix(".py")


def _consumer_name(rel: str) -> str:
    for name, prefixes in CONSUMER_GROUPS.items():
        if any(
            rel == prefix or rel.startswith(prefix.rstrip("/") + "/")
            for prefix in prefixes
        ):
            return name
    return rel
