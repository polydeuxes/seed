"""Implementation-backed consumer dependency audit."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.observation_inventory import build_observation_inventory


@dataclass(frozen=True)
class ConsumerAuditItem:
    item: str
    kind: str
    consumers: tuple[str, ...]

    @property
    def consumer_count(self) -> int:
        return len(self.consumers)

    @property
    def orphaned(self) -> bool:
        return not self.consumers

    @property
    def highlight(self) -> str:
        if self.orphaned:
            return "orphaned"
        if self.consumer_count == 1:
            return "fragile"
        if self.consumer_count >= 3:
            return "widely used"
        return "used"

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "item": self.item,
            "kind": self.kind,
            "consumers": list(self.consumers),
            "consumer_count": self.consumer_count,
            "orphaned": self.orphaned,
            "highlight": self.highlight,
        }


@dataclass(frozen=True)
class ConsumerAudit:
    items: tuple[ConsumerAuditItem, ...]
    metadata: dict[str, str]

    @property
    def summary(self) -> dict[str, int]:
        return {
            "items_scanned": len(self.items),
            "orphaned_items": sum(item.orphaned for item in self.items),
            "single_consumer_items": sum(
                item.consumer_count == 1 for item in self.items
            ),
            "multi_consumer_items": sum(item.consumer_count > 1 for item in self.items),
        }

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary,
            "items": [item.to_json_dict() for item in self.items],
            "metadata": dict(self.metadata),
        }


CONSUMER_PATHS = {
    "projection_builders": (
        "seed_runtime/state.py",
        "seed_runtime/projection_store.py",
    ),
    "read_models": (
        "seed_runtime/state_views.py",
        "seed_runtime/context_views.py",
        "seed_runtime/state_summary_views.py",
        "seed_runtime/context_selection.py",
        "seed_runtime/facts.py",
    ),
    "diagnostics": (
        "seed_runtime/ownership_discrepancies.py",
        "seed_runtime/capability_needs.py",
        "seed_runtime/classification_coverage.py",
        "seed_runtime/knowledge_reachability.py",
        "seed_runtime/observation_utilization.py",
    ),
    "state_build": (
        "scripts/seed_local.py",
        "seed_runtime/state_summary_views.py",
        "seed_runtime/facts.py",
    ),
    "views": (
        "scripts/seed_local.py",
        "seed_runtime/state_views.py",
        "seed_runtime/context_views.py",
    ),
}


def build_consumer_audit(
    root: str | Path | None = None,
    *,
    predicate_filter: str | None = None,
    diagnostic_filter: str | None = None,
) -> ConsumerAudit:
    repo_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    sources = _read_sources(repo_root)
    items: list[ConsumerAuditItem] = []
    if diagnostic_filter is None:
        inventory = build_observation_inventory(
            repo_root, predicate_filter=predicate_filter
        )
        for predicate in inventory.predicates:
            items.append(
                _audit_item(
                    predicate.predicate,
                    "observation_predicate",
                    sources,
                    repo_root=repo_root,
                )
            )
    if predicate_filter is None:
        diagnostics = [entry.name for entry in DIAGNOSTIC_INVENTORY]
        for diagnostic in diagnostics:
            if diagnostic_filter is not None and diagnostic != diagnostic_filter:
                continue
            items.append(
                _audit_item(diagnostic, "diagnostic", sources, repo_root=repo_root)
            )
    return ConsumerAudit(
        items=tuple(sorted(items, key=lambda item: (item.kind, item.item))),
        metadata={
            "discovery": "observation predicates from observation inventory; diagnostics from diagnostic inventory; consumers from implementation source mentions",
            "consumer_evidence": "; ".join(
                f"{name}: {', '.join(paths)}" for name, paths in CONSUMER_PATHS.items()
            ),
        },
    )


def consumer_audit_json(audit: ConsumerAudit) -> dict[str, Any]:
    return audit.to_json_dict()


def format_consumer_audit(audit: ConsumerAudit) -> str:
    lines = [
        "Consumer Dependency Audit",
        "",
        f"Items scanned: {audit.summary['items_scanned']}",
        f"Orphaned items: {audit.summary['orphaned_items']}",
        f"Single-consumer items: {audit.summary['single_consumer_items']}",
        f"Multi-consumer items: {audit.summary['multi_consumer_items']}",
        "",
    ]
    if not audit.items:
        lines.append("No items matched the selected filters.")
        return "\n".join(lines)
    for item in audit.items:
        lines.extend(
            [
                f"Item: {item.item}",
                f"Kind: {item.kind}",
                "",
                "Consumers:",
            ]
        )
        (
            lines.extend(f"  {consumer}" for consumer in item.consumers)
            if item.consumers
            else lines.append("  none")
        )
        lines.extend(
            [
                "",
                f"Consumer Count: {item.consumer_count}",
                f"Orphaned: {'yes' if item.orphaned else 'no'}",
                f"Highlight: {item.highlight}",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def _audit_item(
    item: str, kind: str, sources: dict[str, dict[str, str]], *, repo_root: Path
) -> ConsumerAuditItem:
    aliases = _consumer_lookup_terms(item, repo_root=repo_root)
    consumers = []
    for consumer, files in sources.items():
        if _mentions_any_item(files.values(), aliases):
            consumers.append(consumer)
    return ConsumerAuditItem(item=item, kind=kind, consumers=tuple(consumers))


def _read_sources(root: Path) -> dict[str, dict[str, str]]:
    return {
        consumer: {path: _read(root / path) for path in paths}
        for consumer, paths in CONSUMER_PATHS.items()
    }


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _consumer_lookup_terms(item: str, *, repo_root: Path) -> frozenset[str]:
    """Return exact predicate terms that can prove implementation consumption.

    Observation producers may emit provider/raw predicate names while read models
    consume the canonical predicate produced by the projection normalizer.  The
    audit should therefore credit implementation references to the canonical
    predicate for raw predicates that have an explicit catalog mapping, without
    falling back to broad prefix/family matching.
    """

    terms = {item}
    catalog_path = repo_root / "predicate_catalog" / "core.json"
    if catalog_path.exists():
        data = json.loads(catalog_path.read_text(encoding="utf-8"))
        for mapping in data.get("mappings", []):
            if mapping.get("predicate") == item and mapping.get("canonical_predicate"):
                terms.add(str(mapping["canonical_predicate"]))
    return frozenset(terms)


def _mentions_any_item(sources: Iterable[str], items: Iterable[str]) -> bool:
    needles = set()
    for item in items:
        needles.update({item, json.dumps(item), repr(item), item.replace("_", "-")})
    return any(any(needle in source for needle in needles) for source in sources)
