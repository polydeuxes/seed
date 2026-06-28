"""Read-only capability verification inventory.

Capability verification is represented as projected facts and evidence. This
module only interprets already-projected State; it does not execute tools, call
providers, append events, schedule work, or route through Runtime behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

from seed_runtime.evidence_graph import EvidenceNode, build_fact_evidence_view
from seed_runtime.facts import Fact, FactSupport, is_fact_expired
from seed_runtime.predicate_catalog import PredicateCatalog
from seed_runtime.state import State

CAPABILITY_VERIFIED_PREDICATE = "capability_verified"
CapabilityVerificationState = Literal[
    "verified", "unverified", "stale", "provider_reported", "unknown"
]

_VERIFIED_VALUES = {"verified", "true", "yes"}
_PROVIDER_REPORTED_VALUES = {"provider_reported", "provider-reported"}
_UNVERIFIED_VALUES = {"unverified", "false", "no"}


@dataclass(frozen=True)
class CapabilityEvidenceSummary:
    """Compact evidence summary for one capability inventory entry."""

    evidence_id: str
    evidence_type: str
    summary: str
    confidence: float
    observed_at: datetime | None = None


@dataclass(frozen=True)
class CapabilitySupportSummary:
    """FactSupport details exposed without creating a new explanation engine."""

    predicate: str
    value: Any
    confidence: float
    supporting_fact_ids: list[str] = field(default_factory=list)
    source_types: list[str] = field(default_factory=list)
    observed_at: datetime | None = None
    latest_observed_at: datetime | None = None
    expired: bool = False
    expires_at: datetime | None = None


@dataclass(frozen=True)
class CapabilityInventoryEntry:
    """Read-only verification belief for one capability."""

    capability: str
    state: CapabilityVerificationState
    supporting_facts: list[str] = field(default_factory=list)
    supporting_evidence: list[CapabilityEvidenceSummary] = field(default_factory=list)
    support: CapabilitySupportSummary | None = None
    observed_at: datetime | None = None
    latest_observed_at: datetime | None = None
    age_seconds: int | None = None
    reason: str = ""


def build_capability_inventory(
    state: State,
    *,
    predicate_catalog: PredicateCatalog | None = None,
    now: datetime | None = None,
) -> list[CapabilityInventoryEntry]:
    """Return deterministic capability verification inventory from State only.

    The inventory universe is the union of capabilities already present in the
    projection (registered tools, ToolNeeds, and verification fact subjects).
    Verification state is derived from ``capability_verified`` facts and their
    projected FactSupport records. Missing verification facts produce
    ``unverified`` entries; expired verification facts produce ``stale`` entries
    using the existing fact expiry semantics.
    """

    catalog = predicate_catalog or state.predicate_catalog
    if catalog.get(CAPABILITY_VERIFIED_PREDICATE) is None:
        return []

    current_time = _normalize_time(now or datetime.now(timezone.utc))
    capabilities = _inventory_capabilities(state)
    return [
        _entry_for_capability(state, capability, current_time)
        for capability in sorted(capabilities)
    ]


def _inventory_capabilities(state: State) -> set[str]:
    capabilities: set[str] = set()
    capabilities.update(_registered_operation_contract_capabilities(state))
    capabilities.update(_requested_capabilities(state))
    capabilities.update(_observed_verification_capability_subjects(state))
    return capabilities


def _registered_operation_contract_capabilities(state: State) -> set[str]:
    """Capabilities declared by executable operation contracts.

    These names come from registered ``ToolSpec`` records and only describe
    operation-contract metadata. They are not observed evidence that the
    capability is present, available, verified, authorized, or callable in the
    current environment.
    """

    capabilities: set[str] = set()
    for tool in state.tools.values():
        capabilities.update(tool.capabilities or [tool.name])
    return capabilities


def _observed_verification_capability_subjects(state: State) -> set[str]:
    """Capability subjects named by observed verification facts.

    These names come from projected observation/evidence-derived facts. They are
    interpreted as observed verification support only, separate from registered
    executable operation contracts.
    """

    return {
        fact.subject_id
        for fact in state.facts.values()
        if fact.predicate == CAPABILITY_VERIFIED_PREDICATE
    }


def _requested_capabilities(state: State) -> set[str]:
    """Capabilities requested by unresolved needs, separate from evidence and contracts."""

    return {need.capability for need in state.tool_needs.values()}


def _entry_for_capability(
    state: State, capability: str, now: datetime
) -> CapabilityInventoryEntry:
    active_supports = state.get_fact_supports(
        capability, CAPABILITY_VERIFIED_PREDICATE, include_expired=False
    )
    if active_supports:
        support = _best_support(active_supports)
        entry_state = _state_from_value(support.value)
        return _entry_from_support(state, capability, entry_state, support, now)

    expired_supports = state.get_fact_supports(
        capability, CAPABILITY_VERIFIED_PREDICATE, include_expired=True
    )
    stale_supports = [support for support in expired_supports if _support_is_expired(state, support)]
    if stale_supports:
        return _entry_from_support(
            state,
            capability,
            "stale",
            _best_support(stale_supports),
            now,
            reason="verification fact exists but is expired",
        )

    return CapabilityInventoryEntry(
        capability=capability,
        state="unverified",
        reason="no capability_verified fact is present in projected State",
    )


def _entry_from_support(
    state: State,
    capability: str,
    entry_state: CapabilityVerificationState,
    support: FactSupport,
    now: datetime,
    *,
    reason: str | None = None,
) -> CapabilityInventoryEntry:
    facts = _supporting_facts(state, support)
    evidence = _supporting_evidence(state, facts)
    latest = _normalize_time(support.latest_observed_at)
    return CapabilityInventoryEntry(
        capability=capability,
        state=entry_state,
        supporting_facts=[fact.id for fact in facts],
        supporting_evidence=evidence,
        support=CapabilitySupportSummary(
            predicate=support.predicate,
            value=support.value,
            confidence=support.confidence,
            supporting_fact_ids=list(support.supporting_fact_ids),
            source_types=[str(source) for source in support.source_types],
            observed_at=support.observed_at,
            latest_observed_at=support.latest_observed_at,
            expired=support.expired,
            expires_at=support.expires_at,
        ),
        observed_at=support.observed_at,
        latest_observed_at=support.latest_observed_at,
        age_seconds=max(0, int((now - latest).total_seconds())),
        reason=reason or f"derived from {CAPABILITY_VERIFIED_PREDICATE} FactSupport",
    )


def _best_support(supports: list[FactSupport]) -> FactSupport:
    return sorted(
        supports,
        key=lambda support: (
            _state_rank(_state_from_value(support.value)),
            support.confidence,
            _normalize_time(support.latest_observed_at),
            str(support.value),
        ),
        reverse=True,
    )[0]


def _state_rank(state: CapabilityVerificationState) -> int:
    return {
        "verified": 4,
        "provider_reported": 3,
        "stale": 2,
        "unverified": 1,
        "unknown": 0,
    }[state]


def _state_from_value(value: Any) -> CapabilityVerificationState:
    normalized = str(value).strip().lower()
    if normalized in _VERIFIED_VALUES:
        return "verified"
    if normalized in _PROVIDER_REPORTED_VALUES:
        return "provider_reported"
    if normalized in _UNVERIFIED_VALUES:
        return "unverified"
    return "unknown"


def _support_is_expired(state: State, support: FactSupport) -> bool:
    return any(is_fact_expired(fact) for fact in _supporting_facts(state, support))


def _supporting_facts(state: State, support: FactSupport) -> list[Fact]:
    return sorted(
        (
            fact
            for fact_id in support.supporting_fact_ids
            if (fact := state.facts.get(fact_id)) is not None
        ),
        key=lambda fact: fact.id,
    )


def _supporting_evidence(
    state: State, facts: list[Fact]
) -> list[CapabilityEvidenceSummary]:
    nodes: dict[str, EvidenceNode] = {}
    for fact in facts:
        view = build_fact_evidence_view(state, fact.id)
        if view is None:
            continue
        for node in view.evidence:
            nodes.setdefault(node.evidence_id, node)
    return [
        CapabilityEvidenceSummary(
            evidence_id=node.evidence_id,
            evidence_type=node.evidence_type,
            summary=node.summary,
            confidence=node.confidence,
            observed_at=node.created_at,
        )
        for node in sorted(nodes.values(), key=lambda item: item.evidence_id)
    ]


def _normalize_time(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
