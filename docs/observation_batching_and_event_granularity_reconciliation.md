# Observation Batching And Event Granularity Reconciliation

## Purpose

This reconciliation investigates the architectural unit of preservation when a single collection activity produces many observed items.

The motivating example was:

```text
seed --observe-local-host
```

which eventually completed and reported approximately 10,000 observations.

This raised the question:

```text
If a package scan discovers 200 packages, is that one event, 200 events, one piece of evidence, or 200 pieces of evidence?
```

This reconciliation defines boundaries before any batching, transaction, storage, or performance implementation work occurs.

## Central Finding

Collection activity, observation batch, observation, evidence, and ledger event are distinct concepts.

They must not be collapsed merely because batching would improve performance.

The useful architecture is:

```text
Collection Activity
        ↓
Observation Batch
        ↓
Observations
        ↓
Evidence
        ↓
Claims / Facts / Relationships
```

A collection run may be one activity.

It may produce one batch.

That batch may contain many observations.

Each observation may support separate evidence and claims.

The storage layer may persist them using fewer transactions without changing their conceptual identity.

## Key Distinctions

### Collection Activity

A collection activity is the work performed to acquire observations.

Examples:

```text
local host observation run
package inventory scan
/etc/hosts read
Prometheus scrape query
SSH host identity collection
```

A collection activity is not itself all of the observations it produced.

### Observation Batch

An observation batch is a bounded result set produced by one collection activity or one acquisition boundary.

Examples:

```text
all package observations from one dpkg status parse
all hosts-file observations from one /etc/hosts read
all mount observations from one /proc/mounts read
```

A batch preserves shared provenance:

```text
source
collector
run id
observed_at
reader / transport
input path or query
```

without collapsing individual observations.

### Observation

An observation is one source-scoped observed statement or measurement.

Examples:

```text
package nginx is installed
/etc/hosts line 4 maps 192.168.1.10 to example_host
mount /mnt/merged exists
listener tcp/22 is present
```

Observations must remain individually addressable when they support different claims.

### Evidence

Evidence is support for a claim.

Evidence may reference:

```text
one observation
multiple observations
an observation batch
collection metadata
```

but evidence is not identical to collection activity.

### Ledger Event

A ledger event is the persistence record used to preserve change/history.

A ledger event may record:

```text
one observation
multiple observations
a batch envelope
```

without changing the conceptual count of observations.

Therefore:

```text
Ledger Event
        != Observation
```

## Package Scan Example

If a package scan discovers 200 packages:

```text
1 collection activity
1 package observation batch
200 package observations
200 potential package evidence paths
200 package claims or facts, if promoted
```

This does not require 200 SQLite commits.

It may or may not require 200 ledger events depending on the event model.

The architectural requirement is that each package observation remains traceable to:

```text
the package scan
its source text/record
its collection run
the emitted observation
any promoted claim/fact
```

## /etc/hosts Example

If `/etc/hosts` contains 20 meaningful mappings:

```text
1 collection activity
1 hosts-file observation batch
20+ structured observations, depending on mapping/name granularity
```

The batch may preserve:

```text
source_path=/etc/hosts
reader=local
observed_at
collector=LocalHostObservationSource
```

Each observation preserves:

```text
line_number
address
name
role on line
```

## Prometheus Example

A Prometheus query may return many samples.

```text
1 query activity
1 query result batch
N metric observations
N candidate measurement claims
```

The query itself is not host truth.

The returned samples remain individually scoped to metric labels, scrape target, timestamp, and source.

## Batching Does Not Decide Semantics

Performance batching is an implementation concern.

Semantic batching is an architectural concern.

They may align, but they are not the same.

```text
Transaction Batch
        != Observation Batch
```

A transaction may persist many observations.

That does not mean the observations become one observation.

## Event Granularity

Event granularity should be chosen to preserve history and replay semantics.

Possible event shapes:

```text
one event per observation
one event per observation batch
one event per collection activity with embedded observations
hybrid: batch event + addressable child observations
```

The correct choice depends on replay, provenance, deduplication, performance, and audit requirements.

This reconciliation does not prescribe the implementation shape.

It establishes the boundary:

```text
storage batching must not erase observation granularity
```

## Relationship To Execution Status

A collection activity may emit execution status.

Example:

```text
Collecting package observations...
Writing observations 100/200...
```

Execution status is not the observation batch.

Execution status is activity visibility.

Observation batch is acquisition result structure.

```text
Execution Status
        != Observation Batch
```

## Relationship To Evidence

Evidence should be able to point to the specific support needed.

For some claims, batch-level evidence may be appropriate.

For others, individual observation-level evidence is required.

Example:

```text
Claim: package nginx is installed
Support: nginx package observation
```

not merely:

```text
Support: package scan happened
```

But for:

```text
Claim: package inventory was collected at time T
```

batch-level evidence may be sufficient.

## Relationship To Projection

Projection may aggregate observations.

Aggregation does not change preservation granularity.

Example:

```text
installed packages: 200
```

is a projection over many observations.

It does not mean there was only one observation.

## Architectural Invariants

```text
Collection Activity != Observation
Observation Batch != Observation
Transaction Batch != Observation Batch
Ledger Event != Observation
Evidence != Collection Activity
Execution Status != Observation Batch
Projection Aggregate != Preservation Unit
Batching != Semantic Collapse
```

## Non-Goals

This reconciliation does not:

- prescribe a storage schema;
- prescribe SQLite transaction behavior;
- prescribe ledger event shape;
- prescribe event batch implementation;
- change observation ingestion;
- change evidence construction;
- change replay semantics;
- optimize performance.

## Implementation Implications

Before optimizing ingestion performance, implementation should determine:

```text
what is the semantic batch?
what is the persistence batch?
what remains individually addressable?
what evidence IDs point to?
what replay requires?
```

A future implementation may batch database commits while still preserving individual observations and evidence paths.

A future implementation may introduce collection run IDs or batch IDs.

A future implementation may add batch-level status emissions.

None of those should collapse individual observations into one fact or one truth claim.

## Final Finding

A package scan discovering 200 packages should be understood as:

```text
one collection activity
one observation batch
many observations
many possible evidence paths
many possible promoted claims/facts
```

The storage system may persist them efficiently, but architectural provenance must remain granular enough to explain which observed item supports which claim.

The next safe implementation audit is to inspect current ingestion and ledger behavior to determine whether it already conflates observation granularity with event granularity or simply commits too often.