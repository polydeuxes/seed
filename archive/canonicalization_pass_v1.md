# Executive Summary

Canonicalization Pass v1 promotes the highest-value remaining architectural
knowledge from prior audits into canonical owner documents. This pass is limited
to temporal semantics, contradiction semantics, and local observation
negative-space boundaries.

This is a documentation-only canonicalization pass. It does not create a new
audit, reconciliation, characterization, runtime behavior, execution behavior,
provider behavior, observation behavior, or LLM reasoning path.

# Temporal Canonicalization

Promoted temporal semantics from `docs/temporal_reasoning_audit.md` into
`docs/state.md` and `docs/invariants.md`.

Canonicalized semantics:

- State is latest-current projected state, not a general temporal reasoner.
- Projection order is ledger append/insertion order, not timestamp order.
- Timestamps are provenance, freshness, expiry, or cache metadata; they do not
  define projection replay order or a supported as-of query.
- Durable facts remain retained in projected state unless expired or absent from
  replay; durable single-cardinality disagreements can remain conflicting rather
  than being deleted, superseded, or resolved.
- Multi-cardinality durable facts can have multiple current values without those
  values being conflicts solely because they are multiple.
- Measurement predicates expose latest-current samples by default, while bounded
  measurement history is debug/read-only history rather than current truth
  arbitration.
- Expired facts remain stored but are excluded from default current/support and
  conflict queries; stale views and refresh recommendations are read-time views
  and do not mutate facts, lower stored confidence, or append events.
- `ProjectionStore` owns latest-current snapshots only and invalidates by latest
  event ID/projection identity mismatch, not timestamp comparison.
- As-of event projection, as-of timestamp projection, belief timelines,
  why-then explanations, and semantic what-changed timelines remain unsupported
  by current canonical behavior.

# Contradiction Canonicalization

Promoted contradiction semantics from `docs/contradiction_handling_audit.md` into
`docs/state.md`, `docs/invariants.md`, and
`docs/explanation_contract_vocabulary.md`.

Canonicalized semantics:

- Seed has read-only disagreement surfaces, not a unified truth-arbitration
  engine.
- `FactConflict` is the projected-state conflict model for disagreements among
  facts for a resolved subject, predicate, and dimensions scope.
- Projection-level conflicts apply to non-expired facts by default,
  non-measurement predicates, non-multi-cardinality predicates, the same
  alias-canonical subject/predicate/dimensions, and more than one distinct value.
- `FactConflict` may expose `winning_value` and `best_fact_id` when existing
  projection support selects an unambiguous best fact; otherwise all grouped
  facts can remain conflicting with no winner.
- Standalone `Contradiction` remains a separate read-only detector over exact
  subject/predicate exclusive-predicate groups and optional evidence graph data.
- `GraphValidationIssue` is graph-read-model issue reporting, not fact truth
  resolution; it does not remove relationships, alter entity types, rewrite
  aliases, or block projection.
- Explanation conflict exposure can attach matching `FactConflict` and competing
  beliefs for single-cardinality predicates; there is no `why_not()` API or
  negative-belief model.
- Confidence penalties are confined to the separate read-only confidence
  projection and do not change `Fact.confidence`, `FactSupport.confidence`,
  current-belief selection, EventLedger data, or State projection behavior.
- Conflict lifecycle terms remain narrow: stale is expiry/read-time filtering;
  superseded is not a fact/support/evidence/conflict lifecycle; disputed is not a
  first-class state; uncertain is represented through existing confidence,
  ambiguity, unsupported, unknown, or no-current-belief statuses.

# Local Observation Boundary Canonicalization

Promoted local observation negative-space boundaries from
`docs/local_network_observation_audit.md` into
`docs/capability_extension_methodology.md` and `docs/invariants.md`.

Canonicalized boundaries:

- Local configuration is evidence of local configuration only.
- Local observation must not infer availability, reachability, health, internet
  access, provider visibility, management, ownership, orchestration, or
  verification.
- `network_interface` means the local OS exposes an interface name; it does not
  imply carrier, address assignment, remote reachability, host availability, or
  neighbor existence.
- `interface_operstate` means the local kernel reports an operational state; it
  does not imply gateway reachability, internet access, endpoint health, or
  `availability_status=up`.
- Assigned `ip_address` means an address is configured locally; it does not imply
  external routability, duplicate-address success, endpoint availability, or
  packet exchange.
- `default_gateway` means the local route table has a default route/gateway
  entry; it does not imply gateway existence, gateway reachability, packet
  forwarding, DNS success, or internet access.
- `dns_resolver`, `dns_resolver_stub`, and `dns_resolver_upstream` mean local
  resolver configuration names a resolver; they do not imply resolver
  reachability, successful DNS queries, recursion, authority, DNS availability,
  or internet access.
- A future or existing local network segment fact must not imply neighbor
  existence, subnet occupancy, scanning, gateway presence, or broadcast/multicast
  success.
- Missing local facts should render as unknown in read models when needed; the
  absence of evidence must not become `down`, availability failure, or a negative
  operational fact unless separately observed.

# Ownership Clarifications

Canonical ownership is now explicit for the covered topics:

- Temporal State semantics live in `docs/state.md`, with compact architectural
  invariants in `docs/invariants.md`.
- Conflict and contradiction State semantics live in `docs/state.md`, with
  explanation vocabulary ownership for conflict terminology in
  `docs/explanation_contract_vocabulary.md`.
- Local observation negative-space rules live in
  `docs/capability_extension_methodology.md`, with compact guardrail invariants
  in `docs/invariants.md`.

The source audit documents remain source/history documents only. The promoted
semantics above now have canonical homes.

# Promotion Summary

| Topic | Source | Destination |
| --- | --- | --- |
| Temporal Projection Semantics | `docs/temporal_reasoning_audit.md` | `docs/state.md`, `docs/invariants.md` |
| Timestamp Non-Ordering | `docs/temporal_reasoning_audit.md` | `docs/state.md`, `docs/invariants.md` |
| Durable Fact Retention | `docs/temporal_reasoning_audit.md`, `docs/contradiction_handling_audit.md` | `docs/state.md` |
| Measurement Latest-Current Semantics | `docs/temporal_reasoning_audit.md`, `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/invariants.md` |
| Stale Read-Time Filtering | `docs/temporal_reasoning_audit.md`, `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/invariants.md` |
| `ProjectionStore` Latest-Current Boundary | `docs/temporal_reasoning_audit.md` | `docs/state.md`, `docs/invariants.md` |
| `FactConflict` Semantics | `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/explanation_contract_vocabulary.md` |
| Standalone `Contradiction` Semantics | `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/explanation_contract_vocabulary.md` |
| `GraphValidationIssue` Distinction | `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/explanation_contract_vocabulary.md` |
| Explanation Conflict Attachment | `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/explanation_contract_vocabulary.md` |
| Confidence-Penalty Boundary | `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/explanation_contract_vocabulary.md` |
| Conflict Lifecycle Distinctions | `docs/contradiction_handling_audit.md` | `docs/state.md`, `docs/explanation_contract_vocabulary.md` |
| Resolver Non-Inference | `docs/local_network_observation_audit.md` | `docs/capability_extension_methodology.md`, `docs/invariants.md` |
| Gateway Non-Inference | `docs/local_network_observation_audit.md` | `docs/capability_extension_methodology.md`, `docs/invariants.md` |
| Interface Non-Inference | `docs/local_network_observation_audit.md` | `docs/capability_extension_methodology.md`, `docs/invariants.md` |
| Observation-vs-Management Boundary | `docs/local_network_observation_audit.md` | `docs/capability_extension_methodology.md`, `docs/invariants.md` |

# Remaining Promotion Backlog

No genuinely remaining promotion backlog is identified for the intentionally
limited Canonicalization Pass v1 scope: temporal semantics, contradiction
semantics, and local observation negative-space boundaries now have canonical
homes.

Items outside this pass, such as repository self-observation design or future
as-of temporal features, remain outside scope and are not added as new backlog by
this document.
