# State Summary Endpoint Prominence Audit

## Purpose

This audit investigates why the operator State Summary is surfacing Prometheus
scrape targets such as `10.0.0.1:9100` and `192.168.254.100:9200` as top
entities, and whether that behavior represents an ingestion boundary violation,
a projection issue, or expected output.

This is a documentation-only implementation audit.

It does not modify code, schemas, tests, projections, observations, facts,
relationships, Prometheus ingestion, identity logic, availability logic, or CLI
rendering.

## Input Symptom

A recent State Summary rendered:

```text
Facts: 976
Observations: 948
Requirements: 0
Capabilities: 0
Issues: 0
Projection Version: v1
Last Event: evt_002825

State summary
entities: 66
facts: 976
durable facts: 66
measurement current samples: 910
conflicts: 0
stale facts: 0
graph issues: 0 warnings, 0 errors
observation sources:
  provider: 948
top entities:
  10.0.0.1:8080 (aliases: 0 total; facts: 1)
  10.0.0.1:9100 (aliases: 0 total; facts: 1)
  10.0.0.1:9200 (aliases: 0 total; facts: 1)
  10.0.0.70:9101 (aliases: 0 total; facts: 1)
  10.0.0.70:9200 (aliases: 0 total; facts: 1)
  10.0.0.70:9400 (aliases: 0 total; facts: 1)
  192.168.254.100:9100 (aliases: 0 total; facts: 1)
  192.168.254.100:9200 (aliases: 0 total; facts: 1)
  192.168.254.101:9100 (aliases: 0 total; facts: 1)
  192.168.254.101:9200 (aliases: 0 total; facts: 1)
availability:
  up: 34
  down: 13
  unknown: 19
```

The operator question was:

```text
Do I need entities in my state summary?
Why are they endpoints?
What boundary is being violated or is it a projection issue?
```

## Documents And Code Reviewed

- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/foundational_ontology_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `seed_runtime/state_summary_views.py`
- `tests/test_state_summary_views.py`

## Architectural Baseline

The Prometheus observation boundary states:

```text
Prometheus instance label == contextual scrape-target identifier
Prometheus instance label != host identity by default
```

A `host:port` Prometheus `instance` value safely represents an endpoint or
scrape target subject. It may support endpoint identity, scrape-target identity,
endpoint reachability evidence, endpoint role evidence, or relationship evidence
to a host when additional host evidence exists. It should not by itself support
host identity, application identity, capability ownership, storage identity, or
alias equivalence with a host.

The `up` metric is endpoint-scoped evidence. It means Prometheus's scrape
attempt for a target succeeded or failed from the Prometheus server's vantage
point. It does not mean the host is healthy, the application is available, or the
service is semantically working.

The foundational ontology also preserves the distinction:

```text
Projection is not authority.
```

A projection may communicate selected knowledge, but it must not silently turn
endpoint-scoped evidence into host, service, application, capability, or topology
authority.

## Implementation Finding 1: Endpoint Entities Are Expected Preservation

The endpoint-shaped subjects in the State Summary are not inherently wrong.

Prometheus-derived facts attached to `10.0.0.1:9100` or
`192.168.254.100:9200` are likely preserving the narrowest safe subject for
scrape-target observations.

That is consistent with the Prometheus boundary:

```text
host:port == endpoint / scrape target subject
host:port != host identity by default
```

Therefore, the presence of endpoint entities in preserved state is not, by
itself, a boundary violation.

## Implementation Finding 2: Top Entities Is Flattening Entity Kinds

The current `state_summary()` projection builds one `entity_aliases` set from
all facts and all entities. It then ranks `top_entities` by durable fact count
and name.

The current implementation already avoids measurement-volume dominance by using
only durable facts for ranking. That fixed the earlier problem where filesystem
measurement volume made scrape endpoints look prominent.

However, the projection still has no visible entity-kind or operator-relevance
boundary for `top_entities`.

As a result, if many endpoint entities each have one durable endpoint-scoped
fact, and there are few stronger host or service entities, the summary can render
a top list dominated by scrape targets.

This is a projection issue.

It is not necessarily an ingestion issue.

The problematic shape is:

```text
all canonical entities
    -> one flat top_entities list
        -> sorted by durable fact count and name
            -> endpoint scrape targets appear as top operator entities
```

The projection should distinguish at least:

```text
operator-relevant entities
scrape targets / endpoints
hosts
services / components
storage or filesystem surfaces
unknown / candidate entities
```

The current output is not wrong because endpoint entities exist.

It is misleading because the operator summary presents endpoint entities without
making their endpoint scope explicit.

## Implementation Finding 3: Availability Counts Are Scope-Collapsed

The current `state_summary()` projection computes availability across all
canonical entities in `entity_aliases`.

For each canonical entity, it asks for an `availability_status` fact. If none is
present, it counts the entity as `unknown`.

This produces a single availability count for all entities, mixing:

```text
endpoint scrape availability
host availability
service/application availability
unknown entity availability
```

This conflicts with the Prometheus observation boundary when Prometheus `up`
values are interpreted or displayed as general availability.

Correct scope should be explicit:

```text
endpoint_scrape_availability
    up / down / unknown for scrape targets

host_availability
    only where host-scoped evidence supports host availability

service_availability
    only where service-scoped evidence supports service availability
```

The current availability field appears to be projection scope collapse.

## Implementation Finding 4: Current Tests Preserve The Old Flattening

The state summary tests currently protect the previous durable-fact ranking
behavior but do not protect endpoint/host/service scope separation.

One test intentionally expects a host and an endpoint to both appear in
`top_entities`, with endpoint availability counted in the same availability
summary as host unknownness.

Another test verifies that measurement-heavy filesystem facts do not dominate
`top_entities`, but still expects the endpoint to appear immediately after the
host with zero durable fact count.

These tests are useful for preserving measurement counting and fact preservation,
but they are insufficient for the current boundary.

The missing test coverage is:

```text
endpoint entities remain preserved and queryable
endpoint scrape availability is counted separately from host/service availability
operator top entities do not flatten scrape targets into host/service prominence
scrape-target rows are rendered under an explicit scrape-target/endpoints section
```

## Boundary Classification

### Not A Boundary Violation

Endpoint-shaped entities existing in preserved state:

```text
10.0.0.1:9100
192.168.254.100:9200
```

This is consistent with Prometheus endpoint identity preservation.

### Likely Projection Boundary Violation

Rendering endpoint scrape targets as flat `top_entities` without endpoint scope:

```text
top entities:
  10.0.0.1:9100
  10.0.0.1:9200
```

The projection is communicating endpoint entities as if they are generic operator
entities.

### Likely Availability Boundary Violation

Computing one availability map across all entities:

```text
availability:
  up: 34
  down: 13
  unknown: 19
```

This collapses endpoint scrape reachability, host availability, service
availability, and unknown entity state into one display.

### Potential Naming Issue

The label `top_entities` may now be too broad for the operator summary.

If it remains, it should probably mean operator-relevant entities, not every
canonical entity discovered through provider observations.

Endpoint scrape targets may need their own explicit projection section.

## Recommended Implementation Direction

Do not fix this by discarding endpoint entities.

Do not fix this by promoting endpoints to hosts.

Do not fix this by aliasing `host:port` to host names.

Do not fix this by hiding Prometheus evidence.

Instead, adjust projection semantics.

### Preferred Shape

```text
state_summary:
  entity_count: all canonical entities, or explicitly named all_entity_count
  operator_entities: host/service/storage/operator-relevant durable entities
  scrape_targets: endpoint scrape target summary
  availability_by_scope:
    endpoint_scrape:
      up: N
      down: N
      unknown: N
    host:
      up: N
      down: N
      unknown: N
    service:
      up: N
      down: N
      unknown: N
```

### Smaller First Step

A smaller first implementation step could be:

```text
1. Keep entity_count unchanged.
2. Rename or supplement top_entities with operator_top_entities.
3. Add scrape_targets or endpoint_summary.
4. Split availability into endpoint_scrape_availability and leave legacy availability only if compatibility requires it.
5. Add regression tests proving endpoint entities are preserved but not treated as top operator entities.
```

## Suggested Regression Tests

Add tests proving:

1. Prometheus endpoint facts remain preserved and queryable.
2. Endpoint scrape availability appears under endpoint/scrape-target scope.
3. Host availability is not inferred from endpoint `up`.
4. Endpoint scrape targets do not dominate operator top entities.
5. The summary remains able to report endpoint counts without collapsing endpoint identity into host identity.

Example scenario:

```text
facts:
  endpoint_a:9100 availability_status=up
  endpoint_b:9100 availability_status=down
  endpoint_c:9200 availability_status=up
  host115 os=linux
  host115 local_observation_status=observed

expected:
  operator_top_entities begins with host115
  endpoint scrape targets are summarized separately
  host availability is unknown unless host-scoped evidence exists
  endpoint_scrape_availability is up=2 down=1
```

## Direct Answers

### Do entities belong in State Summary?

Yes, but not as one undifferentiated flat list.

The operator State Summary needs entities, but it should distinguish operator
entities from scrape targets, endpoints, storage surfaces, candidates, and other
source-scoped subjects.

### Why are the top entities endpoints?

Because Prometheus-derived endpoint subjects are preserved as canonical entities,
and `state_summary()` builds `top_entities` from the flattened set of all
canonical entities. The ranking uses durable fact counts, but it does not apply
an entity-kind or operator-relevance boundary.

### What boundary is being violated?

The likely violation is projection scope collapse:

```text
endpoint scrape target identity
    displayed as generic top operator entity
```

and:

```text
endpoint scrape availability
    counted with generic entity availability
```

The ingestion boundary may be correct if Prometheus facts attach to endpoint
subjects. The projection boundary is where the output becomes misleading.

### Is this a projection issue?

Yes.

The issue is primarily in the operator State Summary projection, especially the
flat `top_entities` list and single `availability` map.

## Non-Goals

This audit does not recommend:

- deleting endpoint entities;
- aliasing endpoints to hosts;
- treating Prometheus `up` as host availability;
- creating storage identity from filesystem metrics;
- changing schemas without further implementation review;
- hiding provider observations;
- changing ingestion before confirming whether facts are already scoped to
  endpoints.

## Final Finding

The State Summary should continue to preserve endpoint entities, but it should
not present endpoint scrape targets as undifferentiated operator top entities.

The current behavior appears to be a projection issue: preserved endpoint-scoped
Prometheus claims are being rendered through a generic entity summary surface
that lacks endpoint/host/service scope separation.

The safest next implementation work is to split the State Summary projection into
operator-relevant entity prominence and endpoint scrape-target visibility, with
availability counted by scope rather than across all entities.
