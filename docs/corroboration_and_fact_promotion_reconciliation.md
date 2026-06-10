# Corroboration And Fact Promotion Reconciliation

## Purpose

This document performs a documentation-only reconciliation of corroboration, fact
promotion, contradiction handling, current-state selection, support strength,
evidence accumulation, and the relationship between observations, evidence,
facts, and projections.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify observations, evidence
records, facts, projections, read models, confidence behavior, trust behavior,
inference rules, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations clarified identity derivation boundaries, Prometheus
observation boundaries, and trust/source-authority boundaries. The remaining
question is:

```text
When does accumulated evidence justify a fact?
```

A useful example is:

```text
Observation:
config says port 80 open

Observation:
network probe says port 80 open
```

This raises several architectural questions:

```text
Do these become two facts?
One fact?
One fact with two supporting observations?
How does contradiction affect promotion?
How should current-state views behave?
```

## Central Finding

The safest architectural answer is:

```text
Evidence accumulates.
Facts normalize.
Projections select.
```

A fact is not the same thing as raw observation preservation, accumulated
evidence, selected current state, or verified truth.

Architecturally:

```text
Observation preserves what was seen.
Evidence preserves why Seed may consider a claim.
Fact normalizes the claim being considered.
Projection selects, summarizes, or explains a current view over preserved claims.
```

Corroboration can strengthen support for a compatible claim, but corroboration
alone does not prove truth. Contradiction can weaken certainty or create
competing support, but contradiction alone does not delete evidence or make a
fact false.

## Architectural Definitions

### Observation

An observation is a source-attributed statement received by Seed.

It answers:

```text
What did this source report at this time from this vantage point?
```

Examples:

```text
local discovery reports package openssh-server installed
Prometheus reports target up = 1
operator declares desired port 80 should be open
network probe reports port 22 closed from probe vantage point A
```

An observation may be accurate, stale, incomplete, mistaken, scoped to one
vantage point, or only about desired state. Observation preservation means Seed
retains the source claim. It does not mean Seed has proven the external world.

### Evidence

Evidence is the preserved provenance and support material derived from an
observation, tool result, import, declaration, or inference input.

It answers:

```text
Why is this claim available for consideration?
```

Evidence should preserve enough context for audit and explanation:

```text
source
source type
payload or normalized payload reference
observed time
vantage point or dimensions when available
confidence or source-reported quality when available
links to observations, facts, or source facts
```

A single observation may produce evidence. Multiple observations may produce
multiple evidence records for the same compatible claim. Evidence is allowed to
exist before, after, or without being selected as current state.

### Fact

A fact is a normalized claim backed by provenance evidence.

It answers:

```text
What claim has Seed represented in normalized form?
```

A fact is not necessarily:

```text
verified live reality
operator intent
current selected state
corroborated truth
absence of all contradiction
```

The useful conceptual shape is:

```text
subject
predicate
value
dimensions or scope
supporting evidence
provenance
confidence/support signal
time and freshness metadata
```

Facts should remain explainable through provenance. A fact without an evidence
path is architecturally suspicious because it cannot answer why it exists.

### Projection

A projection is a deterministic read view over preserved observations,
evidence, facts, relationships, support records, conflicts, and other projected
state.

It answers view-specific questions such as:

```text
What facts are currently visible?
Which value currently wins for this predicate?
Which facts support this claim?
Which contradictions or conflicts are visible?
Which evidence explains this fact?
What should an operator see in a summary?
```

A projection may select, group, summarize, rank, suppress expired items by
default, expose ambiguity, or roll up support. A projection must not be confused
with the only preserved interpretation of the evidence.

## Fact Promotion

Fact promotion is the movement from evidence-backed input into a normalized fact
claim.

It should not be overloaded to mean all of the following at once:

```text
Seed observed this.
Seed has evidence for this.
Seed currently believes this.
Seed selected this as current state.
Seed verified this as true.
```

These are separate concepts:

| Statement | Architectural owner | Meaning |
| --- | --- | --- |
| Seed observed this | Observation | A source reported a claim. |
| Seed has evidence for this | Evidence | Provenance exists that can support or explain a claim. |
| Seed represented this as a fact | Fact | The claim was normalized into Seed's fact vocabulary. |
| Seed currently believes/selects this | Projection/current-state selection | A view selected this fact or support group under current rules. |
| Seed verified this as true | Not implied by promotion | Requires a separate scoped verification/truth model if ever introduced. |

Promotion may therefore occur from a single observation when the observation is
sufficient to justify representing a normalized claim with provenance. Promotion
does not require independent corroboration unless the claim being promoted is
itself a stronger claim such as "verified," "currently reachable," or "healthy."

## Can A Single Observation Create A Fact?

Yes, a single observation may create a fact when the fact's claim strength does
not exceed what that observation directly supports.

Examples:

```text
local package inventory reports package X installed
        -> fact: package X installed according to the local package inventory source/scope

Prometheus reports target up = 1
        -> fact: Prometheus sample reports target up at sample time/scope

operator declares desired configuration
        -> fact: desired configuration declaration exists from operator/source/scope
```

The promoted fact must remain scoped to the evidence. A single observation does
not automatically justify stronger claims such as:

```text
package X is usable
service X is running
host is healthy
target is reachable from every vantage point
live state matches desired configuration
```

Independent corroboration is not required for every fact. It is required only
when the architectural claim demands stronger support than one observation can
provide.

## What Is Corroboration?

Corroboration is support from multiple pieces of evidence for a compatible claim.

It answers:

```text
How much evidence supports this claim, and how independent is that support?
```

Corroboration is not identical to trust, authority, observation count, or truth.
It is a support relationship among evidence items and claims.

### Repeated Observations

Repeated observations are multiple reports from the same source path or failure
domain.

Example:

```text
one Prometheus scrape series reports target up for 100 consecutive samples
```

Repetition may improve temporal stability and reduce the chance that a single
sample was accidental, but it may still share the same adapter, source, metric,
configuration, identity mapping, and vantage-point failure modes.

### Independent Corroboration

Independent corroboration is support from meaningfully different source paths or
failure domains.

Example:

```text
package inventory says openssh-server installed
service manager says sshd service exists
local socket inspection says port 22 is listening
remote probe says TCP 22 is reachable from vantage point A
```

These observations do not all assert the exact same predicate, but they are
compatible evidence for a higher-level claim such as:

```text
SSH appears to be present and reachable from vantage point A.
```

The higher-level claim is stronger than any one underlying observation and must
remain explainable through the individual facts and evidence that support it.

### Compatible Evidence

Compatible evidence supports claims that can coexist.

Examples:

```text
config declares port 80
local socket is listening on port 80
HTTP probe receives a response on port 80
```

Compatibility does not require identical predicates. It requires that the claims
can support a shared interpretation without exceeding their scopes.

### Contradictory Evidence

Contradictory evidence supports claims that cannot all be true within the same
scope, time semantics, predicate cardinality, and dimensions.

Examples:

```text
port 22 open from the same vantage point and time window
port 22 closed from the same vantage point and time window
```

```text
package X installed in the same package database snapshot
package X not installed in the same package database snapshot
```

```text
host up according to a current availability predicate
host down according to the same current availability predicate
```

Contradiction is evidence. It is not merely the absence of corroboration.

## What Corroboration Contributes

Corroboration contributes support strength and explanation depth.

It can help Seed communicate:

```text
how many evidence paths support a claim
whether those evidence paths are independent
which source types agree
which dimensions or vantage points agree
whether support is repeated over time
whether the claim remains supported despite stale or contradictory evidence
```

Corroboration should not independently determine truth. A false claim can be
repeated many times by one broken source. A true claim may have only one strong
authoritative observation. A claim may be well corroborated in one scope and
unsupported or contradicted in another.

## Multiple Observations Supporting The Same Claim

When multiple observations support the same normalized claim, Seed should
conceptually accumulate support rather than create unnecessary duplicate
interpretations.

Example:

```text
package inventory says ssh installed
service manager says sshd exists
Prometheus endpoint suggests ssh reachable
```

These may produce several scoped facts because they are not identical claims:

```text
package ssh installed
service sshd exists
ssh-related endpoint reachable from Prometheus vantage point
```

A projection or higher-level support view may roll these up as support for a
claim such as:

```text
SSH capability appears present on host H.
```

For truly identical normalized claims, the better conceptual shape is:

```text
one normalized claim/support group
multiple supporting observations/evidence paths
```

rather than:

```text
many indistinguishable facts treated as independent truths
```

This does not require changing current implementation. The architectural
principle is that support should accumulate without destroying source evidence,
and read views should preserve navigation from rolled-up support back to each
observation and evidence record.

## What Happens When Observations Disagree?

Disagreement should be preserved before it is interpreted.

### Preservation Behavior

Seed should preserve:

```text
the positive observation
the negative observation
evidence for both
facts or candidate claims for both when normalized
source context for both
time/freshness context for both
dimensions and vantage points for both
```

Contradictory evidence must not be destroyed merely because a current-state view
selects one value.

### Fact Behavior

Fact behavior depends on claim scope and predicate semantics:

- If two claims have different scopes, dimensions, or time semantics, they may
  both be valid scoped facts rather than contradictions.
- If two claims compete for a single-cardinality durable predicate in the same
  scope, they should be represented as competing facts/support groups.
- If the predicate is multi-cardinality, multiple values may be expected rather
  than contradictory.
- If the predicate is measurement-like, currentness and freshness may matter
  more than durable conflict.

A contradicted fact should not be rewritten into a false fact. The contradiction
is a relationship or condition over evidence/facts in a scope.

### Projection Behavior

Projection behavior should be explicit about what it is selecting:

```text
latest sample
best-supported durable value
all current multi-cardinality values
ambiguous/no winner
conflict inventory
confidence-adjusted view
operator summary
```

A current-state projection may select one value, expose ambiguity, or surface a
conflict. That selection must not erase the underlying evidence.

## Relationship Between Contradiction And Corroboration

Contradiction is not simply absence of corroboration.

The relationship is:

```text
corroboration = evidence supports compatible claims
contradiction = evidence supports incompatible claims within the same scope
```

Contradiction can be considered negative support for a candidate current-state
selection, but architecturally it is better treated as a separate evidence
condition:

```text
compatible support accumulates for a claim
contradictory support accumulates for competing claims
selection views compare or expose the competition
```

This distinction matters because absence of corroboration is often just
unknownness:

```text
one observation says port 22 open
no other evidence exists
```

Contradiction is stronger than unknownness:

```text
one observation says port 22 open
another same-scope observation says port 22 closed
```

## Current-State Selection

Current-state selection is a projection concern, not an evidence preservation
concern.

It answers:

```text
Given preserved facts and support, what should this read view present as current?
```

Selection may consider:

```text
predicate cardinality
measurement versus durable semantics
support strength
source types
source independence
confidence signals
freshness and expiry
contradictions
ambiguity
dimensions and vantage point
operator-facing surface purpose
```

Current-state selection differs from preservation in three ways:

1. Preservation keeps the historical and evidentiary record.
2. Selection chooses or summarizes for a particular current read purpose.
3. Selection can change as new evidence arrives without mutating the meaning of
   old observations.

A current-state view should therefore be explainable as:

```text
selected value
supporting evidence
competing evidence when present
selection reason
freshness/staleness status
scope and dimensions
```

## Confidence Boundaries

Confidence is a support or selection signal, not a universal truth value.

Confidence may appear at several layers, but the meaning differs by layer:

| Layer | Confidence means |
| --- | --- |
| Observation | Source-reported or adapter-assigned quality of one reported claim. |
| Evidence | Strength/quality of provenance for considering a claim. |
| Fact | Confidence attached to the normalized claim as represented. |
| Support group | Aggregate support for a normalized claim/value. |
| Projection | View-specific confidence after selection, penalties, freshness, or conflict handling. |
| Current-state selection | Preference or belief strength for choosing one current representation over alternatives. |

These concepts should not be collapsed. A high-confidence observation can be
contradicted. A low-confidence observation can still be important evidence. A
projection may lower confidence because of contradiction without mutating the
original fact confidence. A support group may be strong for one scoped value
while the broader operator conclusion remains weak.

## Can A Fact Be True, False, Stale, Contradicted, Weak, Or Strong?

The vocabulary should be scoped carefully.

### True Or False

Truth is not currently established by the existence of a fact. A fact is a
normalized claim with provenance. Calling it true or false requires a separate
truth or verification model, or a projection explicitly scoped as a belief view.

### Stale

Staleness is a freshness/expiry concern over evidence, facts, supports, or
projections. It should not erase provenance. A stale fact can remain historically
important while being excluded from default current-state selection.

### Contradicted

Contradicted is a relationship or condition involving competing evidence/facts
within a scope. It is not an intrinsic permanent property of one fact in
isolation. A fact may be contradicted in one projection scope and not in another
if dimensions, time windows, or predicate semantics differ.

### Weakly Or Strongly Supported

Weak and strong support are support/projection properties. They describe the
quality, quantity, independence, and compatibility of evidence for a claim. They
should remain explainable through the underlying observations and evidence.

## Port Example Reconciled

Input:

```text
Observation: config says port 80 open
Observation: network probe says port 80 open
```

Architectural interpretation:

1. Preserve both observations.
2. Preserve evidence for both source paths.
3. Normalize scoped facts without exceeding evidence strength:

```text
configuration declares/listens/allows port 80, depending on exact config source
network probe reached port 80 from vantage point V at time T
```

4. Treat them as compatible evidence for a broader claim only if a support rule
   or projection explicitly states the bridge:

```text
port 80 appears intended and reachable from vantage point V
```

5. Preserve provenance so the broad claim can explain which source contributed
   which support.
6. If later evidence says port 80 closed, preserve that evidence and surface a
   same-scope conflict or a scoped distinction depending on dimensions and time.

## Non-Goals

This reconciliation does not require or recommend:

```text
new schemas
new runtime semantics
a truth engine
a trust scoring engine
a source authority implementation
a new inference engine
a change to current confidence behavior
a change to current contradiction behavior
a change to current projection behavior
test changes
fact deletion when contradicted
a requirement that all facts be independently corroborated
```

It also does not require that every read surface expose every piece of evidence.
It requires that any selected or summarized state remain traceable to preserved
provenance through appropriate explanation or inspection surfaces.

## Implementation Implications

Because this is documentation-only, these are interpretive implications for
future work, not requested changes:

- Do not interpret fact count as truth count.
- Do not interpret observation count as corroboration count.
- Do not treat independent corroboration as equivalent to source trust.
- Do not treat source authority as equivalent to live truth.
- Do not delete contradictory evidence during current-state selection.
- Do not make a fact stronger than the evidence scope that produced it.
- Do not collapse desired state, configured state, observed local state,
  externally reachable state, and health into one unscoped fact.
- Do preserve provenance paths from projections back to facts, evidence, and
  observations.
- Do allow projections to summarize support, select current values, and expose
  ambiguity while preserving the underlying evidence record.

## Architectural Invariants

The reconciliation supports the following invariants:

```text
Evidence accumulates.
Facts normalize.
Projections select.
```

```text
Preserve observations.
Preserve evidence.
Explain facts.
```

```text
A single observation may justify a scoped fact.
A single observation does not justify claims stronger than its scope.
```

```text
Corroboration strengthens support.
Contradiction weakens certainty or creates competing support.
Neither independently determines truth.
```

```text
Corroboration is not trust.
Corroboration is not authority.
Corroboration is not observation count.
```

```text
Contradiction is evidence.
Contradiction is not merely missing corroboration.
Contradiction must not destroy source evidence.
```

```text
Current state is a view.
Current state is not the only preserved interpretation.
```

```text
Support should accumulate without destroying source evidence.
Support rollups must remain explainable through provenance.
```

```text
Preservation and promotion are different concerns.
Promotion and current-state selection are different concerns.
Current-state selection and truth are different concerns.
```

## Final Reconciliation

Seed should reason about accumulated evidence by separating four questions:

```text
What was observed?
What evidence exists?
What normalized claim does that evidence support?
What should a particular projection present right now?
```

A single observation can produce evidence and may justify a scoped fact.
Multiple compatible observations can accumulate support for one normalized claim
or for a higher-level claim when an explicit bridge exists. Contradictory
observations should be preserved as evidence for competing claims, not erased or
silently transformed into truth arbitration. Current-state selection should be a
view over preserved evidence and facts, with provenance, ambiguity, support
strength, contradiction, confidence, and staleness exposed according to the
surface's authority.
