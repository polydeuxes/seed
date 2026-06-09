"""Read-only State Summary aggregation helpers.

This module owns the semantic aggregation for the operator State Summary.  CLI
code should render the returned summary, not decide what the summary means.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from typing import Any

from seed_runtime.facts import is_fact_expired, is_measurement_predicate
from seed_runtime.state import State


def state_summary(
    state: State,
    *,
    top_entity_limit: int = 10,
    include_relationship_count: bool = False,
) -> dict[str, Any]:
    """Build a concise operator summary using only the projected State."""

    current_measurements = [
        fact
        for fact in state.facts.values()
        if is_measurement_predicate(fact.predicate) and not is_fact_expired(fact)
    ]
    durable_facts = [
        fact
        for fact in state.facts.values()
        if not is_measurement_predicate(fact.predicate)
    ]

    entity_aliases: dict[str, set[str]] = defaultdict(set)
    entity_fact_counts: Counter[str] = Counter()
    for fact in state.facts.values():
        canonical = state.alias_resolver.canonical(fact.subject_id)
        entity_aliases[canonical].update(state.alias_resolver.resolve(fact.subject_id))
        entity_fact_counts[canonical] += 1
    for entity in state.entities.values():
        canonical = state.alias_resolver.canonical(entity.name)
        entity_aliases[canonical].update({entity.name, *entity.aliases})
        entity_fact_counts.setdefault(canonical, 0)

    top_entities = [
        {
            "name": canonical,
            "alias_count": len(entity_aliases[canonical] - {canonical}),
            "fact_count": entity_fact_counts[canonical],
        }
        for canonical in sorted(
            entity_aliases, key=lambda name: (-entity_fact_counts[name], name)
        )[:top_entity_limit]
    ]

    availability = Counter({"up": 0, "down": 0, "unknown": 0})
    for canonical in sorted(entity_aliases):
        availability_fact = state.get_best_fact(
            canonical, "availability_status", resolve_aliases=False
        )
        status = (
            availability_fact.value
            if availability_fact is not None
            and availability_fact.value in availability
            else "unknown"
        )
        availability[status] += 1

    filesystems: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(dict)
    for fact in current_measurements:
        if fact.predicate not in {"filesystem_free_bytes", "filesystem_total_bytes"}:
            continue
        mountpoint = fact.dimensions.get("mountpoint")
        if mountpoint is None:
            continue
        canonical = state.alias_resolver.canonical(fact.subject_id)
        dimensions_key = json.dumps(
            fact.dimensions, sort_keys=True, separators=(",", ":")
        )
        key = (canonical, mountpoint, dimensions_key)
        field = "free" if fact.predicate == "filesystem_free_bytes" else "total"
        filesystems[key][field] = fact.value

    filesystem_summary = [
        {"host": host, "mountpoint": mountpoint, **values}
        for (host, mountpoint, _dimensions), values in sorted(filesystems.items())
        if "free" in values and "total" in values
    ]

    summary = {
        "entity_count": len(entity_aliases),
        "fact_count": len(state.facts),
        "durable_fact_count": len(durable_facts),
        "measurement_current_sample_count": len(current_measurements),
        "conflict_count": len(state.fact_conflicts),
        "stale_fact_count": len(state.get_stale_facts()),
        "graph_issue_count": len(state.graph_issues),
        "graph_issue_warning_count": len(state.get_graph_issues("warning")),
        "graph_issue_error_count": len(state.get_graph_issues("error")),
        "observation_source_counts": dict(
            sorted(
                Counter(obs.source_type for obs in state.observations.values()).items()
            )
        ),
        "top_entities": top_entities,
        "availability": dict(availability),
        "filesystems": filesystem_summary,
    }
    if include_relationship_count:
        summary["relationship_count"] = len(state.relationships)
    return summary


# Descriptive alias for callers that want to distinguish this operator summary
# from the lower-level v1 State View summary.
build_operator_state_summary = state_summary

__all__ = ["build_operator_state_summary", "state_summary"]
