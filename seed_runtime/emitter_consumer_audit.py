"""Implementation-backed emitter/consumer visibility audit."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

RelationshipStatus = Literal["consumed", "orphaned", "partially_consumed", "unknown"]
EmissionType = Literal[
    "domain_emission",
    "rendered_message",
    "fallback_text",
    "guardrail_text",
    "validation_message",
    "unknown_string",
]

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
class EmitterConsumerScanResult:
    emitted: dict[tuple[str, EmissionType], set[str]]
    consumed: dict[tuple[str, EmissionType], set[str]]
    evidence: dict[tuple[str, str], set[str]]


@dataclass(frozen=True)
class EmitterConsumerItem:
    emitter: str
    emits: tuple[str, ...]
    consumers: tuple[str, ...]
    status: RelationshipStatus
    evidence: tuple[str, ...] = ()
    emission_type: EmissionType = "domain_emission"

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "emitter": self.emitter,
            "emits": list(self.emits),
            "consumers": list(self.consumers),
            "status": self.status,
            "evidence": list(self.evidence),
            "emission_type": self.emission_type,
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
    *,
    include_rendered: bool = False,
) -> EmitterConsumerAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    scan_result = _collect_emitter_consumer_scan_result(
        repo_root, include_rendered=include_rendered
    )
    emitted = scan_result.emitted
    consumed = scan_result.consumed

    scanned_rows = _scanned_emitted_item_rows(scan_result)
    unknown_rows = _unknown_emitter_rows(emitted, consumed)

    return _assemble_emitter_consumer_audit(
        scanned_rows, unknown_rows, include_rendered=include_rendered
    )


def _assemble_emitter_consumer_audit(
    scanned_rows: Iterable[EmitterConsumerItem],
    unknown_emitter_rows: Iterable[EmitterConsumerItem],
    *,
    include_rendered: bool = False,
) -> EmitterConsumerAudit:
    items = [*scanned_rows, *unknown_emitter_rows]
    return EmitterConsumerAudit(
        items=tuple(sorted(items, key=lambda i: (i.status, i.emitter, i.emits))),
        metadata={
            "discovery": "AST scan of event ledger append literals, Event(...) kind literals, and event.kind comparisons; rendered strings are excluded unless include_rendered is true.",
            "include_rendered": include_rendered,
            "scope": list(SCAN_PATHS),
        },
    )


def _scanned_emitted_item_rows(
    scan_result: EmitterConsumerScanResult,
) -> list[EmitterConsumerItem]:
    rows: list[EmitterConsumerItem] = []
    for (emitter, emission_type), outputs in scan_result.emitted.items():
        consumers = sorted(
            {
                c
                for output in outputs
                for c in scan_result.consumed.get((output, emission_type), set())
            }
        )
        status = _derive_emitted_output_relationship_status(
            outputs, emission_type, scan_result.consumed
        )
        rows.append(
            EmitterConsumerItem(
                emitter=emitter,
                emits=tuple(sorted(outputs)),
                consumers=tuple(consumers),
                status=status,
                evidence=tuple(
                    sorted(
                        e
                        for output in outputs
                        for e in scan_result.evidence.get((emitter, output), set())
                    )
                ),
                emission_type=emission_type,
            )
        )
    return rows


def _unknown_emitter_rows(
    emitted: dict[tuple[str, EmissionType], set[str]],
    consumed: dict[tuple[str, EmissionType], set[str]],
) -> list[EmitterConsumerItem]:
    rows: list[EmitterConsumerItem] = []
    all_emitted = {output for outputs in emitted.values() for output in outputs}
    for (output, emission_type), consumers in consumed.items():
        if output not in all_emitted:
            rows.append(
                EmitterConsumerItem(
                    emitter="unknown",
                    emits=(output,),
                    consumers=tuple(sorted(consumers)),
                    status="unknown",
                    evidence=(),
                    emission_type=emission_type,
                )
            )
    return rows

def _derive_emitted_output_relationship_status(
    outputs: set[str],
    emission_type: EmissionType,
    consumed: dict[tuple[str, EmissionType], set[str]],
) -> RelationshipStatus:
    consumed_outputs = sum(
        1 for output in outputs if consumed.get((output, emission_type))
    )
    if not outputs:
        return "unknown"
    if consumed_outputs == len(outputs):
        return "consumed"
    if consumed_outputs == 0:
        return "orphaned"
    return "partially_consumed"

def _collect_emitter_consumer_scan_result(
    repo_root: Path, *, include_rendered: bool = False
) -> EmitterConsumerScanResult:
    emitted: dict[tuple[str, EmissionType], set[str]] = {}
    evidence: dict[tuple[str, str], set[str]] = {}
    consumed: dict[tuple[str, EmissionType], set[str]] = {}

    for path in _python_files(repo_root):
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        rel = path.relative_to(repo_root).as_posix()
        for visitor_item in _discover_file(tree, rel, include_rendered=include_rendered):
            kind, name, line = visitor_item
            emission_type = classify_emission_string(name)
            if emission_type != "domain_emission" and not include_rendered:
                continue
            if kind == "emit":
                emitter = _emitter_name(rel, name)
                emitted.setdefault((emitter, emission_type), set()).add(name)
                evidence.setdefault((emitter, name), set()).add(f"{rel}:{line}")
            elif kind == "consume":
                consumed.setdefault((name, emission_type), set()).add(_consumer_name(rel))

    return EmitterConsumerScanResult(
        emitted=emitted,
        consumed=consumed,
        evidence=evidence,
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
        lines += [
            f"Emitter: {item.emitter}",
            f"Emission type: {item.emission_type}",
            "",
            "Emits:",
        ]
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


def _discover_file(
    tree: ast.AST, rel: str, *, include_rendered: bool = False
) -> Iterable[tuple[str, str, int]]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            literal = _event_emit_literal(node, include_rendered=include_rendered)
            if literal:
                yield ("emit", literal, node.lineno)
        if isinstance(node, ast.Compare):
            for literal in _event_consume_literals(node):
                yield ("consume", literal, node.lineno)


def _event_emit_literal(node: ast.Call, *, include_rendered: bool = False) -> str | None:
    if _is_event_ledger_append(node):
        if (
            node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            and "." in node.args[0].value
        ):
            return node.args[0].value
    elif include_rendered and _is_render_append(node):
        if (
            node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            and "." in node.args[0].value
        ):
            literal = node.args[0].value
            if classify_emission_string(literal) != "domain_emission":
                return literal
    if isinstance(node.func, ast.Name) and node.func.id == "Event":
        for kw in node.keywords:
            if (
                kw.arg == "kind"
                and isinstance(kw.value, ast.Constant)
                and isinstance(kw.value.value, str)
            ):
                return kw.value.value
    return None


def _is_event_ledger_append(node: ast.Call) -> bool:
    if not (
        isinstance(node.func, ast.Attribute)
        and node.func.attr in {"append", "append_many"}
    ):
        return False
    receiver = node.func.value
    if isinstance(receiver, ast.Attribute) and receiver.attr == "ledger":
        return True
    if isinstance(receiver, ast.Name) and receiver.id in {"ledger", "event_ledger"}:
        return True
    return False


def _is_render_append(node: ast.Call) -> bool:
    return isinstance(node.func, ast.Attribute) and node.func.attr == "append"


def classify_emission_string(value: str) -> EmissionType:
    normalized = value.strip()
    if normalized.startswith("Guardrail:"):
        return "guardrail_text"
    if normalized.startswith("No ") or normalized.startswith("No emitted outputs"):
        return "fallback_text"
    if (
        any(ch.isspace() for ch in normalized)
        or normalized.endswith(".")
        or ":" in normalized
        or ";" in normalized
    ):
        return "rendered_message"
    parts = normalized.split(".")
    if len(parts) >= 2 and all(
        part.replace("_", "").isalnum() and part.lower() == part
        for part in parts
    ):
        return "domain_emission"
    return "unknown_string"


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
