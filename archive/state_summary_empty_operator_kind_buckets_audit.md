# State Summary Empty Operator Kind Buckets Audit

## Purpose

This audit investigates the follow-up State Summary output after endpoint
prominence was separated into `top_entities_by_kind` and endpoint availability
was scoped under `availability_by_scope`.

This is a documentation-only implementation audit.

It does not modify code, schemas, tests, projections, observations, facts,
relationships, Prometheus ingestion, entity classification, or CLI rendering.

## Input Symptom

After the endpoint prominence cleanup, State Summary rendered:

```text
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

top entities by kind:
  hosts:
    (none)
  services:
    (none)
  endpoints:
    total: 47
    up: 34
    down: 13
    unknown: 0
  storage:
    (none)

availability by scope:
  endpoint_scrape_availability:
    up: 34
    down: 13
    unknown: 0
  host_availability:
    up: 0
    down: 0
    unknown: 0
  service_availability:
    up: 0
    down: 0
    unknown: 0
```

The operator question was whether endpoint totals in `top_entities_by_kind` are
redundant with `availability_by_scope`, or whether the output is communicating
different information.

## Files Reviewed

- `seed_runtime/state_summary_views.py`
- `docs/state_summary_endpoint_prominence_audit.md`
- `docs/prometheus_observation_boundary_reconciliation.md`
- `docs/foundational_ontology_reconciliation.md`

## Current Implementation Shape

The current implementation now classifies summary entities before rendering.

Classification uses:

```text
endpoint-shaped subject -> endpoints
explicit/current entity type service -> services
explicit/current entity type storage -> storage
explicit/current entity type host -> hosts
selected host-scoped predicates on non-endpoint subjects -> hosts
otherwise -> unclassified / omitted from top_entities_by_kind
```

The relevant host-scoped predicate allowlist currently includes:

```text
alias
ansible_host
architecture
availability_status
hostname
ip_address
local_observation_status
os
runtime
```

Endpoint subjects are detected by host:port shape and classified as endpoints.
The code intentionally refuses to treat endpoint-shaped facts as host-scoped
evidence.

The summary then builds:

```text
top_entities_by_kind
availability_by_scope
legacy top_entities
legacy availability
```

Endpoint `top_entities_by_kind["endpoints"]` is replaced with a count/status
summary derived from `availability_by_scope["endpoint_scrape_availability"]`.

## Finding 1: Endpoint Redundancy Is Mostly Presentational

The endpoint section currently says:

```text
top entities by kind:
  endpoints:
    total: 47
    up: 34
    down: 13
    unknown: 0
```

The scoped availability section says:

```text
availability by scope:
  endpoint_scrape_availability:
    up: 34
    down: 13
    unknown: 0
```

When every endpoint is assigned an availability bucket, the endpoint total is the
sum of the availability counts:

```text
total = up + down + unknown
```

Therefore, in the current output, the endpoint subsection is mostly redundant
with `endpoint_scrape_availability`.

However, the two sections are conceptually different:

```text
top_entities_by_kind.endpoints
    answers: how many endpoint entities are in this operator summary bucket?

availability_by_scope.endpoint_scrape_availability
    answers: what is the scrape availability distribution for endpoint entities?
```

The redundancy is not itself the main architectural problem.

The more important signal is that all non-endpoint buckets are empty.

## Finding 2: Empty Host/Service/Storage Buckets Are The Stronger Signal

The summary reports:

```text
entities: 66
durable facts: 66
```

but:

```text
hosts: none
services: none
storage: none
```

This means the operator summary successfully stopped endpoint crowding, but it
also revealed that Seed currently has no safely classified operator-prominent
hosts, services, or storage entities under the current classification rules.

That can mean one of two things:

1. The source state truly contains mostly endpoint-scoped Prometheus facts and
   little or no host/service/storage evidence.
2. The classifier is too strict or lacks the source-specific interpretation and
   routing needed to promote existing evidence into host/service/storage-facing
   summary buckets.

The State Summary output alone cannot distinguish those cases.

## Finding 3: Classification Is Conservative And Probably Correct For Endpoints

The current implementation correctly avoids this unsafe inference:

```text
host:port endpoint
    -> host identity
```

That is consistent with the Prometheus boundary:

```text
Prometheus instance label == contextual scrape-target identifier
Prometheus instance label != host identity by default
```

The absence of hosts is preferable to silently promoting endpoints into hosts.

The problem is not that hosts are missing from the output at any cost.

The problem is that the summary does not yet explain whether the host bucket is
empty because:

```text
no host evidence exists
```

or because:

```text
host evidence exists but is not yet interpreted, routed, or promoted into a host
summary bucket
```

## Finding 4: The Output Needs An Evidence Gap Signal

Now that endpoint noise has been bounded, the operator summary needs a way to
communicate empty operator buckets as information rather than silence.

The current output says:

```text
hosts:
  (none)
```

A more useful operator-facing interpretation would distinguish:

```text
hosts:
  none safely classified
  endpoint scrape targets observed: 47
  host identity evidence: missing / not promoted / unavailable
```

This should not promote endpoints to hosts.

It should expose the gap.

The boundary-preserving shape is:

```text
hosts:
  total: 0
  classification_status: no safely classified host entities
  hint: endpoint scrape targets are preserved separately; host identity requires non-endpoint evidence
```

or an equivalent concise rendering.

## Finding 5: Endpoint Totals May Belong Under Availability Or Endpoint Summary, Not Top Entities

The current label remains slightly awkward:

```text
top entities by kind:
  endpoints:
    total: 47
```

Because endpoints are no longer being shown as top named entities.

They are now an aggregate endpoint summary.

This is a naming/projection clarity issue, not a preservation issue.

Possible future refinement:

```text
top entities by kind:
  hosts:
  services:
  storage:

endpoint scrape targets:
  total:
  up:
  down:
  unknown:
```

However, if compatibility or structural consistency requires endpoints to remain
under `top_entities_by_kind`, the summary should make clear that endpoint rows
are aggregate counts, not named top entities.

## Boundary Classification

### Correct Boundary Preservation

```text
endpoint facts remain endpoint-scoped
endpoint up is counted as endpoint scrape availability
host availability is not inferred from endpoint availability
endpoint names are no longer listed as operator-prominent top entities
```

### Remaining Projection Ambiguity

```text
hosts/services/storage are empty without explaining whether the absence is due to missing evidence, missing interpretation, or missing classification rules
```

### Presentational Redundancy

```text
top_entities_by_kind.endpoints status counts duplicate availability_by_scope.endpoint_scrape_availability when every endpoint has a status bucket
```

The redundancy is acceptable short-term if it helps readers understand endpoint
counts in the same area where endpoint entities used to appear.

It should not distract from the larger empty-bucket signal.

## Recommended Next Implementation Direction

Do not loosen endpoint-to-host rules merely to populate hosts.

Do not infer host availability from endpoint `up`.

Do not remove endpoint preservation.

Instead, add explicit empty-bucket/gap communication.

Recommended next step:

```text
1. Keep endpoint scrape summary aggregate.
2. Keep host/service/storage buckets conservative.
3. Add a concise classification/gap hint when a bucket is empty.
4. Add or expose counts for unclassified durable entities, if any.
5. Audit source facts to determine whether host/service/storage evidence exists but is not being routed into classification.
```

Possible projection addition:

```text
entity_classification_summary:
  hosts:
    total: 0
    status: none_safely_classified
  services:
    total: 0
    status: none_safely_classified
  endpoints:
    total: 47
    status: scrape_targets_observed
  storage:
    total: 0
    status: none_safely_classified
  unclassified:
    total: N
```

This would let State Summary answer:

```text
What did Seed classify?
What did Seed refuse to classify?
What evidence is missing?
```

without crossing identity or availability boundaries.

## Suggested Regression Tests

Add or update tests proving:

1. Empty host bucket remains empty when only endpoint-shaped Prometheus facts
   exist.
2. Empty host bucket includes a boundary-preserving hint or classification status.
3. Endpoint scrape availability remains scoped to endpoints.
4. Host availability remains zero/unknown only for safely classified hosts, not
   endpoint-derived status.
5. Unclassified durable entities, if present, are counted or inspectable without
   being promoted into hosts/services/storage.
6. Adding explicit host-scoped evidence such as `os`, `hostname`, or
   `local_observation_status` on a non-endpoint subject causes that subject to
   appear under hosts.

## Direct Answers

### Is endpoint count redundant with endpoint availability?

Mostly yes in the current output.

The endpoint total is the sum of endpoint scrape availability buckets.

But the two sections still answer different conceptual questions: endpoint
entity population versus endpoint availability distribution.

### Is redundancy the main problem?

No.

The stronger signal is that host, service, and storage buckets are empty despite
66 entities and 66 durable facts.

### What should be investigated next?

Investigate whether those durable facts are all endpoint-scoped or whether
host/service/storage evidence exists but is not being interpreted, routed,
promoted, or classified into the operator summary.

### Is this an ingestion issue?

Not proven.

It may be correct ingestion with conservative projection.

The next audit should inspect actual durable fact predicates and subjects in the
state output or event ledger.

## Final Finding

The endpoint aggregate is a reasonable improvement over listing every endpoint,
but the current State Summary has exposed the next boundary: the operator view
needs to explain empty host/service/storage buckets and distinguish missing
operator-entity evidence from conservative refusal to promote endpoint evidence.

The redundancy between endpoint totals and endpoint availability is secondary.
The primary issue is now classification visibility: Seed should show what it can
safely classify, what remains endpoint-scoped, and what remains unclassified
without collapsing endpoints into hosts or scrape availability into host
availability.
