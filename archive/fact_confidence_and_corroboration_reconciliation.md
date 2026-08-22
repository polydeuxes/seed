# Fact Confidence And Corroboration Reconciliation

## Purpose

This document reconciles a conceptual tension exposed while reviewing Seed's knowledge representation.

The README describes the core acquisition path as:

```text
Observation
        ↓
Evidence
        ↓
Fact
```

The implementation supports that path directly.

However current operator experience often feels like:

```text
Seed is collecting evidence about the system,
not proving the live system's actual state.
```

This document clarifies what Seed means by `Fact` before broad corroboration, live probing, contradiction resolution, and multi-source support are available.

## Trigger

A State Summary showed equal counts:

```text
Facts: 2810
Observations: 2810
```

This is expected in the current acquisition phase because many observation paths currently produce one evidence-backed fact per observation.

The concern is not the count itself.

The concern is interpretation.

A fact emitted from one observation is not the same thing as verified live reality.

## Central Finding

```text
Fact
        ≠
Verified live reality
```

In Seed, a fact is best understood as:

```text
A normalized claim backed by provenance evidence.
```

It is not, by itself:

```text
a proven truth
a live health assertion
a reachability guarantee
a corroborated conclusion
a resolved belief after all evidence is compared
```

## Current Implementation Alignment

The code keeps the acquisition objects distinct:

```text
Observation
Evidence
Fact
FactSupport
EvidenceGraph
Current / Best Fact
Read Views
```

The current ingestion path records:

```text
observation.observed
evidence.observed
fact.observed / fact.inferred
```

This is aligned with the README's acquisition path.

The incomplete part is not implementation separation.

The incomplete part is operator interpretation of what a single fact means.

## Observation Versus Evidence Versus Fact

### Observation

An observation is a normalized external/input claim captured from a source.

Examples:

```text
/etc/passwd contains user john
local filesystem table includes mount /mnt/sda1
provider response reports metric X
operator supplies claim Y
```

### Evidence

Evidence is the provenance payload that records where the observation or tool result came from.

Evidence preserves:

```text
source
kind
payload
observed_at
confidence
```

Evidence explains why a fact exists.

### Fact

A fact is a normalized state claim derived from evidence-backed observation or explicit inference.

A fact preserves:

```text
subject
predicate
value
dimensions
evidence_ids
source_type
confidence
observed_at
expiry
```

A fact is inspectable and projectable.

It is not automatically corroborated truth.

## Why Current Facts Can Feel Like Evidence

Current local-host observation is still mostly single-source.

Typical current shape:

```text
one observation
        ↓
one evidence record
        ↓
one fact
```

Because there is little cross-source or cross-time corroboration yet, many facts feel like evidence records.

That feeling is valid.

The system is in an acquisition-heavy phase:

```text
Observation-rich
Support-poor
```

As more sources are added, Seed should become:

```text
Observation-rich
Support-rich
```

## Port Example

Port evidence illustrates the distinction.

Separate observations may later include:

```text
configuration declares port 80
local socket inspection shows port 80 listening
firewall policy allows port 80
remote TCP probe reaches port 80
HTTP request on port 80 responds
```

These are not the same claim.

They should not collapse into one generic fact such as:

```text
port_80_open = true
```

without explicit scope.

Better scoped facts might include:

```text
service_config_declares_port
local_socket_listening
firewall_rule_allows_port
remote_tcp_probe_reachable
http_endpoint_responded
```

A read view may later summarize:

```text
port 80 appears reachable from vantage point X
```

but that summary should be supported by the scoped facts rather than emitted as an unqualified observation.

## Corroboration Role

Corroboration belongs downstream of raw fact acquisition.

Seed already has structures that can support this:

```text
FactSupport
EvidenceGraph
Contradictions
Confidence Aggregation
Current Fact / Best Fact
Fact Support views
Why views
```

These structures should explain:

```text
which facts support a current belief
which evidence supports those facts
whether support is single-source or multi-source
whether evidence is current or stale
whether facts conflict
whether the claim is scoped or overbroad
```

## Single Observation Boundary

A single observed fact may be useful and valid.

But the operator-facing interpretation should remain conservative.

```text
single observed fact
        ≠
corroborated knowledge
```

A single fact can support statements like:

```text
Seed observed evidence that X was reported.
Seed currently has a fact claiming X.
```

It should not automatically support stronger statements like:

```text
X is certainly true now.
X is live.
X is reachable.
X is healthy.
X is safe.
```

Those require additional evidence and scoped vocabulary.

## Relationship To Availability

This reconciliation reinforces the availability boundary.

Local observation does not imply availability.

Static configuration does not imply reachability.

A fact about declared configuration is not a live-status proof.

Examples:

```text
user exists in /etc/passwd
        ≠
user can log in

service unit exists
        ≠
service is running

firewall config allows port
        ≠
remote host can reach port

local host was observed
        ≠
host availability_status = up
```

## Relationship To Fact Counts

Equal fact and observation counts are not inherently wrong.

They indicate the current acquisition shape:

```text
many observations produce one direct fact each
```

As corroboration grows, counts may diverge.

Possible future shapes:

```text
many observations
        ↓
many facts
        ↓
fewer current beliefs
```

or:

```text
one evidence record
        ↓
multiple facts
```

or:

```text
tool output evidence
        ↓
no facts until explicit mapping exists
```

The counts alone do not define correctness.

Interpretation depends on acquisition source, fact semantics, support, and read view.

## README Implication

The README's acquisition flow is valid:

```text
Observation
        ↓
Evidence
        ↓
Fact
```

But it should eventually be supplemented with the projection/support path:

```text
Fact
        ↓
FactSupport
        ↓
Current / Best Fact
        ↓
Read Views / Explanation
```

This avoids implying that the word `Fact` means final verified truth.

## Non-Goals

This document does not rename `Fact`.

It does not change the ingestion pipeline.

It does not require implementation changes.

It does not add port probing.

It does not add availability checks.

It does not redefine Evidence.

It does not make every fact provisional in the schema.

It clarifies operator interpretation and future read-view responsibility.

## Current Conclusion

Seed has done a good job separating observations, evidence, facts, and support structures in code.

The remaining risk is semantic overstatement.

A Seed fact is an evidence-backed normalized claim.

It becomes more useful as knowledge when projected through support, freshness, confidence, contradiction, scope, and read views.

The important invariant is:

```text
Do not confuse evidence-backed claim
with verified live reality.
```

This should guide future work on ports, probes, firewall rules, services, availability, and any read view that summarizes observed claims into operator-facing conclusions.
