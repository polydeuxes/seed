"""Read-only operational ownership discrepancy diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from seed_runtime.models import Fact
from seed_runtime.state import State

OwnershipKind = Literal["storage", "service"]
ConflictClass = Literal[
    "missing_owner",
    "multiple_candidate_owners",
    "owner_not_observed",
    "consumer_mistaken_as_owner",
    "shared_visibility_not_ownership",
    "mount_source_conflict",
    "remote_export_attribution_missing",
    "service_endpoint_conflict",
    "insufficient_evidence",
]


@dataclass(frozen=True)
class OwnershipEvidenceRef:
    fact_id: str
    support_ids: list[str]
    subject: str
    predicate: str
    value: Any
    role: str


@dataclass
class OwnershipCandidate:
    owner: str
    confidence: float
    evidence: list[OwnershipEvidenceRef] = field(default_factory=list)
    label: str = "candidate"


@dataclass(frozen=True)
class OwnershipDiscrepancyRow:
    subject: str
    kind: OwnershipKind
    candidate_owner: str | None
    confidence: float
    evidence_count: int
    conflict: ConflictClass | None
    reason: str
    evidence: list[OwnershipEvidenceRef]
    label: str = "candidate"


_STORAGE_PREDICATES = {
    "mountpoint",
    "mount_point",
    "filesystem_mountpoint",
    "filesystem_mounted_at",
    "mounted_at",
    "mount_source",
    "mount_source_host",
    "mount_source_path",
    "mount_attribution_status",
    "filesystem_source",
    "device",
    "device_id",
    "filesystem_device",
    "filesystem_uuid",
    "fs_uuid",
    "export_path",
    "shared_path",
    "nfs_export",
    "smb_share",
    "storage_owner_candidate",
}
_HOST_PREDICATES = {"host", "hostname", "node", "endpoint", "instance"}
_SERVICE_PREDICATES = {
    "listens_on",
    "listen_endpoint",
    "service_endpoint",
    "service_port",
    "port",
    "process_host",
    "container_host",
    "prometheus_instance",
    "prometheus_target",
    "service_config_host",
}


def build_ownership_discrepancies(
    state: State, *, subject_filter: str | None = None
) -> list[OwnershipDiscrepancyRow]:
    facts = list(state.facts.values())
    storage_subjects = _storage_subjects(facts, subject_filter)
    service_subjects = _service_subjects(facts, subject_filter)
    rows: list[OwnershipDiscrepancyRow] = []
    for subject in sorted(storage_subjects):
        rows.extend(_diagnose_storage_subject(subject, facts))
    for subject in sorted(service_subjects):
        rows.extend(_diagnose_service_subject(subject, facts))
    if subject_filter and not rows:
        rows.append(
            OwnershipDiscrepancyRow(
                subject=subject_filter,
                kind="storage",
                candidate_owner=None,
                confidence=0.0,
                evidence_count=0,
                conflict="missing_owner",
                reason="No storage or service ownership evidence was found for the requested subject.",
                evidence=[],
            )
        )
    return rows


_CAPABILITY_NEEDS_BY_CONFLICT: dict[
    tuple[OwnershipKind, ConflictClass], list[tuple[str, str, str]]
] = {
    ("service", "insufficient_evidence"): [
        ("local_listener", "tcp_listen_inventory", "non_root_partial_root_full"),
        ("process_inventory", "process_inventory", "partial_root_full"),
        ("container_inventory", "container_inventory", "partial_root_full"),
    ],
    ("service", "owner_not_observed"): [
        (
            "listener_process_inventory",
            "listener_process_inventory",
            "partial_root_full",
        ),
        ("container_port_mapping", "container_port_mapping", "partial_root_full"),
        ("container_inventory", "container_inventory", "partial_root_full"),
    ],
    ("storage", "missing_owner"): [
        ("mount_source", "mount_source_inventory", "non_root_partial_root_full"),
        ("export_visibility", "export_visibility_inventory", "partial_root_full"),
    ],
    ("storage", "remote_export_attribution_missing"): [
        ("nfs_export_inventory", "nfs_export_inventory", "partial_root_full"),
        ("smb_share_inventory", "smb_share_inventory", "partial_root_full"),
        (
            "remote_storage_export_inventory",
            "remote_storage_export_inventory",
            "partial_root_full",
        ),
    ],
    ("service", "missing_owner"): [
        ("local_listener", "tcp_listen_inventory", "non_root_partial_root_full"),
        ("service_manager", "systemd_unit_inventory", "partial_root_full"),
    ],
}


def diagnostic_capability_need_records(
    row: OwnershipDiscrepancyRow,
) -> list[dict[str, Any]]:
    """Return diagnostic-only capability needs implied by an ownership row."""

    if row.conflict is None:
        return []
    needs = _CAPABILITY_NEEDS_BY_CONFLICT.get((row.kind, row.conflict), [])
    return [
        {
            "diagnostic_name": "ownership_discrepancies",
            "diagnostic_subject": row.subject,
            "diagnostic_conflict": row.conflict,
            "needed_evidence": needed_evidence,
            "candidate_capability": candidate_capability,
            "privilege_level": privilege_level,
        }
        for needed_evidence, candidate_capability, privilege_level in needs
    ]


def ownership_discrepancies_json(
    rows: list[OwnershipDiscrepancyRow],
) -> list[dict[str, Any]]:
    return [
        {
            "subject": row.subject,
            "kind": row.kind,
            "candidate_owner": row.candidate_owner,
            "confidence": row.confidence,
            "evidence_count": row.evidence_count,
            "conflict": row.conflict,
            "reason": row.reason,
            "label": row.label,
            "evidence": [ref.__dict__ for ref in row.evidence],
        }
        for row in rows
    ]


def format_ownership_discrepancies(rows: list[OwnershipDiscrepancyRow]) -> str:
    header = "Subject | Kind | Candidate Owner | Confidence | Evidence Count | Conflict | Reason"
    lines = [header]
    for row in rows:
        lines.append(
            " | ".join(
                [
                    row.subject,
                    row.kind,
                    row.candidate_owner or "-",
                    f"{row.confidence:.2f}",
                    str(row.evidence_count),
                    row.conflict or "-",
                    row.reason,
                ]
            )
        )
    return "\n".join(lines)


def _storage_subjects(facts: list[Fact], subject_filter: str | None) -> set[str]:
    subjects = {f.subject_id for f in facts if f.predicate in _STORAGE_PREDICATES}
    if subject_filter:
        return {subject_filter} if subject_filter in subjects else set()
    return subjects


def _service_subjects(facts: list[Fact], subject_filter: str | None) -> set[str]:
    subjects = {f.subject_id for f in facts if f.predicate in _SERVICE_PREDICATES}
    if subject_filter:
        return {subject_filter} if subject_filter in subjects else set()
    return subjects


def _diagnose_storage_subject(
    subject: str, facts: list[Fact]
) -> list[OwnershipDiscrepancyRow]:
    related = [f for f in facts if f.subject_id == subject]
    candidates: dict[str, OwnershipCandidate] = {}
    consumer_hosts: set[str] = set()
    source_hosts: set[str] = set()
    mountpoints = {
        str(f.value)
        for f in related
        if f.predicate
        in {
            "mountpoint",
            "mount_point",
            "filesystem_mountpoint",
            "mounted_at",
            "filesystem_mounted_at",
        }
    }
    identities = {
        str(f.value)
        for f in related
        if f.predicate
        in {"device", "device_id", "filesystem_device", "filesystem_uuid", "fs_uuid"}
    }

    for fact in related:
        if fact.predicate in _HOST_PREDICATES:
            owner = str(fact.value)
            consumer_hosts.add(owner)
            _add_candidate(candidates, owner, 0.72, fact, "local_mount_observed")
        if fact.predicate in {"mount_source", "filesystem_source"}:
            owner = _host_from_source(fact.value)
            if owner:
                source_hosts.add(owner)
                _add_candidate(
                    candidates, owner, 0.86, fact, "remote_mount_source_observed"
                )
        if fact.predicate == "mount_source_host":
            owner = str(fact.value)
            source_hosts.add(owner)
            _add_candidate(
                candidates, owner, 0.88, fact, "remote_mount_source_host_observed"
            )
        if fact.predicate in {
            "export_path",
            "shared_path",
            "nfs_export",
            "smb_share",
            "storage_owner_candidate",
        }:
            owner = (
                str(fact.value)
                if fact.predicate == "storage_owner_candidate"
                else subject
            )
            _add_candidate(candidates, owner, 0.70, fact, "export_or_candidate")

    for other in facts:
        if other.subject_id == subject:
            continue
        if other.predicate in _HOST_PREDICATES and mountpoints:
            other_mounts = {
                str(f.value)
                for f in facts
                if f.subject_id == other.subject_id
                and f.predicate
                in {
                    "mountpoint",
                    "mount_point",
                    "filesystem_mountpoint",
                    "mounted_at",
                    "filesystem_mounted_at",
                }
            }
            if mountpoints & other_mounts:
                host = str(other.value)
                consumer_hosts.add(host)
                _add_candidate(candidates, host, 0.45, other, "same_mountpoint_visible")
        if other.predicate in _HOST_PREDICATES and identities:
            other_ids = {
                str(f.value)
                for f in facts
                if f.subject_id == other.subject_id
                and f.predicate
                in {
                    "device",
                    "device_id",
                    "filesystem_device",
                    "filesystem_uuid",
                    "fs_uuid",
                }
            }
            if identities & other_ids:
                host = str(other.value)
                consumer_hosts.add(host)
                _add_candidate(
                    candidates, host, 0.45, other, "same_filesystem_identity_visible"
                )

    return _rows_for_candidates(
        subject, "storage", candidates, consumer_hosts, source_hosts
    )


def _diagnose_service_subject(
    subject: str, facts: list[Fact]
) -> list[OwnershipDiscrepancyRow]:
    related = [f for f in facts if f.subject_id == subject]
    candidates: dict[str, OwnershipCandidate] = {}
    endpoint_only: list[OwnershipEvidenceRef] = []
    for fact in related:
        if fact.predicate in {"process_host", "container_host", "host"}:
            _add_candidate(
                candidates, str(fact.value), 0.84, fact, "process_or_container_observed"
            )
        elif fact.predicate in {
            "listens_on",
            "listen_endpoint",
            "service_endpoint",
            "service_port",
            "port",
        }:
            owner = _host_from_source(fact.value)
            if owner:
                _add_candidate(
                    candidates, owner, 0.72, fact, "service_listens_on_endpoint"
                )
            else:
                endpoint_only.append(_evidence(fact, "service_endpoint_only"))
        elif fact.predicate in {"prometheus_instance", "prometheus_target"}:
            endpoint_only.append(_evidence(fact, "prometheus_endpoint_only"))
        elif fact.predicate == "service_config_host":
            _add_candidate(
                candidates, str(fact.value), 0.65, fact, "service_config_source"
            )
    listener_refs = _matching_local_listener_refs(endpoint_only, facts)
    for ref in listener_refs:
        _add_candidate_ref(
            candidates, ref.subject, 0.55, ref, "local_listener_confirmed"
        )
    if listener_refs:
        rows = _rows_for_candidates(subject, "service", candidates, set(), set())
        return [
            OwnershipDiscrepancyRow(
                row.subject,
                row.kind,
                row.candidate_owner,
                row.confidence,
                row.evidence_count,
                "owner_not_observed" if row.conflict is None else row.conflict,
                (
                    "Local listener evidence confirms a socket is present, but process/container "
                    "owner attribution is unavailable."
                    if row.conflict is None
                    else row.reason
                ),
                row.evidence,
                row.label,
            )
            for row in rows
        ]
    if not candidates and endpoint_only:
        return [
            OwnershipDiscrepancyRow(
                subject,
                "service",
                None,
                0.0,
                len(endpoint_only),
                "insufficient_evidence",
                "Only endpoint/target evidence exists; no host, process, container, or local listener evidence was observed.",
                endpoint_only,
            )
        ]
    return _rows_for_candidates(subject, "service", candidates, set(), set())


def _rows_for_candidates(subject, kind, candidates, consumers, sources):
    if not candidates:
        return [
            OwnershipDiscrepancyRow(
                subject,
                kind,
                None,
                0.0,
                0,
                "missing_owner",
                "No ownership candidate could be inferred from existing facts.",
                [],
            )
        ]
    ordered = sorted(candidates.values(), key=lambda c: (-c.confidence, c.owner))
    conflict = None
    reason = "Provisional owner inferred from existing cluster evidence."
    if kind == "storage" and len(sources) == 1 and ordered[0].owner in sources:
        conflict = "remote_export_attribution_missing"
        reason = (
            "Remote mount source evidence supports this candidate owner and treats "
            "local mount hosts as consumers, but export attribution remains unverified."
        )
    elif len(ordered) > 1 and ordered[1].confidence >= 0.45:
        conflict = (
            "mount_source_conflict"
            if kind == "storage" and len(sources) > 1
            else "multiple_candidate_owners"
        )
        reason = "Multiple plausible candidate owners were inferred; ambiguity is intentionally exposed."
    elif (
        kind == "storage"
        and consumers
        and sources
        and any(c.owner in consumers - sources for c in ordered[1:])
    ):
        conflict = "consumer_mistaken_as_owner"
        reason = (
            "A locally visible mount also appears to be consumed from a remote source."
        )
    best = ordered[0]
    return [
        OwnershipDiscrepancyRow(
            subject,
            kind,
            best.owner,
            best.confidence,
            len(best.evidence),
            conflict,
            reason,
            best.evidence,
            best.label,
        )
    ]


def _add_candidate(
    candidates, owner: str, confidence: float, fact: Fact, role: str
) -> None:
    _add_candidate_ref(candidates, owner, confidence, _evidence(fact, role), role)


def _add_candidate_ref(
    candidates, owner: str, confidence: float, ref: OwnershipEvidenceRef, role: str
) -> None:
    ref = OwnershipEvidenceRef(
        ref.fact_id, ref.support_ids, ref.subject, ref.predicate, ref.value, role
    )
    existing = candidates.get(owner)
    if existing is None:
        candidates[owner] = OwnershipCandidate(owner, confidence, [ref])
    else:
        existing.confidence = max(existing.confidence, confidence)
        existing.evidence.append(ref)


def _evidence(fact: Fact, role: str) -> OwnershipEvidenceRef:
    return OwnershipEvidenceRef(
        fact.id,
        list(fact.evidence_ids),
        fact.subject_id,
        fact.predicate,
        fact.value,
        role,
    )


def _host_from_source(value: Any) -> str | None:
    if isinstance(value, dict):
        for key in ("host", "node", "endpoint", "server"):
            if value.get(key):
                return str(value[key])
        return None
    text = str(value)
    if "//" in text:
        rest = text.split("//", 1)[1]
        return rest.split("/", 1)[0].split(":", 1)[0] or None
    if ":" in text and not text.startswith("/"):
        return text.split(":", 1)[0].strip("[]") or None
    return None


def _matching_local_listener_refs(
    endpoint_refs: list[OwnershipEvidenceRef], facts: list[Fact]
) -> list[OwnershipEvidenceRef]:
    endpoints = [_endpoint_host_port(ref.value) for ref in endpoint_refs]
    endpoints = [item for item in endpoints if item is not None]
    if not endpoints:
        return []
    listener_facts = [
        fact
        for fact in facts
        if fact.predicate in {"listening_socket", "listening_endpoint"}
    ]
    matches: list[OwnershipEvidenceRef] = []
    seen: set[str] = set()
    for fact in listener_facts:
        listener = _listener_protocol_address_port(fact)
        if listener is None:
            continue
        _protocol, address, port = listener
        for endpoint_host, endpoint_port in endpoints:
            if endpoint_port != port:
                continue
            if address in {"0.0.0.0", "::", endpoint_host, "127.0.0.1", "::1"}:
                if fact.id not in seen:
                    matches.append(_evidence(fact, "local_listener_confirmed"))
                    seen.add(fact.id)
                break
    return matches


def _endpoint_host_port(value: Any) -> tuple[str | None, int] | None:
    text = str(value)
    if "//" in text:
        text = text.split("//", 1)[1].split("/", 1)[0]
    if text.startswith("[") and "]:" in text:
        host, port_text = text[1:].split("]:", 1)
    elif ":" in text:
        host, port_text = text.rsplit(":", 1)
    else:
        return None
    try:
        return host.strip("[]") or None, int(port_text)
    except ValueError:
        return None


def _listener_protocol_address_port(fact: Fact) -> tuple[str | None, str, int] | None:
    protocol = fact.dimensions.get("protocol") if fact.dimensions else None
    address = fact.dimensions.get("address") if fact.dimensions else None
    port_text = fact.dimensions.get("port") if fact.dimensions else None
    if address and port_text:
        try:
            return protocol, address, int(port_text)
        except ValueError:
            return None
    text = str(fact.value)
    parts = text.split()
    endpoint = parts[-1] if parts else text
    if endpoint.startswith("[") and "]:" in endpoint:
        address, port_text = endpoint[1:].split("]:", 1)
    elif ":" in endpoint:
        address, port_text = endpoint.rsplit(":", 1)
    else:
        return None
    try:
        return (parts[0] if len(parts) > 1 else protocol), address, int(port_text)
    except ValueError:
        return None
