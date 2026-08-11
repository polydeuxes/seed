"""Read-only operational brief aggregated from existing visibility surfaces."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seed_runtime.audit_snapshots import list_audit_snapshots
from seed_runtime.capability_needs import build_capability_needs
from seed_runtime.consumer_dependency_audit import build_consumer_audit
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import (
    build_diagnostic_shape_audit,
    summarize_diagnostic_shape_audit,
)
from seed_runtime.observation_inventory import build_observation_inventory
from seed_runtime.observation_utilization import build_observation_utilization_audit
from seed_runtime.ownership_discrepancies import build_ownership_discrepancies
from seed_runtime.state import State


@dataclass(frozen=True)
class OpsBrief:
    observations: dict[str, Any]
    ownership: dict[str, Any]
    capabilities: dict[str, Any]
    diagnostics: dict[str, Any]
    snapshots: dict[str, Any]
    recommended_actions: list[dict[str, str]]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "observations": self.observations,
            "ownership": self.ownership,
            "capabilities": self.capabilities,
            "diagnostics": self.diagnostics,
            "snapshots": self.snapshots,
            "recommended_actions": self.recommended_actions,
        }


def build_ops_brief(state: State, *, repo_root: str | Path | None = None) -> OpsBrief:
    root = (
        Path(repo_root)
        if repo_root is not None
        else Path(__file__).resolve().parents[1]
    )
    inventory = build_observation_inventory(root)
    utilization = build_observation_utilization_audit(root)
    consumers = build_consumer_audit(root)
    ownership_rows = build_ownership_discrepancies(state)
    capability_entries = build_capability_needs(state)
    shape_root = root if (root / "scripts" / "seed_local.py").exists() else None
    shape_rows = build_diagnostic_shape_audit(repo_root=shape_root)
    shape_summary = summarize_diagnostic_shape_audit(shape_rows)
    snapshots = list_audit_snapshots(root)

    consumer_summary = consumers.summary
    utilization_summary = utilization.summary
    conflict_counts = Counter(row.conflict for row in ownership_rows if row.conflict)
    kind_conflicts = Counter(row.kind for row in ownership_rows if row.conflict)
    top_capabilities = [
        {"capability": entry.capability, "subject_count": len(entry.subjects)}
        for entry in capability_entries[:5]
    ]
    latest_snapshot = snapshots[-1] if snapshots else None
    latest_kind = (latest_snapshot or {}).get("metadata", {}).get("kind")
    comparison_available = bool(
        latest_kind
        and sum(
            1 for row in snapshots if row.get("metadata", {}).get("kind") == latest_kind
        )
        >= 2
    )

    observations = {
        "providers": len(inventory.providers),
        "predicates": len(inventory.predicates),
        "unused_predicates": utilization_summary["unused_predicates"],
        "orphaned_predicates": sum(
            item.kind == "observation_predicate" and item.orphaned
            for item in consumers.items
        ),
        "fragile_predicates": sum(
            item.kind == "observation_predicate" and item.consumer_count == 1
            for item in consumers.items
        ),
    }
    ownership = {
        "storage_ambiguities": kind_conflicts["storage"],
        "service_ambiguities": kind_conflicts["service"],
        "insufficient_evidence": conflict_counts["insufficient_evidence"],
        "conflicts": dict(sorted(conflict_counts.items())),
    }
    capabilities = {
        "top_capability_needs": top_capabilities,
        "capability_need_count": len(capability_entries),
    }
    diagnostics = {
        "diagnostics": len(DIAGNOSTIC_INVENTORY),
        "shape_mismatches": shape_summary.mismatches,
        "warnings": shape_summary.warnings,
    }
    snapshot_summary = {
        "latest_snapshot": (latest_snapshot or {}).get("snapshot_id"),
        "snapshot_count": len(snapshots),
        "latest_comparison": "available" if comparison_available else "unavailable",
    }
    return OpsBrief(
        observations=observations,
        ownership=ownership,
        capabilities=capabilities,
        diagnostics=diagnostics,
        snapshots=snapshot_summary,
        recommended_actions=_recommend_actions(
            observations, ownership, capabilities, diagnostics
        ),
    )


def _recommend_actions(
    observations: dict[str, Any],
    ownership: dict[str, Any],
    capabilities: dict[str, Any],
    diagnostics: dict[str, Any],
) -> list[dict[str, str]]:
    actions: list[tuple[int, dict[str, str]]] = []
    top = capabilities["top_capability_needs"]
    if top:
        capability = top[0]["capability"]
        count = top[0]["subject_count"]
        actions.append(
            (
                count + 100,
                {
                    "action": f"Add {capability}.",
                    "reason": f"Highest recorded ownership capability need across {count} subject(s).",
                },
            )
        )
    if ownership["storage_ambiguities"] or ownership["service_ambiguities"]:
        total = ownership["storage_ambiguities"] + ownership["service_ambiguities"]
        actions.append(
            (
                total + 80,
                {
                    "action": "Review ownership discrepancies.",
                    "reason": f"Ownership audit reports {total} storage/service ambiguity row(s).",
                },
            )
        )
    if observations["orphaned_predicates"]:
        count = observations["orphaned_predicates"]
        actions.append(
            (
                count + 60,
                {
                    "action": "Investigate orphaned predicates.",
                    "reason": f"Consumer audit reports {count} observation predicate(s) with no implementation consumers.",
                },
            )
        )
    if observations["fragile_predicates"]:
        count = observations["fragile_predicates"]
        actions.append(
            (
                count + 40,
                {
                    "action": "Review fragile predicates.",
                    "reason": f"Consumer audit reports {count} observation predicate(s) with one implementation consumer.",
                },
            )
        )
    if diagnostics["shape_mismatches"] or diagnostics["warnings"]:
        actions.append(
            (
                diagnostics["shape_mismatches"] + diagnostics["warnings"] + 120,
                {
                    "action": "Repair diagnostic shape audit findings.",
                    "reason": f"Diagnostic shape audit reports {diagnostics['shape_mismatches']} mismatch(es) and {diagnostics['warnings']} warning(s).",
                },
            )
        )
    if not actions:
        return [
            {
                "action": "No immediate operational pressure surfaced.",
                "reason": "Existing audits did not report capability needs, ownership ambiguities, predicate consumer gaps, or diagnostic shape findings.",
            }
        ]
    return [
        item
        for _, item in sorted(actions, key=lambda pair: (-pair[0], pair[1]["action"]))[
            :5
        ]
    ]


def format_ops_brief(brief: OpsBrief) -> str:
    lines = ["Operational Brief", "", "Observations", ""]
    obs = brief.observations
    lines.extend(
        [
            f"Providers: {obs['providers']}",
            f"Predicates: {obs['predicates']}",
            f"Unused: {obs['unused_predicates']}",
            f"Orphaned: {obs['orphaned_predicates']}",
            f"Fragile: {obs['fragile_predicates']}",
            "",
            "Ownership",
            "",
        ]
    )
    own = brief.ownership
    lines.extend(
        [
            f"Storage ambiguities: {own['storage_ambiguities']}",
            f"Service ambiguities: {own['service_ambiguities']}",
            f"Insufficient evidence: {own['insufficient_evidence']}",
            "",
            "Capabilities",
            "",
            "Top capability needs:",
            "",
        ]
    )
    if brief.capabilities["top_capability_needs"]:
        for index, entry in enumerate(
            brief.capabilities["top_capability_needs"], start=1
        ):
            lines.append(f"{index}. {entry['capability']} ({entry['subject_count']})")
    else:
        lines.append("(none)")
    diag = brief.diagnostics
    snap = brief.snapshots
    lines.extend(
        [
            "",
            "Diagnostics",
            "",
            f"Diagnostics: {diag['diagnostics']}",
            f"Shape mismatches: {diag['shape_mismatches']}",
            f"Warnings: {diag['warnings']}",
            "",
            "Snapshots",
            "",
            f"Latest snapshot: {snap['latest_snapshot'] or '-'}",
            f"Snapshot count: {snap['snapshot_count']}",
            f"Latest comparison: {snap['latest_comparison']}",
            "",
            "Recommended Next Actions",
            "",
        ]
    )
    for index, action in enumerate(brief.recommended_actions, start=1):
        lines.append(f"{index}. {action['action']}")
        lines.append(f"   Reason: {action['reason']}")
        lines.append("")
    return "\n".join(lines).rstrip()
