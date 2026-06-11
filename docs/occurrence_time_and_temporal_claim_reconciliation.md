# Occurrence Time And Temporal Claim Reconciliation

## Purpose

This document performs a documentation-only reconciliation of occurrence time,
observation time, source sample time, knowledge time, preservation time, event
timestamps, and temporal claims.

It preserves the boundary exposed by the temporal authority audit:

```text
Occurrence time is usually not directly observed.

Occurrence time is a supported temporal claim that may be revised as new evidence arrives.
```

This document makes no code, schema, runtime behavior, ingestion, projection, or
test changes.

## Authoritative Context

This reconciliation is subordinate to the repository's existing temporal,
evidence, learning, contradiction, federation, and Prometheus boundary documents.
Repository authority wins over prompt language.

The relevant existing findings are:

- Seed already separates event timestamps from observation timestamps.
- Projection replay is ordered by append order, not by event timestamp.
- `Event.timestamp` is a preservation timestamp in the current implementation,
  not automatically an external occurrence timestamp.
- `Observation.observed_at`, `Evidence.observed_at`, `Fact.observed_at`, and
  fact support timestamps are provenance timestamps used by support aggregation,
  measurement latest-current behavior, and deterministic tie-breakers.
- A timestamp is not self-authorizing: it has a source, clock, scope, meaning,
  and authority context.
- Prometheus vector results contain a sample timestamp and a sample value, but
  current Prometheus ingestion documents a gap where the sample timestamp is not
  preserved as source temporal metadata.
- Cross-Seed sharing is evidence transfer, not truth transfer.
- Learning changes Seed's justified knowledge; it does not mean the world changed
  again.
- Contradiction may exist before Seed discovers or exposes it.

## Core Finding

```text
The world changes once.
Seed's understanding of when it changed may improve many times.
```

Occurrence time should not be collapsed into the first time Seed observed,
learned, preserved, imported, or projected evidence of the occurrence.

For many real-world changes, Seed does not directly observe the instant of
change. Seed receives observations, source samples, logs, operator assertions,
remote reports, and preserved events. From that support, Seed may derive a
supported temporal claim about when the external occurrence happened.

That claim can become narrower, stronger, weaker, superseded, or disputed as new
support arrives. The occurrence did not move. Seed's supported understanding of
when it happened changed.

## Definitions

### Occurrence Time

Occurrence time is when the thing in external reality happened.

Examples:

```text
A service became unavailable.
A host rebooted.
A configuration file changed.
A deploy completed.
```

Seed usually does not directly know occurrence time. It may infer, derive, or
accept an asserted occurrence-time claim from support.

Occurrence time is therefore best represented as a supported temporal claim, not
as a universally available single timestamp field.

### Observation Time

Observation time is when a source observed, sampled, read, reported, or collected
some evidence.

Examples:

```text
Prometheus scraped a target.
A local adapter read /etc/hosts.
An SSH command collected process state.
An operator submitted a report.
```

Observation time may come from the source clock, Seed's collection clock, an
import payload, or an operator assertion. It is evidence about when observation
happened, not automatic proof of when the external occurrence happened.

### Source Sample Time

Source sample time is the timestamp supplied by the upstream source for the
sample or record.

Examples:

```text
Prometheus value[0] sample timestamp
log record timestamp
remote Seed source timestamp
sensor sample timestamp
```

A source sample timestamp answers when the source says the sample is from. It
may be highly useful support for an occurrence-time claim, but it is still a
source temporal assertion with provenance and clock authority.

### Knowledge Time

Knowledge time is when Seed became justified in using particular support.

It is close to ingestion, evidence construction, approval, or import time, but it
is not occurrence time. A condition may have been true long before Seed became
justified in believing or using evidence for it.

### Preservation Time

Preservation time is when Seed recorded something in its append-only history or
ledger.

In the current implementation, `Event.timestamp` is the preservation timestamp
for a Seed event. It records when Seed preserved the event, not necessarily when
the external reality occurred.

### Event Timestamp

Event timestamp is the timestamp on a Seed event.

It should be interpreted as Seed-facing event preservation time unless a future
schema explicitly records additional temporal provenance. It is not a generic
external occurrence-time field.

### Temporal Claim

A temporal claim is a supported statement about time.

An occurrence-time claim may have shapes such as:

```text
exact timestamp
lower bound
upper bound
interval
best estimate
unknown
```

Useful temporal-claim metadata may include:

```text
confidence
support
derivation method
source clocks
source clock trust
source timestamp raw value
normalization method
claim author or deriving component
claim creation time
claim supersession or revision links
```

The exact schema is future work. The important reconciliation is that occurrence
time is a claim over support, not just a field copied from the newest timestamp
Seed happens to possess.

### Temporal Claim Revision

A temporal claim revision is a later supported change to Seed's temporal claim.

Revision can narrow an interval, widen an interval, replace an exact estimate
with an interval, add confidence, reduce confidence, attach additional support,
or mark the claim disputed.

A temporal claim revision is not a revision of reality. It is a revision of
Seed's supported understanding.

## Required Boundary

Seed must preserve these non-collapses:

```text
Occurrence Time != Observation Time
Occurrence Time != Source Sample Time
Occurrence Time != Knowledge Time
Occurrence Time != Preservation Time
Occurrence Time Claim != Observation
Occurrence Time Claim != Event
Event Timestamp != External Occurrence Time
Prometheus Sample Time != Occurrence Time
Log Timestamp != Occurrence Time
Temporal Claim Revision != Reality Revision
Support Increase != Occurrence Change
Reality Change != Learning Change
```

The same source timestamp may support an occurrence-time claim. It does not
become occurrence time merely by being source-provided.

The same observation may support an occurrence-time claim. It does not become the
occurrence itself.

The same event may preserve evidence or a claim. It does not become the external
change.

## Motivating Example: Service Unavailability

A service becomes unavailable.

Initial Prometheus evidence:

```text
last successful scrape: 10:49:45
first failed scrape: 10:50:15
```

Supported temporal claim:

```text
outage occurred sometime between 10:49:45 and 10:50:15
```

Later host log evidence:

```text
last application log entry: 10:49:59.500
```

Revised temporal claim:

```text
outage occurred sometime between 10:49:59.500 and 10:50:15
```

Interpretation:

```text
The occurrence did not change.
Seed's supported temporal claim changed.
The earlier claim was not erased; it reflected the support available at the time.
```

The outage happened once. Prometheus support first bounded it between the last
successful scrape and the first failed scrape. Later log support narrowed the
lower bound. Seed learned more about the same outage.

The revised claim should preserve provenance for both the earlier Prometheus
support and the later log support. If the earlier claim is superseded, it remains
historically meaningful because it describes what Seed was justified in claiming
before the additional evidence arrived.

## Temporal Claim Shapes

Occurrence-time claims should allow more than a single timestamp.

Common shapes include:

| Shape | Meaning | Example |
| --- | --- | --- |
| Exact timestamp | Support asserts or derives one instant strongly enough to use as exact. | `occurred_at = 10:50:02.123` |
| Lower bound | Support only proves the occurrence happened after a time. | `after 10:49:45` |
| Upper bound | Support only proves the occurrence happened before a time. | `before 10:50:15` |
| Interval | Support bounds the occurrence between two times. | `10:49:59.500..10:50:15` |
| Best estimate | Support suggests a likely instant but does not prove exactness. | `estimate 10:50:00, derived from heartbeat midpoint` |
| Unknown | Support proves the occurrence or condition, but not when it occurred. | `time unknown` |

A future model may also attach confidence, support identities, derivation method,
source clocks, authority context, and revision lineage. Those details should make
claims more inspectable without pretending that every occurrence has a directly
observable timestamp.

## Prometheus-Specific Guidance

Prometheus provides a particularly important boundary because a Prometheus vector
sample contains both a sample timestamp and a sample value.

```text
Prometheus sample timestamp answers:
  when Prometheus says the sample is from

Seed collection timestamp answers:
  when Seed queried/received the sample

Event timestamp answers:
  when Seed preserved the resulting event
```

None of those automatically equals occurrence time.

For example, `up == 0` at a Prometheus sample timestamp means Prometheus reports
that the scrape target was not successfully scraped for that sample. It does not
by itself prove the application occurrence time, host failure time, service
semantic outage time, or user-visible incident time.

Prometheus sample timestamps should be preserved as source support. Seed
collection timestamps should remain available separately. Event timestamps should
remain preservation timestamps. Occurrence-time claims should be derived later
from the available support rather than invented at collection time.

## Logs And Other Source Timestamps

Log timestamps also require the same boundary.

A log timestamp answers when the logging source says a record was emitted,
written, received, or timestamped, depending on the logging system. It may be a
strong clue for occurrence time, but it is not occurrence time by definition.
Clock skew, buffering, batching, delayed writes, local timezone conversion,
forwarder delay, and parser normalization can all affect interpretation.

Therefore:

```text
Log Timestamp != Occurrence Time
```

A host log entry such as `last application log entry: 10:49:59.500` may support a
lower bound for a service outage claim. It should not erase Prometheus evidence
or be treated as a direct observation of the precise outage instant unless the
log semantics support that stronger claim.

## Learning Connection

The learning pattern is:

```text
same outage
new evidence
better temporal claim
```

The world did not change again. Seed learned more.

This matters because Seed's learning history should distinguish reality changes
from knowledge changes. A new observation, imported report, log line, approval,
or derived claim can change Seed's justified state without implying a new
external occurrence.

A later temporal claim may be more accurate, more precise, or better supported.
It should remain traceable to the learning step that made the revision justified.

## Contradiction Parallel

The same shape appears in contradiction handling:

```text
Contradiction may exist before discovery.
Occurrence may happen before observation.
Temporal understanding may improve after occurrence.
```

Seed discovering a contradiction does not create the contradiction in the world.
Seed observing evidence of an occurrence does not necessarily mark when the
occurrence happened. Seed revising a temporal claim does not move the occurrence.

Discovery time, observation time, and learning time are important because they
explain Seed's epistemic state. They must not be collapsed into external reality
time.

## Federation Implication

Remote Seeds may share multiple kinds of time:

```text
source timestamps
remote observation times
remote knowledge times
remote temporal claims
local receipt times
```

These must remain distinct.

A remote temporal claim remains a claim with provenance, not local occurrence
truth. The receiving Seed has local evidence that a remote Seed made or exported
a temporal claim. It may use that claim as support according to local trust,
authority, verification, and federation policy, but it should preserve the remote
claim's origin, support path, source clocks, remote preservation context, transfer
path, and local receipt time.

Cross-Seed import therefore adds at least one additional temporal layer:

```text
source occurrence support
remote Seed observation or knowledge time
remote Seed temporal claim time
remote Seed preservation/export time
local Seed receipt/import time
local Seed claim revision time, if promoted or rederived locally
```

Treating a remote temporal claim as local occurrence truth would collapse
evidence transfer into truth transfer, which the federation reconciliation rejects.

## Implementation Implications

Future implementation should first preserve source timestamps before deriving
occurrence-time claims.

The following should be preserved as support:

```text
Prometheus sample timestamps
log timestamps
remote Seed timestamps
operator asserted times
```

Occurrence-time claims should be derived later from support, not invented at
collection time.

A safe sequence is:

1. Preserve raw and normalized source timestamps with their source, clock, and
   authority context.
2. Preserve Seed collection, receipt, knowledge, and event preservation times
   separately.
3. Derive occurrence-time claims from support with an explicit claim shape.
4. Preserve derivation method, confidence or support strength when available, and
   source identifiers.
5. Revise or supersede temporal claims when new support arrives, without erasing
   the prior claim's historical support context.

This keeps current event and observation semantics intact while creating a path
to better temporal reasoning.

## Non-Goals

This document does not:

```text
define temporal schema
define interval algorithms
define outage inference algorithms
define confidence calculations
modify Prometheus ingestion
implement source timestamp preservation
change Event.timestamp
change Observation.observed_at semantics
```

It also does not define projection-as-of APIs, event replay changes, fact
selection changes, federation trust policy, contradiction algorithms, or
Prometheus subject identity changes.

## Final Finding

Occurrence time is best understood as a supported temporal claim rather than a
universally observable timestamp.

The claim may be revised as new evidence arrives.

The world changes once; Seed's understanding of when it changed may improve many
times.
