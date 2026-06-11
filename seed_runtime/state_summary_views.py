"""Read-only State Summary aggregation helpers.

This module owns the semantic aggregation for the operator State Summary.  CLI
code should render the returned summary, not decide what the summary means.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json
import re
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

_STORAGE_TOPOLOGY_AMBIGUITY_BOUNDARY = (
    "ambiguity != fact; "
    "ambiguity != ownership; "
    "ambiguity != storage identity; "
    "ambiguity != resolved topology"
)

_HISTORICAL_NODE_STYLE_MOUNTPATH = re.compile(r"(?:^|/)node\d+(?:/|$)")

_FILESYSTEM_CATEGORY_ORDER = ("root", "boot", "cluster mounts", "other")
_CLUSTER_MOUNTPOINT_PATTERN = re.compile(r"^/mnt/(?:node|rpi)[^/]*(?:/|$)")
_FILESYSTEM_DETAIL_LIMIT = 10

_ENDPOINT_SUBJECT = re.compile(r"^(?:\[[^]]+\]|[^:]+):[0-9]{1,5}$")
_ENTITY_KIND_ORDER = ("hosts", "services", "endpoints", "storage")
_AVAILABILITY_STATUSES = ("up", "down", "unknown")
_HOST_SCOPED_SUMMARY_PREDICATES = {
    "alias",
    "ansible_host",
    "architecture",
    "availability_status",
    "hostname",
    "ip_address",
    "local_observation_status",
    "os",
    "runtime",
}


def _looks_like_endpoint_subject(subject: str) -> bool:
    """Return whether a subject is safely shaped as a host:port endpoint."""

    if not _ENDPOINT_SUBJECT.fullmatch(subject):
        return False
    try:
        port = int(subject.rsplit(":", 1)[1])
    except ValueError:
        return False
    return 0 < port <= 65535


def _empty_availability_counts() -> dict[str, int]:
    return {status: 0 for status in _AVAILABILITY_STATUSES}


def _entity_summary_row(
    canonical: str,
    entity_aliases: dict[str, set[str]],
    entity_fact_counts: Counter[str],
) -> dict[str, Any]:
    return {
        "name": canonical,
        "alias_count": len(entity_aliases[canonical] - {canonical}),
        "fact_count": entity_fact_counts[canonical],
    }


def _canonical_entity_types(state: State, canonical: str, aliases: set[str]) -> set[str]:
    """Return current entity types for a canonical entity and explicit aliases."""

    types: set[str] = set()
    for entity_id in {canonical, *aliases}:
        types.update(
            entity_type
            for entity_type in state.get_current_entity_types(entity_id)
            if entity_type != "unknown"
        )
        entity = state.entities.get(entity_id)
        if entity is not None and entity.kind != "unknown":
            types.add(entity.kind)
    return types


def _has_host_scoped_summary_evidence(
    state: State, canonical: str, aliases: set[str]
) -> bool:
    """Return whether non-endpoint facts safely support host summary grouping."""

    names = {canonical, *aliases}
    for fact in state.facts.values():
        fact_canonical = state.alias_resolver.canonical(fact.subject_id)
        if fact.subject_id not in names and fact_canonical != canonical:
            continue
        if _looks_like_endpoint_subject(fact.subject_id):
            continue
        if fact.predicate in _HOST_SCOPED_SUMMARY_PREDICATES:
            return True
    return False


def _classify_state_summary_entity(
    state: State, canonical: str, aliases: set[str]
) -> str | None:
    """Classify State Summary rows without crossing endpoint identity boundaries."""

    if _looks_like_endpoint_subject(canonical) or any(
        _looks_like_endpoint_subject(alias) for alias in aliases
    ):
        return "endpoints"

    entity_types = _canonical_entity_types(state, canonical, aliases)
    if "service" in entity_types:
        return "services"
    if "storage" in entity_types:
        return "storage"
    if "host" in entity_types or _has_host_scoped_summary_evidence(
        state, canonical, aliases
    ):
        return "hosts"
    return None


def _filesystem_category(filesystem: dict[str, Any]) -> str:
    """Classify filesystem rows for bounded summary rendering only.

    This is intentionally presentation taxonomy.  It does not assert ownership,
    storage identity, or topology truth.
    """

    mountpoint = str(filesystem.get("mountpoint", ""))
    normalized = mountpoint.rstrip("/") or "/"
    if normalized == "/":
        return "root"
    if (
        normalized == "/media/boot"
        or normalized.startswith("/boot/")
        or normalized == "/boot"
        or normalized.startswith("/System/Volumes/iSCPreboot")
        or "preboot" in normalized.lower()
    ):
        return "boot"
    if _CLUSTER_MOUNTPOINT_PATTERN.search(normalized):
        return "cluster mounts"
    return "other"


def _filesystem_shape_summary(
    filesystems: list[dict[str, Any]],
    *,
    detail_limit: int = _FILESYSTEM_DETAIL_LIMIT,
) -> dict[str, Any]:
    """Return counts and bounded default detail rows for filesystem rendering.

    The full ``filesystems`` list remains available to callers.  This helper
    only chooses what the default top-level State Summary should render.
    """

    counts = {category: 0 for category in _FILESYSTEM_CATEGORY_ORDER}
    categorized: dict[str, list[dict[str, Any]]] = {
        category: [] for category in _FILESYSTEM_CATEGORY_ORDER
    }
    for filesystem in filesystems:
        category = _filesystem_category(filesystem)
        counts[category] += 1
        categorized[category].append(filesystem)

    detail_category = "root"
    detail_rows = categorized["root"][:detail_limit]
    return {
        "counts": {
            category: count
            for category, count in counts.items()
            if count or category in _FILESYSTEM_CATEGORY_ORDER
        },
        "detail_category": detail_category,
        "detail_limit": detail_limit,
        "detail_rows": [dict(row) for row in detail_rows],
        "detail_row_count": len(detail_rows),
        "total_row_count": len(filesystems),
        "classification_basis": (
            "presentation-only mountpoint classification; does not infer "
            "ownership, shared storage identity, or topology truth"
        ),
    }


def _counts_by_field(
    items: list[dict[str, Any]],
    field: str,
    *,
    order: tuple[str, ...] = (),
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(field, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    order_index = {value: index for index, value in enumerate(order)}
    return dict(
        sorted(
            counts.items(),
            key=lambda item: (order_index.get(item[0], len(order_index)), item[0]),
        )
    )


def _storage_topology_summary(
    cluster_mount_groups: list[dict[str, Any]],
    shared_storage_candidates: list[dict[str, Any]],
    storage_topology_ambiguities: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return bounded operator-facing counts for storage topology projections."""

    return {
        "cluster_mount_group_count": len(cluster_mount_groups),
        "shared_storage_candidate_count": len(shared_storage_candidates),
        "shared_storage_candidate_confidence_counts": _counts_by_field(
            shared_storage_candidates,
            "confidence",
            order=("high", "medium", "low"),
        ),
        "storage_topology_ambiguity_count": len(storage_topology_ambiguities),
        "storage_topology_ambiguity_materiality_counts": _counts_by_field(
            storage_topology_ambiguities,
            "materiality",
            order=("high", "medium", "low"),
        ),
    }


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


def _storage_topology_ambiguities(
    filesystems: list[dict[str, Any]],
    cluster_mount_groups: list[dict[str, Any]],
    shared_storage_candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return projection-only unresolved storage interpretation pressure.

    Ambiguities are assembled only from already-projected filesystem
    measurements, mount visibility groups, and shared-storage candidates.  They
    intentionally do not create facts, ownership, storage identity, topology
    truth, issues, or operator clarification requests.
    """

    ambiguity_by_subject: dict[str, dict[str, Any]] = {}

    def ambiguity_for(subject: str) -> dict[str, Any]:
        return ambiguity_by_subject.setdefault(
            subject,
            {
                "subject": subject,
                "reasons": [],
                "candidate_interpretations": [],
                "observable_evidence": [],
                "materiality": "low",
                "materiality_basis": (
                    "smallest safe heuristic from projected visibility and "
                    "candidate evidence; not certainty"
                ),
                "boundary": _STORAGE_TOPOLOGY_AMBIGUITY_BOUNDARY,
            },
        )

    def add_unique(items: list[str], value: str) -> None:
        if value not in items:
            items.append(value)

    endpoint_counts = {
        group["mountpoint"]: group["visible_endpoint_count"]
        for group in cluster_mount_groups
    }
    endpoint_lists = {
        group["mountpoint"]: group["visible_endpoints"]
        for group in cluster_mount_groups
    }

    for group in cluster_mount_groups:
        subject = group["mountpoint"]
        ambiguity = ambiguity_for(subject)
        add_unique(
            ambiguity["reasons"],
            f"mountpath visible on {group['visible_endpoint_count']} endpoints",
        )
        add_unique(
            ambiguity["candidate_interpretations"],
            "multi-endpoint mount visibility",
        )
        add_unique(
            ambiguity["observable_evidence"],
            "cluster_mount_groups.visible_endpoint_count",
        )
        ambiguity["visible_endpoint_count"] = group["visible_endpoint_count"]
        ambiguity["visible_endpoints"] = group["visible_endpoints"]
        ambiguity["materiality"] = "medium"

    for filesystem in filesystems:
        mountpoint = str(filesystem["mountpoint"])
        if not _HISTORICAL_NODE_STYLE_MOUNTPATH.search(mountpoint):
            continue
        ambiguity = ambiguity_for(mountpoint)
        add_unique(ambiguity["reasons"], "mountpath contains node-number path segment")
        add_unique(
            ambiguity["candidate_interpretations"],
            "historical-node-style naming",
        )
        add_unique(
            ambiguity["candidate_interpretations"],
            "possible compatibility path",
        )
        add_unique(ambiguity["observable_evidence"], "filesystem.mountpoint")
        if endpoint_counts.get(mountpoint, 1) > 1:
            ambiguity["materiality"] = "medium"

    for candidate in shared_storage_candidates:
        for mountpath in candidate["mountpaths"]:
            ambiguity = ambiguity_for(mountpath)
            add_unique(
                ambiguity["reasons"],
                "shared-storage candidate exists from matching observable filesystem fields",
            )
            add_unique(
                ambiguity["candidate_interpretations"],
                "possible shared backing",
            )
            add_unique(
                ambiguity["observable_evidence"],
                "shared_storage_candidates.evidence",
            )
            ambiguity.setdefault("shared_storage_candidate_evidence", [])
            for evidence in candidate["evidence"]:
                add_unique(ambiguity["shared_storage_candidate_evidence"], evidence)
            ambiguity["shared_storage_candidate_confidence"] = candidate["confidence"]
            if mountpath in endpoint_counts:
                ambiguity.setdefault("visible_endpoint_count", endpoint_counts[mountpath])
                ambiguity.setdefault("visible_endpoints", endpoint_lists[mountpath])
            if candidate["confidence"] != "low" or mountpath in endpoint_counts:
                ambiguity["materiality"] = "medium"

    return sorted(
        ambiguity_by_subject.values(),
        key=lambda ambiguity: (
            {"medium": 0, "low": 1}.get(ambiguity["materiality"], 2),
            ambiguity["subject"],
        ),
    )


def _storage_projection(state: State) -> dict[str, Any]:
    """Build the explicit storage-focused projection surface from State."""

    current_measurements = [
        fact
        for fact in state.facts.values()
        if is_measurement_predicate(fact.predicate) and not is_fact_expired(fact)
    ]

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
    storage_topology_ambiguities = _storage_topology_ambiguities(
        operator_relevant_filesystems,
        cluster_mount_groups,
        shared_storage_candidates,
    )

    return {
        "fact_count": len(state.facts),
        "measurement_current_sample_count": len(current_measurements),
        "filesystems": filesystem_summary,
        "filesystem_shape_summary": _filesystem_shape_summary(filesystem_summary),
        "cluster_mount_groups": cluster_mount_groups,
        "shared_storage_candidates": shared_storage_candidates,
        "storage_topology_ambiguities": storage_topology_ambiguities,
        "storage_topology_summary": _storage_topology_summary(
            cluster_mount_groups,
            shared_storage_candidates,
            storage_topology_ambiguities,
        ),
    }


def storage_state_projection(state: State) -> dict[str, Any]:
    """Build the explicit storage/filesystem topology projection surface."""

    return _storage_projection(state)


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
    # Default top-entity prominence is based on durable facts only.
    # Current measurement volume must remain queryable and counted elsewhere,
    # but should not make scrape-target endpoints look operator-prominent.
    for fact in durable_facts:
        canonical = state.alias_resolver.canonical(fact.subject_id)
        entity_fact_counts[canonical] += 1
    for entity in state.entities.values():
        canonical = state.alias_resolver.canonical(entity.name)
        entity_aliases[canonical].update({entity.name, *entity.aliases})
        entity_fact_counts.setdefault(canonical, 0)

    entity_kinds = {
        canonical: _classify_state_summary_entity(
            state, canonical, entity_aliases[canonical]
        )
        for canonical in entity_aliases
    }
    ranked_entities = sorted(
        entity_aliases, key=lambda name: (-entity_fact_counts[name], name)
    )
    top_entities_by_kind = {kind: [] for kind in _ENTITY_KIND_ORDER}
    for canonical in ranked_entities:
        kind = entity_kinds[canonical]
        if kind is None or len(top_entities_by_kind[kind]) >= top_entity_limit:
            continue
        top_entities_by_kind[kind].append(
            _entity_summary_row(canonical, entity_aliases, entity_fact_counts)
        )

    # Legacy compatibility field: keep the historical name for callers that have
    # not migrated yet, but make it operator-prominence scoped by excluding
    # scrape-target endpoints from the undifferentiated list. Endpoint visibility
    # is preserved through endpoint summary counts in top_entities_by_kind["endpoints"].
    top_entities = [
        _entity_summary_row(canonical, entity_aliases, entity_fact_counts)
        for canonical in ranked_entities
        if entity_kinds[canonical] in {"hosts", "services", "storage"}
    ][:top_entity_limit]

    availability_by_scope = {
        "endpoint_scrape_availability": _empty_availability_counts(),
        "host_availability": _empty_availability_counts(),
        "service_availability": _empty_availability_counts(),
    }
    scope_by_kind = {
        "endpoints": "endpoint_scrape_availability",
        "hosts": "host_availability",
        "services": "service_availability",
    }
    for canonical in sorted(entity_aliases):
        scope = scope_by_kind.get(entity_kinds[canonical])
        if scope is None:
            continue
        availability_fact = state.get_best_fact(
            canonical, "availability_status", resolve_aliases=False
        )
        status = (
            availability_fact.value
            if availability_fact is not None
            and availability_fact.value in availability_by_scope[scope]
            else "unknown"
        )
        availability_by_scope[scope][status] += 1

    # Legacy compatibility field: retained with the historical all-entity
    # semantics for older callers. New code should read availability_by_scope so
    # endpoint scrape availability is not presented as host or service
    # availability.
    availability = Counter(_empty_availability_counts())
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

    endpoint_availability = availability_by_scope["endpoint_scrape_availability"]
    top_entities_by_kind["endpoints"] = {
        "total": sum(endpoint_availability.values()),
        **endpoint_availability,
    }

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
        "top_entities_by_kind": top_entities_by_kind,
        "availability_by_scope": availability_by_scope,
        "top_entities": top_entities,
        "availability": dict(availability),
    }
    if include_relationship_count:
        summary["relationship_count"] = len(state.relationships)
    return summary


# Descriptive alias for callers that want to distinguish this operator summary
# from the lower-level v1 State View summary.
build_operator_state_summary = state_summary

__all__ = [
    "build_operator_state_summary",
    "state_summary",
    "storage_state_projection",
]
