"""Read-only State Summary aggregation helpers.

This module owns the semantic aggregation for the operator State Summary.  CLI
code should render the returned summary, not decide what the summary means.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from typing import Any

from seed_runtime.facts import is_fact_expired, is_measurement_predicate
from seed_runtime.local_host_mounts import (
    is_operator_relevant_mount,
    mount_display_priority,
)
from seed_runtime.state import State


_SHARED_STORAGE_CANDIDATE_BOUNDARY = (
    "candidate shared storage != shared storage fact; "
    "candidate shared storage != ownership; "
    "candidate shared storage != topology authority"
)


def _shared_storage_candidates(
    filesystems: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return projection-only shared-storage interpretations.

    Candidates are deliberately rendered from observed filesystem measurement
    fields only.  They are not facts, ownership assertions, storage identities,
    relationships, or topology authority.
    """

    signature_specs = [
        (("mountpoint", "device", "fstype", "total", "free"), "high"),
        (("device", "fstype", "total"), "medium"),
        (("mountpoint", "fstype", "total"), "medium"),
        (("total",), "low"),
    ]
    evidence_labels = {
        "mountpoint": "matching mountpath",
        "device": "matching device",
        "fstype": "matching filesystem type",
        "total": "matching total bytes",
        "free": "matching free bytes",
    }

    candidates_by_key: dict[tuple[tuple[str, object], ...], dict[str, Any]] = {}
    for fields, confidence in signature_specs:
        groups: dict[tuple[object, ...], list[dict[str, Any]]] = defaultdict(list)
        for filesystem in filesystems:
            values = tuple(filesystem.get(field) for field in fields)
            if any(value is None for value in values):
                continue
            groups[values].append(filesystem)

        for values, members in groups.items():
            endpoints = sorted({str(member["host"]) for member in members})
            if len(endpoints) < 2:
                continue
            mountpaths = sorted({str(member["mountpoint"]) for member in members})
            evidence = [evidence_labels[field] for field in fields]
            observed_values = dict(zip(fields, values, strict=True))
            candidate_key = tuple(sorted(observed_values.items()))
            candidates_by_key.setdefault(
                candidate_key,
                {
                    "candidate_kind": "candidate_shared_storage",
                    "mountpaths": mountpaths,
                    "visible_endpoint_count": len(endpoints),
                    "visible_endpoints": endpoints,
                    "evidence": evidence,
                    "observed_values": observed_values,
                    "confidence": confidence,
                    "confidence_basis": (
                        "derived only from matching observable filesystem "
                        "measurement fields; confidence is not certainty"
                    ),
                    "boundary": _SHARED_STORAGE_CANDIDATE_BOUNDARY,
                },
            )

    return sorted(
        candidates_by_key.values(),
        key=lambda candidate: (
            {"high": 0, "medium": 1, "low": 2}[candidate["confidence"]],
            candidate["mountpaths"],
            candidate["evidence"],
            candidate["visible_endpoints"],
        ),
    )


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
            if availability_fact is not None and availability_fact.value in availability
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
        filesystems[key].setdefault("device", fact.dimensions.get("device"))
        filesystems[key].setdefault("fstype", fact.dimensions.get("fstype"))

    complete_filesystems = [
        {
            "host": host,
            "mountpoint": mountpoint,
            "dimensions_key": dimensions_key,
            **values,
        }
        for (host, mountpoint, dimensions_key), values in filesystems.items()
        if "free" in values and "total" in values
    ]
    operator_relevant_filesystems = [
        filesystem
        for filesystem in complete_filesystems
        if is_operator_relevant_mount(
            filesystem["mountpoint"],
            [filesystem["fstype"]] if filesystem.get("fstype") else (),
        )
    ]
    filesystem_summary = [
        {
            key: value
            for key, value in filesystem.items()
            if key not in {"device", "dimensions_key"}
        }
        for filesystem in sorted(
            operator_relevant_filesystems,
            key=lambda filesystem: (
                mount_display_priority(
                    filesystem["mountpoint"],
                    [filesystem["fstype"]] if filesystem.get("fstype") else (),
                ),
                filesystem["host"],
                filesystem["dimensions_key"],
            ),
        )
    ]

    mount_visibility: dict[str, set[str]] = defaultdict(set)
    for filesystem in filesystem_summary:
        mount_visibility[filesystem["mountpoint"]].add(filesystem["host"])
    cluster_mount_groups = [
        {
            "mountpoint": mountpoint,
            "visible_endpoint_count": len(endpoints),
            "visible_endpoints": sorted(endpoints),
        }
        for mountpoint, endpoints in mount_visibility.items()
        if len(endpoints) > 1
    ]
    cluster_mount_groups.sort(
        key=lambda group: (
            mount_display_priority(group["mountpoint"]),
            group["mountpoint"],
        )
    )
    # This projection groups only mount visibility.  The grouping key is the
    # mountpoint path because the slice answers "where is this path visible?"
    # It must not be interpreted as shared storage identity or ownership.

    shared_storage_candidates = _shared_storage_candidates(operator_relevant_filesystems)

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
        "cluster_mount_groups": cluster_mount_groups,
        "shared_storage_candidates": shared_storage_candidates,
    }
    if include_relationship_count:
        summary["relationship_count"] = len(state.relationships)
    return summary


# Descriptive alias for callers that want to distinguish this operator summary
# from the lower-level v1 State View summary.
build_operator_state_summary = state_summary

__all__ = ["build_operator_state_summary", "state_summary"]
