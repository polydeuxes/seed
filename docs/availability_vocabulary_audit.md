# Executive Summary

Fresh local-host observation currently proves only that Seed can inspect the
machine on which the local observation source is running. It does not prove that
any network interface is healthy, that the host is reachable from another node,
that Prometheus can scrape the host, that any endpoint is accepting traffic, or
that a provider sees the host.

This audit therefore keeps `availability_status` as a projected/evidence-backed
interpretation and rejects direct assignment of `availability_status = up` from
local observation. The smallest safe implementation is a narrow
`local_observation_status = observed` fact emitted by `LocalHostObservationSource`.
Its meaning is limited to successful local read-only inspection by Seed.

No broad availability inference is implemented here. No network probing,
Prometheus dependency, Runtime behavior, or ToolExecutor behavior is added.

# Existing Availability Concepts

## `availability_status`

- **Owner:** canonical predicate vocabulary in `predicate_catalog/core.json`,
  with projection behavior owned by `StateProjector` and current-belief support
  selection.
- **Current shape:** measurement, single cardinality, enum values `up`, `down`,
  and `unknown`.
- **Current evidence:** Prometheus `up` samples are mapped by the predicate
  normalizer into canonical `availability_status` values, with `1 -> up` and
  `0 -> down`.
- **Important scope boundary:** endpoint-shaped subjects such as `host:9100`
  remain endpoint-scoped. Existing projection code intentionally excludes
  `availability_status` from alias-flattened host inference and handles endpoint
  availability with endpoint subjects.

## Endpoint availability

- **Owner:** projected state and impact/unhealthy read views.
- **Current shape:** not a separate predicate. Endpoint availability is expressed
  as `availability_status` facts whose subject looks like a network endpoint.
- **Current evidence:** provider observations such as Prometheus `up` samples on
  endpoint subjects.
- **Current read views:** impact output groups endpoint availability by
  `endpoint_role`; unhealthy output lists current down endpoints.

## Prometheus ingestion and provider visibility

- **Owner:** `PrometheusObservationSource` for collection and
  `PredicateNormalizer`/`PredicateCatalog` for provider-to-canonical mapping.
- **Current shape:** Prometheus is a read-only provider observation source using
  allowlisted safe queries. It emits raw provider facts such as `up`,
  `node_uname_info`, filesystem metrics, `endpoint_role`, and
  `prometheus_instance` alias facts.
- **Current evidence:** successful Prometheus read API results. If Prometheus is
  unreachable, ingestion fails gracefully with zero observations.
- **Current vocabulary gap:** Seed has `prometheus_instance` for identity/provider
  relationship modeling, but no explicit `provider_visibility_status` predicate.
  Today, a Prometheus `up` sample contributes directly to endpoint-scoped
  `availability_status`, not to a separate provider-visibility predicate.

## Local-host observation

- **Owner:** `LocalHostObservationSource`.
- **Previous shape:** local observation emitted `os`, `architecture`,
  `disk_total_bytes`, and `disk_free_bytes` using Python standard-library
  platform and disk APIs.
- **Current evidence after this audit:** local observation also emits
  `local_observation_status = observed` for the local hostname.
- **Boundary:** local observation metadata explicitly states that it does not
  assert network reachability, provider visibility, or availability.

## Impact output

- **Owner:** `scripts/seed_local.py` read-only projected-state formatting.
- **Current shape:** impact output reports the canonical entity, entity types,
  aliases, host-level `availability_status`, endpoint availability by role,
  groups, dependencies, dependents, conflicts, and graph issues.
- **Current change:** impact output now also reports `local_observation_status`
  so local inspection evidence is visible without overloading host availability.

## State projection

- **Owner:** `StateProjector` and associated support/conflict selection helpers.
- **Current shape:** facts are projected from append-only events; current belief
  is selected by support, confidence, source type, recency, and predicate
  cardinality.
- **Availability boundary:** observed `availability_status` is excluded from
  generic alias-collapsed inference and separately considered only for
  endpoint-looking subjects when deriving endpoint health.

## Availability summaries

- **Owner:** `format_entity_impact` and `format_unhealthy` in the CLI read views.
- **Current evidence:** summaries read projected facts only. They do not collect
  new observations, call providers, probe the network, run tools, or mutate
  state.

# Vocabulary Proposal

## Local observability

**Definition:** evidence that Seed successfully inspected the local machine
through a local observation source.

Examples:

- local observation succeeded;
- Seed can inspect host-local platform/disk metadata;
- `local_observation_status = observed`.

Non-claims:

- no network reachability;
- no interface health;
- no Prometheus visibility;
- no remote reachability;
- no service or endpoint availability.

## Process visibility

**Definition:** evidence that a Seed process, observer, or runtime source is
active or visible within a defined scope.

Examples:

- Seed runtime process running;
- observation source active;
- a collector heartbeat observed.

Current status: no dedicated canonical predicate is implemented in this audit.
Do not reuse local host observation as process visibility unless future evidence
specifically observes the process/source lifecycle.

## Network interface status

**Definition:** evidence about a concrete network interface state.

Examples:

- interface up;
- interface down;
- link disconnected;
- isolated.

Current status: no dedicated canonical predicate is implemented in this audit.
Local host observation does not inspect interfaces and must not imply interface
status.

## Endpoint reachability

**Definition:** evidence that a specific endpoint can be reached by a specified
method from a specified vantage point.

Examples:

- TCP reachable from observer X;
- ICMP reachable from observer X;
- HTTP scrape reachable from Prometheus Y.

Current status: endpoint reachability is not represented separately. Existing
endpoint-shaped `availability_status` facts from Prometheus `up` are the closest
implemented concept, but they should be treated as provider-reported endpoint
availability rather than general reachability from all nodes.

## Provider visibility

**Definition:** evidence that an external inventory, monitoring, or provider
system reports or sees an entity.

Examples:

- Prometheus sees host/endpoint;
- inventory contains host;
- provider reports host.

Current status: `prometheus_instance` and inventory identity facts can establish
provider-associated identity/relationship evidence, but there is no dedicated
`provider_visibility_status` predicate. Future provider visibility should be
modeled explicitly rather than inferred from local observation.

## Availability status

**Definition:** projected interpretation of whether an entity or endpoint should
be treated as currently available for a specific scope.

Examples:

- `availability_status = up`;
- `availability_status = down`;
- unknown when evidence is missing, stale, conflicting, or outside scope.

Boundary: availability must be derived from evidence appropriate to the scope. A
local observation alone is insufficient evidence for `availability_status = up`.

# Evidence Sources

| Evidence source | Existing predicates/facts | What it can support today | What it must not imply |
| --- | --- | --- | --- |
| Local host observation | `local_observation_status`, `os`, `architecture`, disk byte observations | Seed inspected the local host with read-only local APIs | Network reachability, provider visibility, endpoint availability, host availability `up` |
| Prometheus read API | raw `up`, canonical `availability_status`, `endpoint_role`, filesystem metrics, `prometheus_instance` | Provider-reported endpoint availability/metrics and monitoring relationships | Universal reachability from every remote node; local host process health |
| Ansible inventory ingestion | `ansible_host`, `ip_address`, `alias`, `group` | Inventory identity and grouping facts | Successful Ansible connection, interface health, service availability |
| State projection | current facts, supports, conflicts, inferred facts | Current belief summaries and endpoint-scoped health inference | New observations, provider calls, network checks, host mutation |
| Impact/unhealthy views | projected facts only | Read-only summaries of existing evidence | Fresh availability checks or reachability probing |

# Availability Derivation Boundaries

Future derivation should remain evidence-backed and scoped. Potential future
rules include:

- Prometheus scrape success for an endpoint may support provider visibility for
  that endpoint from Prometheus's vantage point.
- Remote endpoint TCP success may support endpoint reachability for that target,
  port, protocol, and observer.
- ICMP success may support host/network reachability from a specific observer,
  but not service availability.
- Multiple recent independent positive observations may support projecting
  `availability_status = up` for a declared scope.
- Explicit negative observations such as scrape failure, TCP failure, or provider
  down status may support `availability_status = down` for the same scope.
- Missing, stale, conflicting, or out-of-scope evidence should leave
  `availability_status` unknown rather than invented.

This audit does not implement these derivations.

# Recommended Minimal Local Observation Fact

Add one canonical measurement predicate:

```text
local_observation_status = observed
```

Semantics:

- subject: local hostname observed by `LocalHostObservationSource`;
- value: `observed`;
- source type: `discovery`;
- meaning: Seed successfully inspected local host metadata through local
  read-only APIs;
- negative space: no network reachability, provider visibility, endpoint
  reachability, service health, or availability claim.

Rationale:

- It reuses the existing Observation -> Evidence -> Fact -> State projection
  pipeline.
- It is directly observed and narrow.
- It avoids duplicate endpoint/provider/reachability vocabulary.
- It makes local observability visible in impact output while preserving
  `availability_status: unknown` until appropriate evidence exists.

# Invariants

- Local observation never implies network reachability.
- Local observation never implies network interface health.
- Local observation never implies endpoint reachability.
- Local observation never implies provider visibility.
- Local observation never implies Prometheus visibility.
- Local observation never implies service availability.
- Local observation never implies `availability_status = up`.
- `availability_status` must be evidence-backed and scoped to the evidence that
  supports it.
- Missing availability evidence must project as unknown in read views.
- Impact and unhealthy views must remain read-only projections over existing
  state.
- Availability derivation must not be implemented by `Runtime` or
  `ToolExecutor` side effects.

# Recommended Smallest Next Step

Keep this change limited to documentation plus the narrow local observation fact:

1. Register `local_observation_status` in the canonical predicate catalog.
2. Emit `local_observation_status = observed` from local host observation.
3. Surface the fact in impact output.
4. Test that local observation records the fact, impact output reflects it, and
   `availability_status` remains unknown.
5. Do not add network probing, provider calls, Prometheus requirements,
   Runtime behavior, or ToolExecutor behavior.

Future work, if desired, should separately design scoped predicates for provider
visibility, network interface status, and endpoint reachability before deriving
host-level availability.
