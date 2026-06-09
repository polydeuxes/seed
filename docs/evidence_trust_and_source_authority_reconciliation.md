# Evidence Trust And Source Authority Reconciliation

## Purpose

This document performs a documentation-only reconciliation of observation trust,
source authority, source independence, corroboration, confidence, and
observation preservation.

It is an architectural boundary audit.

It does not implement trust scores, source weighting, new schemas, new
projection behavior, new inference behavior, new storage behavior, or tests.

## Central Question

Seed currently preserves observations and derives facts from observed evidence.
As more sources arrive, Seed must distinguish two different questions:

```text
How much evidence supports this?
```

from:

```text
How much should this evidence be trusted?
```

Those questions are related, but they are not interchangeable.

## Central Finding

```text
Evidence support
        ≠
Source trust
        ≠
Source authority
        ≠
Truth
```

Seed should preserve evidence more readily than it asserts knowledge.

Observation preservation, fact promotion, current-state selection, operator
interpretation, and future belief ranking are separate architectural concerns.

## Current Architectural Baseline

Seed already separates the acquisition path:

```text
Observation
        ↓
Evidence
        ↓
Fact
        ↓
Projection / Read View
```

The current runtime models include observation source types such as:

```text
user
discovery
provider
imported
inferred
```

Current facts also carry source type and confidence fields. Current support and
confidence views can count linked evidence and note contradictions. These are
useful signals, but they should not be retroactively interpreted as a complete
trust model.

This reconciliation therefore treats existing confidence fields as present
support/selection signals, not as a finished answer to source trust, source
independence, or truth.

## Definitions And Boundaries

### Observation

An observation is a source-attributed claim captured from outside the fact being
projected.

Examples:

```text
local discovery reports port 22 listening
Prometheus reports target up = 0
operator states service sshd should be running
imported inventory says host web-01 exists
future agent reports package openssh-server installed
```

An observation is allowed to be wrong.

It may be stale, mistaken, incomplete, malformed, based on a provider bug,
corrupted during import, or produced by a hallucinating agent.

Observation means:

```text
Seed received this claim from this source at this time.
```

Observation does not mean:

```text
The claim is true.
```

### Evidence

Evidence is the preserved provenance that explains why a fact or candidate fact
exists.

Evidence should retain enough source, payload, time, and context information to
support later audit, explanation, contradiction review, and reinterpretation.

Evidence answers:

```text
What was observed, by whom or what, when, and with what source context?
```

Evidence does not answer by itself:

```text
Should Seed believe it?
```

### Corroboration

Corroboration is support from multiple pieces of evidence for a compatible
claim.

Corroboration answers:

```text
How much independent or repeated evidence supports this claim?
```

There are two distinct forms:

| Form | Meaning | Example |
| --- | --- | --- |
| Repetition | Multiple observations report the same thing | 100 samples from one provider say port 22 is open |
| Independent corroboration | Multiple independent source paths report compatible things | local socket inspection, package inventory, service manager, and Prometheus all support sshd running |

Repetition can be useful, especially for measurements over time, but repetition
from one source path is not the same as independent corroboration.

### Confidence

Confidence is Seed's current expression of support strength or selection
preference for a claim in a given view.

In the current system, confidence is already present on observations, evidence,
facts, support records, and confidence views. This document does not redefine
those fields or change their behavior.

Architecturally, confidence should be treated as a projection-time belief or
support signal, not as proof of truth.

Confidence may be affected by:

```text
available evidence
explicit source-reported confidence
corroboration
contradictions
staleness
future trust policy
future authority policy
```

but no single factor should be mistaken for truth.

### Trust

Trust is a belief about the reliability of a source, source path, adapter,
operator input channel, import path, or agent process.

Trust answers:

```text
How likely is this source path to produce accurate observations in this domain?
```

Trust is not currently a complete Seed runtime model in this reconciliation.
It is a conceptual boundary.

Trust may depend on:

```text
source history
adapter correctness
domain fit
operator role
provider quality
freshness guarantees
tamper resistance
auditability
known failure modes
```

Trust does not make observations true.

### Authority

Authority is the right of a source to make declarations within a particular
domain or workflow.

Authority answers:

```text
Is this source allowed to declare, override, or define this class of claim?
```

Authority is not the same as truth.

An operator may be authorized to declare an intended configuration. That does
not mean the live system currently matches the declaration.

A package manager may be authoritative for installed package metadata. That
does not mean a related service is running.

A provider may be authoritative for its own API response. That does not mean
its response correctly describes the external world.

### Source Independence

Source independence is the degree to which pieces of evidence arise from
different failure domains.

It answers:

```text
Could these observations all be wrong for the same reason?
```

Independence is not equivalent to source type count. Two providers may depend
on the same backend. Two local observations may come from independent kernel and
filesystem surfaces. One imported inventory and one operator note may both have
been copied from the same stale spreadsheet.

Source independence should consider:

```text
collection mechanism
adapter implementation
upstream data origin
operator or agent identity
time window
network vantage point
host vantage point
shared transformation path
shared cache or import source
```

### Fact

A fact is a normalized state claim derived from evidence-backed observation or
explicit inference.

In Seed architecture, a fact is inspectable, attributable, and projectable.

A fact should be read as:

```text
Seed has normalized evidence for this claim.
```

not necessarily:

```text
This claim is verified reality.
```

Facts can be contradicted, stale, weakly supported, strongly supported, inferred,
or superseded in a view without requiring the original observations to be
destroyed.

## Question Reconciliation

### 1. Can An Observation Be False?

Yes.

False observations are expected architectural inputs.

Examples include:

```text
stale local discovery output
mistaken operator input
buggy provider response
corrupted import
hallucinated agent output
clock-skewed scrape result
cached inventory record
partial filesystem view
```

Seed should not require all accepted observations to be true. It should require
accepted observations to be preservable, attributable, bounded, and safe to
store.

### 2. Are All Observation Sources Equal?

No.

Sources differ by collection path, failure mode, domain fit, freshness,
auditability, and authority.

However, source type alone does not establish trust.

For example:

| Source type | Useful interpretation | Boundary |
| --- | --- | --- |
| `discovery` | Locally collected observation | May still be stale, buggy, partial, or environment-dependent |
| `provider` | External or integration-provided observation | May be accurate, delayed, misconfigured, or provider-reported only |
| `imported` | Observation loaded from an external artifact | May preserve inventory intent, but may be stale or copied |
| `user` / operator | Human-supplied observation or declaration | May carry authority in a workflow, but may still be mistaken |
| `inferred` | Derived from other facts or rules | Depends on source facts and rule boundaries |

Source type is provenance, not a trust verdict.

### 3. Difference Between Observation, Evidence, Corroboration, Confidence, Trust, Authority, And Fact

The concepts should remain separate:

| Concept | Primary question | Not the same as |
| --- | --- | --- |
| Observation | What claim did a source report? | Truth |
| Evidence | What provenance supports the claim? | Belief |
| Corroboration | How much compatible support exists? | Trust |
| Confidence | How strongly does a view currently rank or believe the claim? | Proof |
| Trust | How reliable is the source path expected to be? | Evidence count |
| Authority | Is the source entitled to declare this kind of claim? | Accuracy |
| Fact | What normalized claim has Seed projected from evidence? | Verified reality |

### 4. What Is Source Independence?

Source independence is separation of failure domains.

The following are not equivalent:

```text
100 observations from one provider
```

and:

```text
1 local socket observation
1 Prometheus observation
1 package inventory observation
1 service-manager observation
```

The first case may show repeated evidence, temporal persistence, or provider
consistency. It may also show one repeated bug.

The second case may show stronger independent corroboration if the observations
come from distinct collection paths and support compatible scoped claims.

Corroboration should therefore consider source independence separately from
observation count.

### 5. Can A Trusted Source Be Wrong?

Yes.

A trusted source can be wrong because trust is a reliability expectation, not a
truth guarantee.

Examples:

```text
local discovery adapter has a parsing bug
Prometheus scrape caught a transient anomaly
operator typed the wrong host name
inventory was generated before a migration
package database was partially updated
```

Implication:

Seed should allow trusted-source observations to be contradicted, expired,
superseded, explained, or reinterpreted without deleting their provenance.

### 6. Can An Untrusted Source Be Correct?

Yes.

An untrusted or low-trust source can report a true claim.

Examples:

```text
an imported observation accurately records an old but still-valid host
an external provider correctly reports a metric
an agent-produced observation correctly identifies a package
an unaudited script accurately reports an open port
```

Implication:

Low trust should not automatically erase evidence. It may limit promotion,
selection priority, automation eligibility, or operator-facing claim strength.

### 7. Should Seed Preserve Contradictory Observations?

Yes, when they are well-formed, attributable, and safe to store.

Contradictory observations are evidence about disagreement.

Example:

```text
observation A: port 22 open
observation B: port 22 closed
```

Both may be valid observations if they differ by:

```text
time
vantage point
network path
host identity
namespace
source freshness
predicate scope
```

Even when one is wrong, preserving both supports later audit and explanation.

Observation preservation and fact promotion are separate concerns.

Seed may preserve both observations while a current-state view selects one,
marks both contradicted, narrows the predicates, asks for refresh, or refuses to
make a stronger claim.

### 8. Should Seed Reject Observations?

Seed should reject or quarantine observations for structural and safety reasons,
not merely because they are low-trust or contradictory.

| Category | Preservation stance | Rationale |
| --- | --- | --- |
| Malformed | Reject or quarantine | Cannot be safely normalized or attributed |
| Unsafe / secret-bearing | Reject or redact according to existing safety boundaries | Preservation must not leak secrets |
| Impossible under schema constraints | Reject or quarantine | The system cannot attach coherent semantics |
| Contradictory | Preserve | Contradiction is evidence, not an ingestion failure |
| Low-trust | Preserve with provenance if safe and well-formed | Trust affects belief, not existence of evidence |
| Suspicious | Preserve, quarantine, or flag depending on safety | Suspicion may affect promotion; unsafe payloads still require rejection |
| Stale | Preserve with time/expiry context | Staleness is interpretive evidence, not necessarily invalidity |

A useful boundary is:

```text
Reject when Seed cannot safely preserve the observation as evidence.
Do not reject merely because Seed should not believe it yet.
```

### 9. Relationship Between Trust And Corroboration

Trust and corroboration answer different questions.

Trust asks:

```text
How reliable is this source path expected to be?
```

Corroboration asks:

```text
How much compatible evidence supports this claim?
```

Therefore:

```text
100 observations from one buggy provider
```

may have high repetition but weak independent corroboration and low trust.

```text
4 observations from independent sources
```

may have stronger corroboration even with fewer total observations.

Neither pattern independently proves truth.

### 10. How Should Operator Observations Be Viewed?

Operator observations should be treated as observations from a special and often
high-importance source path, not as automatic truth.

Operators may provide different kinds of input:

| Operator input | Architectural interpretation |
| --- | --- |
| Observation | "I saw X"; evidence from a human source |
| Declaration | "X should be true"; may define desired state or intent |
| Override | "Use X for this workflow"; may be authoritative for a decision boundary |
| Correction | "Previous claim Y was wrong"; evidence about prior evidence |
| Approval | "Proceed"; policy/action authorization, not a world-state fact |

Operator authority is domain-specific.

An operator may be authoritative for intent, approval, ownership declaration, or
manual override. The same operator may still be wrong about live runtime state.

Implication:

Seed should avoid collapsing these into one concept called "trusted user truth."

## Required Findings

This reconciliation supports the following findings:

```text
An observation can be wrong.
A trusted source can be wrong.
An untrusted source can be correct.
Observation preservation is not the same as fact promotion.
Source authority is not the same as truth.
Corroboration and trust are distinct concepts.
Observation count is not the same as source independence.
Many observations from one source do not automatically create strong corroboration.
```

## Architectural Invariants

The findings support these architectural invariants:

1. Observation preservation should be easier than fact promotion.
2. Seed should preserve evidence more readily than it asserts knowledge.
3. Trust affects belief.
4. Corroboration affects support.
5. Authority affects interpretation.
6. Source independence affects corroboration quality.
7. None of trust, corroboration, authority, confidence, or count independently determines truth.
8. Contradiction is a first-class evidence condition, not necessarily an ingestion error.
9. Source type is provenance, not a trust score.
10. Operator authority is domain-specific and should not be conflated with live-state accuracy.

## Boundary Model

A future trust-aware architecture should keep these layers separate:

```text
Ingestion boundary
    Can this observation be safely preserved?

Provenance boundary
    Where did it come from, when, through what path, and with what payload?

Support boundary
    What other evidence supports the same scoped claim?

Independence boundary
    Are supporting observations from separate failure domains?

Trust boundary
    How reliable is each source path expected to be for this domain?

Authority boundary
    Is this source allowed to declare or override this kind of claim?

Promotion boundary
    What claim strength is justified in a fact, view, answer, or action?

Truth boundary
    Seed may estimate belief, but no single internal signal proves reality.
```

## Non-Goals

This document does not propose or implement:

```text
trust scores
source weights
source reputation storage
new observation schemas
new fact schemas
new evidence schemas
new projection behavior
new read models
new inference rules
new contradiction rules
new confidence aggregation behavior
new provider behavior
new operator override mechanics
new tests
```

It also does not declare any existing source type universally trusted or
untrusted.

## Implementation Implications

No implementation work is required by this reconciliation.

If future implementation work is considered, it should preserve these
boundaries:

- Do not use source type alone as a trust score.
- Do not treat observation count as source independence.
- Do not treat operator authority as automatic live-state truth.
- Do not reject safe, well-formed observations merely because they conflict with
  current facts.
- Do not destroy contradictory evidence to simplify current-state views.
- Do not let confidence terminology imply proof unless the supporting view
  explicitly justifies that claim strength.
- Keep preservation, promotion, selection, explanation, and action authorization
  separate.

## Architectural Conclusion

Seed should reason about evidence in layers.

Observation preservation records what was claimed.

Evidence records why Seed can audit the claim.

Corroboration records how much compatible support exists.

Source independence records whether support comes from separate failure domains.

Trust records expected reliability of a source path.

Authority records whether a source is entitled to declare a claim in a domain.

Confidence records a view's current belief or support estimate.

Facts record normalized claims derived from evidence.

None of these alone determines truth.

The safest architectural posture is therefore:

```text
Preserve broadly.
Promote carefully.
Explain provenance.
Separate support from trust.
Separate authority from truth.
Separate repetition from independence.
```
