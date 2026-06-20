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
                _add_candidate(candidates, owner, 0.86, fact, "mount_source_owner")
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
        conflict = None
        reason = "Remote mount source evidence identifies the owner; local mount hosts are treated as consumers."
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
    existing = candidates.get(owner)
    ref = _evidence(fact, role)
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
