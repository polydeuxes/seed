# Claim Strength And Assertion Semantics Reconciliation

## Purpose

This document performs a documentation-only reconciliation of claim strength,
assertion semantics, historical truth, current-state selection, verification,
contradiction, and temporal claim interpretation.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify observations, evidence,
facts, relationships, projections, confidence behavior, trust behavior,
temporal logic, storage models, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established trust and authority boundaries,
corroboration boundaries, fact promotion boundaries, and relationship promotion
boundaries. The remaining question is:

```text
What exactly does a Seed claim mean?
```

The answer cannot be reduced to a single word such as `fact`, `true`,
`current`, or `verified`.

Seed preserves knowledge claims with provenance. Different views may then
characterize those claims as observed, supported, corroborated, contradicted,
selected, current, stale, historical, or verified under scoped rules.

## Central Finding

The safest architectural answer is:

```text
A Seed claim is a scoped proposition preserved or interpreted through
provenance-backed knowledge structures. It is not, by itself, universal truth.
```

More compactly:

```text
Observations report.
Evidence preserves provenance.
Facts normalize claims.
Relationships normalize edges.
Projections select interpretations.
Verification confirms a scoped question.
History preserves what was knowable at a time.
```

Therefore:

```text
Fact
  ≠ raw observation
  ≠ evidence payload
  ≠ selected current state
  ≠ verified live reality
  ≠ universal or timeless truth
```

A Seed fact is best understood as:

```text
A normalized, provenance-backed claim within a defined subject, predicate,
value, scope, and time context.
```

## Files Inspected

This reconciliation builds on the following existing documentation:

- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/claim_support_design.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/contradiction_handling_audit.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/capability_verification_audit.md`
- `docs/capability_verification_vocabulary.md`

## Architectural Definitions

### Observation

An observation is a source-attributed report captured by Seed.

It answers:

```text
What did this source report, from this vantage point, at this time?
```

Examples:

```text
local package inspection reported openssh-server installed
Prometheus reported target up = 1
network probe reported port 22 closed from vantage point A
operator input declared service X should be enabled
```

An observation may be accurate, stale, partial, scoped, mistaken, duplicated, or
superseded by later observations. Preserving an observation means Seed preserves
what was reported. It does not mean the reported proposition is proven true.

### Evidence

Evidence is the preserved provenance and support material that explains why a
claim is available for consideration.

It answers:

```text
Why may Seed consider this claim?
```

Evidence may include source, source type, payload, observed time, dimensions,
vantage point, confidence signal, trust metadata, and links to observations or
source facts.

Evidence is not itself the normalized claim. It is the audit path for a claim.

### Fact

A fact is a normalized claim backed by evidence.

It answers:

```text
What proposition has Seed represented in normalized form?
```

A fact should be interpreted with its scope:

```text
subject
predicate
value
dimensions
source/provenance
time/freshness metadata
support/confidence signals
```

Examples:

```text
package openssh-server was observed installed by local package adapter at T
service ssh had running status reported by systemd observation at T
port 80 was locally observed listening on node N at T
filesystem /var had usage > 90% in metric sample interval I
```

A fact may be useful and valid as a normalized claim even when it is not
corroborated, selected as current, or verified as live reality.

### Relationship

A relationship is a normalized edge between entities, artifacts, concepts, or
claims.

It answers:

```text
What connection has Seed represented between things?
```

Examples:

```text
component A imports component B
service S listens_on port P
fact F supports claim C
entity E has alias A
```

A relationship may itself be evidence-backed, supported, contradicted, selected,
or historical. A relationship is not automatically stronger than a fact; it is a
different knowledge shape. Relationship evidence that justifies preserving an
edge may not justify promoting ownership, causality, dependency, or behavioral
control.

### Projection

A projection is a deterministic read view over preserved knowledge structures.

It answers view-specific questions such as:

```text
Which facts are visible under current rules?
Which value is selected for a single-cardinality predicate?
Which claims have competing support?
Which facts are stale or expired?
Which evidence explains this selected view?
```

Projection is selection and interpretation over preserved knowledge. It is not
new observation. It is not proof. It is not the only truth of the ledger.

### Claim

A claim is the proposition being asserted, preserved, normalized, supported,
selected, contradicted, verified, or communicated.

It answers:

```text
What is being said about the world, system, source, relationship, or history?
```

Claims can appear at multiple layers:

| Layer | Example claim form |
| --- | --- |
| Observation | `source S reported package P installed at T` |
| Evidence | `payload E supports considering package P installed` |
| Fact | `package P was observed installed on host H at T` |
| Relationship | `service S listens_on port P` |
| Projection | `current selected package state for P is installed as of projection time Q` |
| Response | `Seed can say P appears installed, with caveats` |

The claim is not identical to any one storage object. Storage objects preserve,
normalize, relate, or select claims.

## Assertion Semantics

Seed should conceptually distinguish claim forms that may sound similar in
natural language:

| Natural-language statement | Architectural interpretation |
| --- | --- |
| `A package was installed.` | Historical claim about a prior state or event. Requires time/scope. |
| `A package is installed.` | Current-state claim. Requires selection/freshness rules and an `as of` time. |
| `A package is believed installed.` | Support/selection claim about Seed's knowledge state. |
| `A package was observed installed.` | Observation/fact claim tied to source, vantage point, and observation time. |
| `A package is currently projected installed.` | Projection claim tied to projection rules and projection time. |
| `A package is verified installed.` | Verification claim tied to a verification method, scope, and verification time. |

These are not interchangeable.

The same underlying evidence may support some of them and fail to support
others. For example, a package inventory observation at 09:00 may justify:

```text
package P was observed installed at 09:00
```

It may not, by itself, justify:

```text
package P is installed now
package P is verified installed now
package P is guaranteed available
```

unless freshness, projection, and verification boundaries explicitly support
those stronger assertions.

## Claim Strength

Claim strength is the amount of assertion made by a claim relative to what its
support justifies.

It asks:

```text
How much does this claim assert?
```

It is related to, but distinct from, confidence, trust, corroboration, and
authority.

| Concept | Question answered | Boundary |
| --- | --- | --- |
| Claim strength | How strong is the assertion? | A semantic property of the claim. |
| Evidence strength | How much does the available evidence justify? | A property of support material. |
| Confidence | How much support does Seed estimate for a fact or view? | A support/integrity signal, not truth itself. |
| Trust | How much should Seed rely on this source or authority class? | A source/source-role property, not claim truth. |
| Corroboration | Do independent or compatible sources support the same scoped claim? | A support relationship, not proof. |
| Authority | Is this source allowed to define this kind of claim? | A governance/source boundary, not automatic truth. |

A claim may have high trust but excessive claim strength. A trusted package
manager observation may justify `package P was installed according to package
manager at T`; it may not justify `service P was reachable from the internet at
T`.

A claim may have high confidence but limited scope. Many local observations may
support `port 80 is locally listening`; they do not automatically support `port
80 is externally reachable`.

A claim may be corroborated but still historically scoped. Multiple sources may
corroborate `service S was running yesterday`; that does not make `service S is
running now` true.

## Semantic State Boundaries

The following terms should remain conceptually separate.

### Observed

`Observed` means a source reported or Seed captured something at a time from a
vantage point.

It does not mean:

```text
true
current
corroborated
verified
selected
```

An observed claim can later be contradicted, expire, or cease to be current while
remaining a preserved historical observation.

### Supported

`Supported` means evidence or facts provide a reason to consider a claim.

It does not mean the support is sufficient for every stronger phrasing of the
claim. Support must be evaluated against claim strength and scope.

A single observation may support a weak scoped claim. Multiple independent
observations may support a stronger claim. Some claims require specific evidence
kinds, not merely more evidence volume.

### Corroborated

`Corroborated` means compatible support exists from multiple observations,
sources, methods, times, or independent evidence paths as defined by the claim's
support rule.

Corroboration strengthens support. It does not automatically produce verified
truth, current truth, or authority.

Corroboration must preserve scope. The following are not necessarily
corroborating the same claim:

```text
config declares port 80
local socket is listening on port 80
remote HTTP request succeeded on port 80
```

They may support a broader availability interpretation only through explicit
projection or support rules.

### Contradicted

`Contradicted` means there is incompatible or competing support under a relevant
predicate, relationship, dimension, or claim rule.

It does not mean the contradicted claim is false.

Contradiction may indicate:

```text
uncertainty
staleness
vantage-point difference
measurement timing difference
source disagreement
single-cardinality conflict
modeling ambiguity
```

For example:

```text
port 22 open
port 22 closed
```

may be conflicting only if they refer to the same host, same port, same protocol,
same vantage point, same time window, and same meaning of `open`. If one claim is
local listening and the other is remote unreachable, they are different scoped
claims, not a direct logical contradiction.

### Selected

`Selected` means a projection or read view chose a claim, value, support group,
or interpretation under deterministic selection rules.

It does not mean verified.

Selection answers:

```text
Which preserved interpretation does this view expose now?
```

Selection must be read with:

```text
projection name
projection rules
projection time
input evidence/facts
freshness and expiry behavior
cardinality semantics
conflict behavior
```

### Verified

`Verified` means a scoped verification question received confirmation through a
specified verification method at a specified time.

It does not mean universal truth, indefinite currentness, or independence unless
those are part of the verification definition.

Verification may involve additional observation. It may involve independent
corroboration. It may provide stronger support. It may confirm current state.
But none of those is the generic definition by itself.

The safest general definition is:

```text
Verification is scoped confirmation of a specific claim by a declared method,
with provenance and time.
```

Therefore `verified reachable` is a different claim from `configured reachable`,
`believed reachable`, or `previously observed reachable`.

## Historical Truth, Current Truth, Projected Current State, And Preserved Evidence

Seed should distinguish four related concepts.

### Historical truth

Historical truth concerns whether a claim was true at a past time or during a
past interval.

Examples:

```text
George Washington was President.
Node115 rebooted yesterday.
Port 80 was open at observation time.
Filesystem usage exceeded 90% last week.
```

These claims require temporal scope. They do not become false merely because the
current state changed.

`George Washington was President` is not contradicted by `George Washington is
not currently President` because the predicates have different temporal scopes.

### Current truth

Current truth concerns whether a claim is true now, or as of a stated `now`.

Examples:

```text
Node115 is reachable now.
service S is running now.
user U exists now.
filesystem F is attached now.
```

Current truth requires current evidence, acceptable freshness, or a projection
rule that explicitly allows durable facts to remain current until expired or
contradicted.

### Projected current state

Projected current state is Seed's selected current interpretation under a
projection.

It answers:

```text
What does this projection currently select from preserved knowledge?
```

It should always be understood as:

```text
current according to projection P
as of projection/evaluation time T
from evidence/facts E
under freshness/cardinality/conflict rules R
```

Projected current state is not identical to live truth. It is an inspectable
view over preserved knowledge.

### Preserved evidence

Preserved evidence is the retained provenance that explains why a claim was
available.

It may outlive currentness. It may outlive verification. It may be attached to a
claim that is no longer selected. It may support historical reasoning even after
current state changes.

Preservation answers:

```text
What did Seed receive, from whom, when, and with what payload or support path?
```

Preservation does not assert current truth.

## Historical Claims Are First-Class

A claim can be historically true but not currently true.

Examples:

| Historical claim | Possible current claim |
| --- | --- |
| `service was installed` | `service is no longer installed` |
| `service was running` | `service is stopped now` |
| `service was reachable` | `service is unreachable now` |
| `user existed` | `user no longer exists` |
| `filesystem was attached` | `filesystem is detached now` |

The current claim does not erase the historical claim. It changes the current
interpretation.

This supports the invariant:

```text
History should not be destroyed merely because current state changed.
```

Historical claims may be needed for audit, debugging, incident reconstruction,
trend analysis, causality investigation, compliance, and explanation.

## Verification Boundary

Verification should be treated as a scoped status over a claim, not as a generic
upgrade of all related claims.

A verification record or view should conceptually answer:

```text
Which claim was verified?
What method verified it?
From which vantage point?
At what time?
For what duration or freshness window?
Against which expected condition?
With which evidence?
```

Verification can mean different things depending on the claim family:

| Claim family | Possible verification meaning |
| --- | --- |
| Package state | Package manager query confirmed package state at T. |
| Service state | Service manager query confirmed running/stopped state at T. |
| Reachability | Probe from vantage point V succeeded at T. |
| File existence | Filesystem inspection confirmed path at T. |
| Capability | Required capability facts were present and consistent at T. |

Verification is not identical to corroboration:

```text
corroboration = compatible support from multiple paths
verification = scoped confirmation by an accepted method
```

A claim may be corroborated but not verified. A claim may be verified by one
accepted method but not independently corroborated. A claim may have been
verified historically and later become unverified for current-state purposes when
its freshness window expires.

## Current-State Selection Boundary

Current-state selection is a projection concern.

It should not be read as:

```text
all preserved history
all truth
all support
all verified knowledge
```

A current-state statement must be qualified by:

```text
Current according to what projection?
Current as of when?
Current from which evidence and facts?
Current under which cardinality and expiry rules?
Current despite, without, or because of which contradictions?
```

For example:

```text
Node115 was observed up.
```

means a source reported an up state at an observation time.

```text
Node115 is currently projected up.
```

means a current-state projection selected `up` under its rules.

```text
Node115 is verified reachable.
```

means a verification method confirmed reachability from a scoped vantage point at
a scoped time.

These are different claim categories.

## Contradiction And Truth

Contradiction is an integrity signal, not a truth verdict.

Contradiction means Seed has preserved or projected competing claims that cannot
all be selected as the same scoped current interpretation under a relevant rule.

It may imply:

```text
one claim is false
one claim is stale
both claims are true under different scopes
sources disagree
projection rules are underspecified
the model collapsed distinct predicates
```

Seed should therefore avoid treating contradiction as deletion, automatic
falsehood, or automatic confidence collapse.

For example:

```text
port 22 open
port 22 closed
```

can represent:

- a real conflict about the same scoped state;
- a time difference, such as open at 10:00 and closed at 10:05;
- a vantage-point difference, such as open locally but blocked remotely;
- a vocabulary difference, such as listening versus reachable;
- a stale fact competing with a fresh fact.

The contradiction boundary is:

```text
Contradiction preserves disagreement for explanation and selection; it does not
resolve truth by itself.
```

## Historical Claims And Preservation

Historical claims, events, observations, and facts should be conceptually
distinct even when they are related.

| Concept | Historical role |
| --- | --- |
| Event | Records that something happened in Seed's ledger or runtime history. |
| Observation | Records that a source reported something at a time. |
| Evidence | Records why a claim was available and from what provenance. |
| Fact | Normalizes a scoped claim derived from evidence. |
| Historical claim | Interprets a proposition as applying to a past time or interval. |
| Current projection | Selects an interpretation for present use. |

Historical preservation should retain enough provenance to answer:

```text
What was claimed?
Who or what claimed it?
When was it observed?
What scope did it have?
Was it later contradicted, expired, or no longer selected?
```

Preserved historical knowledge can remain valuable after current-state selection
moves elsewhere.

## Can Claims Move Between Semantic States?

The sequence:

```text
observed
  ↓
supported
  ↓
corroborated
  ↓
verified
```

is tempting, but it should not be treated as a mandatory linear promotion
pipeline.

These are better understood as mostly orthogonal properties or interpretations
that may accumulate, expire, disappear, or apply to different scoped claims.

A claim may be:

```text
observed but unsupported by other facts
supported but not corroborated
corroborated but not verified
verified but no longer current
current but not independently corroborated
contradicted but still historically true
selected but not verified
preserved but not selected
```

Some workflows may present these as stages for convenience, but the architecture
should not collapse them into a single lifecycle state.

The safer model is:

```text
Claim
  has provenance
  has scope
  has time semantics
  may have support
  may have corroboration
  may have contradiction
  may be selected by a projection
  may be verified by a method
  may remain preserved historically
```

## Examples

### George Washington was President

This is a historical claim.

It is not a current-state claim. It should not be contradicted by a current
claim that someone else is President, because the time scope differs.

### Node115 was observed up

This is an observation/fact claim.

It means Seed preserved a source report. It does not necessarily mean Node115 is
up now.

### Node115 is currently projected up

This is a projection claim.

It means current-state selection chose `up` according to projection rules,
freshness, and available evidence.

### Node115 is verified reachable

This is a verification claim.

It means a scoped verification method confirmed reachability at a time and from
a vantage point. It is stronger than merely being observed up only if the
verification method and scope justify that stronger assertion.

### Port 80 was open at observation time

This is a historical observed-state claim.

It may remain true even if port 80 is closed now.

### Filesystem usage exceeded 90% last week

This is a historical measurement claim over a time interval.

It should not be replaced by the current filesystem usage. Current projection may
select the latest retained measurement, but historical reasoning may still need
the older measurement or an aggregate derived from preserved evidence.

## Architectural Invariants

The reconciliation supports the following invariants:

```text
Observed is not identical to true.
```

```text
Current is not identical to historical.
```

```text
Selected is not identical to verified.
```

```text
Contradicted is not identical to false.
```

```text
Verification is not identical to corroboration.
```

```text
Historical truth is a first-class knowledge concern.
```

```text
Seed may preserve claims long after they cease to be current.
```

```text
A fact may represent a justified claim without representing universal truth.
```

```text
Truth and currentness are different concepts.
```

```text
Projection selects a present interpretation; preservation retains historical
knowledge.
```

```text
A claim's provenance is as important as the claim itself.
```

```text
Claim strength should not exceed evidence strength without explicitly
acknowledging the gap.
```

```text
Temporal scope is part of claim meaning, not metadata that can be ignored.
```

## Implementation Implications

This reconciliation is documentation-only and does not require implementation
work.

However, it clarifies how future implementation and documentation should avoid
semantic overstatement:

- Do not use `fact` as shorthand for verified live truth.
- Do not use `current` without an implied or explicit projection and `as of`
  boundary.
- Do not treat historical facts as invalid merely because current state changed.
- Do not treat contradiction as deletion or automatic falsehood.
- Do not treat selection as verification.
- Do not treat corroboration as authority.
- Do not treat verification as timeless.
- Do not collapse local, remote, configured, observed, reachable, desired, and
  selected claims into one unscoped predicate.
- Do not strengthen natural-language responses beyond the evidence, support,
  projection, and verification scope.

## Non-Goals

This document does not:

- rename `Fact`;
- redefine existing schemas;
- require a new truth engine;
- require a new verification engine;
- require a new temporal model;
- require new contradiction resolution behavior;
- require changes to confidence aggregation;
- require changes to trust behavior;
- require changes to projections;
- require changes to tests;
- introduce runtime semantics;
- decide that Seed should prove universal truth.

## Conclusion

A Seed claim is a scoped proposition whose meaning depends on assertion strength,
provenance, support, time, and projection context.

Facts are normalized provenance-backed claims. Relationships are normalized
provenance-backed edges. Evidence explains why claims are available.
Observations preserve what sources reported. Projections select current
interpretations. Verification confirms scoped questions by declared methods.
Contradiction preserves competing support. History remains meaningful after
current state changes.

The architectural boundary is therefore:

```text
Seed should preserve claims conservatively, characterize their support
explicitly, select current interpretations through projections, and communicate
truth/currentness/verification only within the scope justified by provenance.
```
