# Repository invariants

These invariants describe the accepted Seed architecture. They are intended to be
readable documentation today and executable architecture checks over time.

## Runtime invariants

- `Runtime` is canonical.
- `RuntimeLoop` must not exist in active runtime paths.
- `request_tool` records and resolves a capability gap; it does not execute.

## Execution invariants

- `CapabilityCatalog` is read-only capability/provider metadata; it does not
  execute.
- `CapabilityRecommendation.operation` is provider/handoff metadata, not a
  verification result.

## Projection invariants

- `EventLedger` owns append-only events.
- `ProjectionStore` owns cached projected-state snapshots.
- `StateProjector` owns projection from events to current state.
- Projection replays events in ledger append/insertion order, not timestamp order.
- Event, observation, evidence, fact, support, and projection timestamps are
  provenance, freshness, expiry, or cache metadata; they must not be treated as a
  supported projection-ordering or as-of query mechanism.
- `ProjectionStore` stores latest-current snapshots only and invalidates by latest
  event ID/projection identity mismatch, not timestamp comparison.
- `ProjectionStore` must not append events.
- `EventLedger` must not store projection snapshots.
- Expiry and stale views must not mutate stored facts, lower stored confidence, or
  append refresh events.
- Measurement predicates expose latest-current samples by default; retained
  measurement history is bounded debug/read-only history, not current truth
  arbitration.

## Capability invariants

- `ToolNeed` is a capability gap, not an executable tool.
- Capability resolution is read-only.
- Capability resolution never implies verification.
- ToolNeed creation never implies verification.
- Known capability catalog metadata never implies verification.
- Provider recommendation never implies verification.
- CapabilityRecommendation operation metadata never implies verification.
- A `verify_*` operation name never implies verification.
- Evidence-like objects are not verified capabilities without a scoped
  verification status model.

## Capability extension invariants

- Observation must not imply execution.
- Observation must not imply availability.
- Local configuration must not imply availability, reachability, health, internet
  access, or provider visibility.
- Observing a hostname must not imply DNS validity.
- Observing a hostname must not imply reachability.
- Observing a hostname must not imply availability.
- Observing a machine ID must not imply a global uniqueness guarantee.
- Observing a boot ID must not imply availability.
- Observing a FQDN must not imply DNS success or reachability.
- Observing a listening port must not imply endpoint availability.
- Observing a configured network interface must not imply carrier, assigned
  address, neighbor reachability, gateway reachability, or host availability.
- Observing an interface `operstate=up` must not imply `availability_status=up`.
- Observing an assigned `ip_address` must not imply endpoint availability, remote
  routability, duplicate-address success, or network reachability.
- Observing a default route or `default_gateway` must not imply gateway existence,
  gateway reachability, packet forwarding, DNS success, or internet access.
- Observing a `dns_resolver`, `dns_resolver_stub`, or
  `dns_resolver_upstream` must not imply resolver reachability, DNS query
  success, or DNS availability.
- Observing a local network segment must not imply neighbor existence, subnet
  occupancy, gateway reachability, or scanning.
- Observing kernel, CPU, or memory description facts must not imply host health,
  performance adequacy, workload status, availability, reachability,
  supportability, or provider visibility.
- Observing `memory_total_bytes` must not imply memory pressure, free memory, or
  currently available memory.
- Observation must not imply management.
- Observing a package must not imply ownership.
- Observing a process must not imply management.
- Observing a container must not imply orchestration.
- Capability resolution must not imply verification.
- Write access must not be required for observation.
- Prefer least-privileged observation sources.
- Observation must not claim more than the selected source directly supports.
- Read-only observation must remain separate from mutation and provider calls.

## Capability verification invariants

- Capability verification is not implemented in the current runtime.
- Requested capability, known capability, candidate capability, and
  provider-recommended capability are not synonyms for verified capability.
- Unverified is the default state for requested, known, candidate, and
  provider-recommended capabilities unless a future scoped verification model
  proves otherwise.
- Stale verification must not be treated as current positive verification.
- Failed verification requires accepted negative evidence; it is not merely the
  absence of positive evidence.
- Future verification should be modeled as a separate scoped read model with
  explicit status, evidence, target, freshness, and boundary semantics.
- `CapabilityCatalog` remains read-only metadata and must not become a
  verification authority by catalog presence alone.

## Historical/quarantine invariants

- `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are not Core MVP artifacts.
- If retained, `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and
  `ExecutionAuthorization` are historical or legacy compatibility artifacts only.
- Historical planning artifacts must not become active runtime orchestration,
  scheduling, retry, selection, or execution systems.
