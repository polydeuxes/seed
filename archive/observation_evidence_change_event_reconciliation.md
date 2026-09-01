# Observation Evidence Change Event Reconciliation

## Purpose

This reconciliation connects two architectural regions that were previously explored from different directions.

Acquisition-oriented work established:

```text
Collection Activity
Observation Batch
Observation
Evidence
```

Preservation-oriented work established:

```text
Change
Event
```

The missing question is:

```text
How does observed support become preserved change?
```

## Central Finding

Observation, evidence, change, and event are distinct architectural concepts.

They participate in the same lifecycle but should not be collapsed.

The reconciled shape is:

```text
Collection Activity
        ↓
Observation Batch
        ↓
Observation
        ↓
Evidence
        ↓
Claim / Relationship
        ↓
Change
        ↓
Event
```

Not every observation becomes evidence.

Not every evidence path supports a claim.

Not every claim produces change.

Not every change produces a distinct event.

The distinctions matter because acquisition, justification, preservation, and history answer different questions.

## Observation

Observation answers:

```text
What was observed?
```

Examples:

```text
Package nginx is present.
Listener tcp/22 exists.
/etc/hosts contains a mapping.
Prometheus returned a metric sample.
```

Observation is acquisition.

Observation is not justification.

Observation is not change.

Observation is not history.

## Evidence

Evidence answers:

```text
What support exists?
```

Evidence connects observations to later reasoning.

Examples:

```text
Package observation supports package claim.
Hosts-file observation supports identity reasoning.
Prometheus sample supports measurement claim.
```

Evidence is support.

Evidence is not observation.

Evidence is not change.

## Claim And Relationship Formation

Claims and relationships answer:

```text
What is justified?
```

Evidence may justify:

```text
host identity claim
package claim
service claim
relationship claim
```

The claim layer is where support becomes explainable understanding.

## Change

Change answers:

```text
What became different?
```

Examples:

```text
new claim appeared
claim confidence changed
relationship added
relationship removed
identity resolution changed
projection selection changed
```

Change is not observation.

A repeated observation may produce no change.

Example:

```text
Package nginx observed yesterday.
Package nginx observed today.
```

The second observation may produce additional support while producing no change.

## Event

Event answers:

```text
What should be preserved historically?
```

Events preserve meaningful transitions and history.

Events are preservation-oriented.

Observations are acquisition-oriented.

This is the key distinction.

## Repeated Observation Example

Consider:

```text
Package scan
        ↓
200 package observations
```

Suppose all 200 packages were already known.

The run still produced:

```text
observation
support
provenance
```

but may produce:

```text
no new change
```

Therefore:

```text
Observation Count
        != Change Count
```

and:

```text
Observation Count
        != Event Count
```

## Contradiction Example

Suppose:

```text
Observation A
supports Debian

Observation B
supports Ubuntu
```

The observations themselves are not the contradiction.

The contradiction emerges when justified structures are compared.

Possible sequence:

```text
Observation
        ↓
Evidence
        ↓
Claims
        ↓
Contradiction
        ↓
Change
        ↓
Event
```

## Identity Example

Recent Host Observation work provides a useful example.

```text
hostname
machine-id
boot-id
fqdn
/etc/hosts mappings
```

These are observations.

They become evidence for identity reasoning.

Identity reasoning may justify claims.

A change occurs only if identity understanding changes.

An event preserves that change.

## Prometheus Example

```text
Prometheus sample
        ↓
Observation
        ↓
Evidence
        ↓
Measurement claim
```

If the measurement matches existing understanding:

```text
support increases
change may not occur
```

Therefore repeated measurements do not necessarily imply repeated changes.

## Batching Implications

This reconciliation clarifies the batching discussion.

The system may batch:

```text
collection
observations
transactions
```

without changing:

```text
evidence structure
change semantics
event semantics
```

The preservation unit should be determined by change and event requirements.

Not by acquisition volume.

## Relationship To Execution Status

Execution status exists alongside this chain.

Example:

```text
Collecting package observations...
```

Execution status explains activity.

Observation explains acquisition.

Evidence explains support.

Change explains difference.

Event explains preservation.

These are separate architectural roles.

## Architectural Invariants

```text
Collection Activity != Observation
Observation Batch != Observation
Observation != Evidence
Evidence != Claim
Claim != Change
Change != Event

Observation Count != Change Count
Observation Count != Event Count

Support Increase != Change
Repeated Observation != Change
Repeated Observation != Event

Execution Status != Observation
Execution Status != Change
Execution Status != Event
```

## Non-Goals

This reconciliation does not:

- define storage schema;
- define replay implementation;
- define event persistence format;
- define transaction batching;
- define contradiction implementation;
- define claim promotion implementation.

## Implementation Implications

Future performance work should measure:

```text
observation volume
evidence volume
change volume
event volume
```

independently.

The architecture should not assume they are equal.

Future batching should optimize persistence without redefining:

```text
support
change
history
```

## Final Finding

Observation, evidence, change, and event are four distinct architectural layers.

Observation acquires.

Evidence supports.

Change records difference.

Event preserves history.

The critical discovery is that additional observations may increase support without producing additional change, and additional change may be preserved without requiring one event per observation.

This boundary allows Seed to optimize collection and persistence independently while preserving explainability, provenance, support, change semantics, and historical accountability.
