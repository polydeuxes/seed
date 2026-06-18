---
status: audit
scope: baseline, continuity, expectation, and concern architectural investigation
created: 2026-06-17
---

# Baseline / Continuity / Expectation Audit

## Status

Investigation only. No implementation changes were made to baselines,
expectations, concerns, alerts, HomeOps, SeedOps, projection behavior, lenses,
views, fact support, staleness handling, refresh recommendations, measurement
retention, storage topology projection, verification, goals, requirements, or
runtime behavior.

Short answer: under current repository authority, **baseline is not merely the
same thing as continuity evidence**, but the repository also does not yet contain
a general first-class baseline concept for operational topology such as:

```text
example_host_b normally sees mount M
```

The strongest repository-preserving interpretation is that baseline is a
candidate architectural concept between continuity and expectation: it can name a
reference condition used for comparison without itself saying `should continue`.
That makes baseline distinct from expectation, because expectation requires a
named authority source capable of saying `should`. It also makes baseline
distinct from raw continuity evidence, because continuity only says a pattern
survived across observations; a baseline would select or frame some condition as
the comparison reference for a question.

Current evidence does **not** justify selecting a winning implementation model.
It does justify preserving these distinctions for further investigation:

```text
continuity evidence
    = historical survival / repeated observation / pattern persistence

baseline candidate
    = selected or interpreted reference condition for comparison

expectation
    = authority-backed stance that a condition should hold or continue

concern
    = operator-significant pressure, ambiguity, degraded knowledge quality, or
      deviation noticed without necessarily asserting should
```

Therefore, the repository appears to need the baseline question resolved before
expectation can be discussed safely for the example_host_b scenario. A baseline-like
reference could help an operator ask whether a visibility change is significant
without prematurely asserting that the mount was required.

## Audit question

```text
What is a baseline?
```

More specifically:

```text
Is a baseline merely continuity evidence?

Or is it a distinct architectural concept?
```

The operational pressure behind the question is:

```text
example_host_b has observed mount M
for a long period of time

example_host_b stops observing mount M

operator notices change

operator wonders whether change is significant
```

The audit evaluates how these concepts participate:

```text
observation
visibility
continuity
baseline
expectation
concern
```

## Prior findings reconciled

Required documents reconciled as investigation inputs:

- `docs/expectation_continuity_concern_design_space_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/lens_view_reconciliation.md`

Their findings remain mutually compatible with the inspected repository evidence:

1. Current repository authority supports observation, evidence, current facts,
   current support, visibility projections, staleness, refresh recommendations,
   read projections, goals, policy, requirements inside validation boundaries,
   capability verification, and lens-like interpretation.
2. Current repository authority does not contain a general operational
   expectation capable of saying `example_host_b should see mount M`.
3. History can support continuity evidence, but current projected State is not a
   general continuity model: measurement projection defaults to keeping the
   latest sample per canonical subject, predicate, and dimensions while the
   append-only ledger remains the historical authority.
4. Visibility can exist without ownership. The storage projection can group
   visible mount paths and produce shared-storage candidates while explicitly
   avoiding ownership, storage identity, and topology authority.
5. Concern can exist without expectation. Ambiguity, changed visibility,
   stale support, refresh need, and operator-significant pressure can be surfaced
   without converting them into normative should-claims.
6. Lens/view language is useful for bounded interpretation over projected State,
   but it does not create new State authority or operational truth.

The reconciled chain remains:

```text
Observation
    ->
Visibility
    ->
Continuity
```

But the repository does not currently authorize this automatic promotion:

```text
Continuity
    ->
Expectation
```

Baseline is the unresolved candidate between those chains. The key question is
whether a baseline can provide a comparison reference without becoming an
expectation.

## Repository evidence inspected

Implementation evidence inspected:

- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/policy.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/preconditions.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `predicate_catalog/core.json`
- `inference_catalog/core.json`

Tests inspected by targeted search and reading:

- `tests/test_fact_support_aggregation.py`
- `tests/test_temporal_characterization.py`
- `tests/test_state_summary_views.py`
- `tests/test_integrity_summary.py`
- `tests/test_capability_verification_inspection.py`
- `tests/test_policy.py`
- `tests/test_state_views.py`
- `tests/test_inference_catalog.py`
- `tests/test_observation_sources.py`
- `tests/test_predicate_normalizers.py`

Documentation inspected or reconciled:

- the four required input documents listed above
- `docs/continuity_frontier.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/prediction_forecasting_and_future_claims_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/storage_measurement_current_fact_regression_audit.md`
- `docs/availability_vocabulary_audit.md`
- `docs/capability_verification_promotion_reconciliation.md`
- `docs/state_summary_scope_review.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`

## Candidate models

### Model A: Baseline = Historical Continuity

```text
repeated observation
    ->
continuity
    ->
baseline
```

#### What it explains

This model explains the operator's intuition in the example_host_b scenario. If
example_host_b has observed mount M for a long period, then loss of that observation is
significant because it deviates from a long-lived pattern. It does not require
up-front declaration of every mount that matters.

#### Repository support

The append-only ledger can preserve repeated historical observations. The
continuity frontier supports the idea that continuity is weaker than identity but
stronger than mere resemblance. Fact support also preserves source, observed
history, and support metadata for current projected facts.

#### Boundary risks

This model is too strong if it means continuity automatically becomes a baseline
with operational standing. Current measurement projection treats measurements as
volatile current samples, not as cumulative support. Repeated measurement values
do not strengthen support like durable facts. By default, projected State keeps
only recent measurement samples for each series even though ledger events remain
available. Therefore, the current State projection cannot itself substantiate
`long period of time` as a baseline.

This model also risks smuggling in expectation. A statement such as:

```text
example_host_b has always seen M, therefore M is baseline, therefore loss matters
```

is safe only if `matters` means comparison-worthy or attention-worthy. It is not
safe if it means:

```text
example_host_b should still see M
```

#### Compatibility

Partially compatible as a source of baseline evidence. Not compatible as an
automatic promotion rule from history to authoritative baseline or expectation.

### Model B: Baseline = Declared Reference State

```text
operator selects
reference condition

reference condition
    ->
baseline
```

#### What it explains

This model clearly distinguishes baseline from continuity. A baseline exists
because an operator, policy, requirement, workflow, imported source, or other
named authority selected a reference condition. Historical continuity may inform
that selection but does not itself bind it.

For example_host_b, an operator could declare:

```text
For this investigation, compare current example_host_b mount visibility to the selected
reference condition in which example_host_b saw mount M.
```

That can support deviation analysis without asserting that example_host_b must continue
to see M.

#### Repository support

This model best matches current authority discipline. The should-authority audit
shows that `should` requires a named scope and source. The goal/policy authority
work shows that Seed must not silently invent objectives or obligations.

#### Boundary risks

This model may be too narrow if all baseline usefulness requires explicit human
declaration. Operators often need Seed to notice historically stable changes
before they know what to declare. If every baseline must be manually selected,
then continuity evidence cannot help with discovery except as raw history.

#### Compatibility

Strongly compatible with current authority boundaries, provided the declaration
is scoped as a reference for comparison and not silently upgraded into
expectation or policy.

### Model C: Baseline = Projection

```text
current State
    +
historical evidence
    ->
baseline projection
```

#### What it explains

This model treats baseline as a derived read/projection result. It would answer:

```text
What reference condition is supported by the current projection plus historical
ledger evidence?
```

For example_host_b, a baseline projection could summarize that example_host_b historically had
mount M visible and current projected State no longer has the current sample.

#### Repository support

The projection architecture supports deterministic read models derived from
ledger events and projected State. Projection stores cache current derived State
snapshots while preserving the ledger as authority. Existing storage projection
already derives current filesystem surfaces, cluster mount groups, and
projection-only ambiguity from current measurements.

#### Boundary risks

Current projection architecture mostly stores current state snapshots, not a
historical as-of or continuity model. A baseline projection that uses history
would need to declare its evidence source and retention assumptions. If it only
uses current State, it will likely miss the long-period evidence because
measurement history is bounded. If it reads the ledger, it must avoid becoming a
new hidden authority that overrides State boundaries.

#### Compatibility

Compatible as an investigation direction if `baseline projection` is explicitly
read-only, provenance-preserving, and caveated. Not currently implemented.

### Model D: Baseline = Lens Interpretation

```text
baseline
```

does not exist in State. A lens interprets continuity evidence as a baseline.

#### What it explains

This model fits the lens/view reconciliation. A lens answers a bounded question
over projected State or repository knowledge. Under this model, baseline is not a
stored State object. Instead, a continuity or topology lens interprets historical
visibility evidence as a baseline-like comparison frame for the operator's
question.

For example_host_b, the lens would say:

```text
Compared with the observed historical visibility pattern, current example_host_b mount
visibility differs because M is no longer observed.
```

It can preserve caveats:

```text
This is a comparison reference, not ownership, topology truth, alert authority,
or an expectation that M should continue.
```

#### Repository support

Existing lens authority supports bounded question-answering, attention shaping,
classification, compression, and interpretation over projected State. Existing
storage topology ambiguity is already projection-only and boundary-preserving.

#### Boundary risks

Lens authority is weaker than State and is not a canonical runtime primitive.
If baseline exists only as lens interpretation, it may be difficult to preserve,
compare, audit, or reuse across surfaces. The lens must also avoid inventing a
reference condition when history is unavailable in current State.

#### Compatibility

Compatible as vocabulary for investigation. Not sufficient as current runtime
authority because formal lenses are not implemented as a general primitive.

### Model E: No Baseline Concept

Continuity evidence is sufficient. No separate baseline concept is needed.

#### What it explains

This model preserves minimal architecture. Example host's change could be described
without introducing baseline:

```text
Historical evidence: example_host_b repeatedly observed M.
Current evidence: example_host_b no longer observes M.
Concern: operator may want to investigate changed visibility.
```

#### Repository support

The repository already supports observations, facts, current measurement
projection, stale facts, refresh recommendations, ambiguity surfaces, and
concern-like pressure without baseline. Avoiding a new concept reduces risk of
ontology expansion.

#### Boundary risks

Without baseline, the repository lacks a name for the reference condition used
in comparison. Operators often ask not merely `what changed?` but `compared to
what?` If continuity evidence is sufficient, every consumer must independently
express the comparison reference. That risks either repeatedly rediscovering the
same boundary or silently upgrading continuity to expectation.

#### Compatibility

Compatible with current implementation, but it may be insufficient for the audit
question because it leaves the comparison-reference role unnamed.

## Continuity analysis

Continuity answers:

```text
What survived or persisted across observations despite change?
```

In the example_host_b example, continuity evidence would be:

```text
example_host_b observed mount M repeatedly over a long period
```

Under current repository authority, this is historical evidence, not current
State truth unless the relevant facts still exist in projection or are read from
the ledger. For measurements, current projected State intentionally privileges
current samples. Measurement support has `support_kind = current_sample`; older
measurement samples do not aggregate into stronger support for the current
measurement claim.

Continuity is therefore evidence-bearing but not automatically reference-bearing
or authority-bearing:

- It can say a pattern existed.
- It can support a candidate reference condition.
- It can explain why a change is noticeable.
- It cannot by itself say the pattern was intended, required, healthy,
  operator-approved, or should continue.

For the audit's first required question, continuity differs from baseline and
expectation as follows:

| Concept | Primary question | Example host example | Boundary |
| --- | --- | --- | --- |
| Continuity | What pattern survived across observations? | example_host_b historically observed M. | Does not select a reference by itself and does not say should. |
| Baseline | What reference condition is used for comparison? | compare current example_host_b visibility against a reference where M was visible. | May be evidence-backed or declared, but must not automatically become should. |
| Expectation | What condition is authority-backed as anticipated or required? | example_host_b should see M. | Requires named authority; history alone is insufficient. |

## Baseline analysis

Baseline appears to be a distinct architectural role, even if it is not yet a
first-class repository concept.

A baseline would answer:

```text
Compared to what reference condition is this change evaluated?
```

That is not identical to continuity. Continuity can provide candidate evidence,
but baseline involves selection, framing, or interpretation of a reference state.
The same continuity evidence can support multiple possible baselines:

```text
example_host_b normally sees M
cluster nodes normally see M
this mountpoint normally appears on nodes in group G
this investigation compares against the last known complete observation
this investigation compares against the operator-selected pre-change condition
```

Those are different comparison references even when they are supported by the
same observation history.

Baseline can also differ from expectation. A baseline can be used to detect or
explain deviation without asserting that the baseline is desired or required.
For example:

```text
Baseline-like comparison: example_host_b previously observed M.
Current observation: example_host_b no longer observes M.
Concern: this is a visibility deviation worth explaining.
No expectation asserted: the audit does not claim example_host_b should see M.
```

Therefore, a baseline can exist without expectation if it is scoped as a
reference condition rather than an obligation. Conversely, expectation can exist
without a baseline if an authority directly declares:

```text
example_host_b should see mount M
```

without deriving that statement from a historical reference. That expectation
would be under-supported operationally unless it named its authority and perhaps
its evidence, but it would not require a baseline to exist conceptually.

## Expectation analysis

Expectation answers:

```text
What condition is anticipated, intended, required, or otherwise should-bearing
under a named authority?
```

The required documents and implementation evidence continue to show no general
operational expectation authority for `example_host_b should see mount M`. The
repository contains should-like concepts in bounded domains:

- policy constraints over behavior;
- goals as operator-owned desired outcomes;
- requirements and expected types inside validation or catalog boundaries;
- decisions and approvals inside action lifecycles;
- refresh recommendations as advisory evidence-acquisition pressure;
- capability verification as support/readiness evidence without execution or
  selection authority.

None of these currently supplies a general topology expectation. In the example_host_b
example, expectation would require extra authority such as an operator-declared
requirement, policy, goal-linked supporting-condition model, imported inventory,
or accepted expectation record. Historical visibility alone does not provide
that authority.

## Example host example analysis

Scenario:

```text
example_host_b has observed mount M
for a long period of time

example_host_b stops observing mount M

operator notices change

operator wonders whether change is significant
```

### Observation

Observation records source-attributed reports at observation times. The relevant
observations are Prometheus or other measurement reports that example_host_b had
filesystem visibility for M, followed by a later report in which M is missing or
no current complete filesystem measurement for M exists.

Observation does not assert truth beyond the report. It does not say M belongs
to example_host_b, should be mounted, or is operationally required.

### Visibility

Visibility is the current or historical fact that M was seen from a subject or
vantage point. Existing storage projection can represent current filesystem
visibility by subject, mountpoint, and dimensions, and can group mount visibility
across endpoints.

For example_host_b:

```text
Before: example_host_b had visibility of mount M.
After: current projection no longer contains complete current visibility of M
       for example_host_b.
```

Visibility remains separate from ownership and expected topology.

### Continuity

Continuity is the survival of the observed pattern over time:

```text
example_host_b repeatedly observed M across many samples or observation events.
```

Continuity helps explain why the disappearance is not just a single isolated
absence. However, current State may not retain the long history unless the ledger
is consulted or the projection was built with a larger measurement history
limit. The current projection is not itself a continuity authority.

### Baseline

A baseline would be the comparison reference:

```text
For this question, treat example_host_b-sees-M as the reference condition being compared
against current visibility.
```

That reference could be:

- selected by the operator;
- suggested by historical continuity evidence;
- generated as a read-only projection from ledger history;
- interpreted by a lens over continuity evidence;
- or not represented separately at all.

The key boundary is that baseline-as-reference does not assert:

```text
example_host_b should see M
```

It only says:

```text
current example_host_b visibility differs from the reference condition.
```

### Expectation

Expectation would say:

```text
example_host_b should continue seeing mount M
```

Current repository authority cannot make that assertion from history alone. It
would need an authority source, such as an operator-declared expectation,
requirement, policy, goal-derived dependency accepted by the operator, or an
imported authoritative topology record.

### Concern

Concern can arise before expectation. The operator can legitimately wonder
whether the change is significant because there is a deviation from historical
visibility or from a selected comparison reference. That concern can be framed as
uncertainty, investigation pressure, ambiguity, or knowledge-quality need:

```text
example_host_b's current visibility differs from the historical/reference condition;
this may deserve investigation, but the repository has not asserted that the
mount should continue.
```

This preserves the boundary:

```text
baseline deviation
    ->
concern / question / investigation pressure
    !=
should violation
```

## Authority analysis

Repository authority supports these boundaries:

### Observation history

The append-only ledger is the source of historical events. Projected State is a
current read model derived from those events. Measurement history in State is
bounded by default; historical continuity claims must either cite retained
projection evidence or consult ledger history.

### Fact support

Fact support distinguishes durable aggregate support from volatile measurement
current samples. Durable facts can aggregate repeated independent observations.
Measurement predicates are treated as current samples, and repeated values do not
increase support in the same way.

This matters for baseline because filesystem visibility is measurement-like. A
long-running measurement series may provide baseline evidence in the ledger, but
current fact support does not automatically turn repeated samples into a
baseline.

### Staleness handling and refresh recommendations

Staleness means support has expired for current use; it does not mean the claim
is false. Refresh recommendations are deterministic advisory signals for
acquiring newer evidence; they are not commands, truth claims, or operational
expectations.

In the example_host_b scenario, stale or missing mount evidence can create refresh or
investigation pressure without asserting that the mount should exist.

### Measurement retention

Measurement projection retains only recent samples per canonical subject,
predicate, and dimensions by default. This protects current State from becoming a
large time-series store, but it also means current State alone is weak evidence
for long-term continuity.

### Continuity-related documents

Continuity is exploratory and boundary-sensitive. It is distinct from identity,
persistence, lineage, and mere resemblance. Applying continuity to filesystem
visibility should therefore be careful: repeated mount visibility may support a
continuity candidate, but not ownership, topology truth, baseline selection, or
expectation by itself.

### Goal and requirement authority

Goals make knowledge relevant to operator-owned desired outcomes, while policy
and requirements can carry bounded should-authority. Current repository evidence
does not show a general requirement that maps `example_host_b` to `mount M` as an
intended visibility relation.

### Verification evidence

Capability verification is evidence about whether a capability candidate appears
supported or ready. It does not select a capability, authorize execution, or
create operational expectations. Verification-like concepts therefore do not
supply baseline authority for example_host_b.

### Projection architecture

Projection architecture supports read-only derived surfaces. A baseline could be
investigated as a projection or lens-like interpretation, but any such model must
state whether it reads current State, ledger history, or an explicit declaration.
It must not hide authority in a projection.

### Lens/view reconciliation

A lens can interpret and compress evidence for a bounded question, but current
lens language is not a formal runtime primitive. A baseline-as-lens model is
plausible but not implemented, and it must preserve caveats.

## Boundary preservation analysis

The candidate models preserve existing authority boundaries differently:

| Model | Boundary preservation | Main risk |
| --- | --- | --- |
| Model A: Historical Continuity | Moderate if history is only evidence; weak if continuity automatically becomes baseline. | Collapses repeated observation into selected reference or expectation. |
| Model B: Declared Reference State | Strong. Authority is explicit and scoped. | May underuse historical continuity for discovery. |
| Model C: Projection | Moderate to strong if read-only and provenance-preserving. | Current projection lacks long history; hidden projection could create unowned authority. |
| Model D: Lens Interpretation | Moderate. Fits bounded interpretation vocabulary. | Lens is not formal runtime authority; persistence and auditability are unclear. |
| Model E: No Baseline | Strong minimalism. | Leaves comparison-reference semantics unnamed and may force continuity/expectation collapse elsewhere. |

The model that best preserves current authority boundaries is **Model B** when
baseline means an explicitly scoped reference condition. However, repository
evidence does not require that all useful baselines be declared. Model C or Model
D may also preserve boundaries if they treat history-derived baselines as
candidate, caveated, read-only comparison references rather than expectations.

Therefore this audit does not select a single winning model. It narrows the safe
space:

```text
baseline may be a reference condition for comparison;
baseline must not silently become expectation;
history may support baseline candidates;
current State is not enough for long-term measurement baselines by default;
concern may arise from baseline deviation without should-authority.
```

## Required questions answered

### 1. What is the difference between continuity, baseline, and expectation?

Continuity is evidence that a pattern survived across observations. Baseline is
a selected or interpreted reference condition for comparison. Expectation is a
should-bearing or anticipated condition under named authority.

### 2. Can a baseline exist without expectation?

Yes, if baseline is scoped as a comparison reference. Example:

```text
Use the historical example_host_b-sees-M condition as the reference for this
investigation.
```

That does not assert:

```text
example_host_b should see M.
```

### 3. Can expectation exist without a baseline?

Yes. An operator, policy, requirement, or other authority could declare:

```text
example_host_b should see M
```

without deriving it from a baseline. It would still need authority and support,
but conceptually the expectation does not require a historical baseline.

### 4. Can concern arise from baseline deviation without asserting `should`?

Yes. A deviation from a comparison reference can create concern, ambiguity,
attention pressure, or a refresh/investigation need without becoming a violation
of expectation.

### 5. Would the example_host_b example benefit from baseline before expectation?

Yes. Baseline would let the repository explain the operator's question:

```text
Is current example_host_b visibility significant compared with the reference condition?
```

before requiring the stronger and currently unsupported statement:

```text
example_host_b should continue seeing M.
```

### 6. Is baseline evidence, projection, lens, view, interpretation, or other?

Current repository evidence supports baseline most safely as a **reference
condition role**. That role may be backed by evidence, surfaced by projection,
interpreted by a lens, or rendered in a view. It should not be collapsed into any
one of those implementation layers without further investigation.

### 7. Does the repository already contain baseline-like concepts under another name?

Yes, but only partially and in bounded forms:

- current sample support for measurement predicates;
- append-only historical ledger events;
- stale fact freshness windows and refresh recommendations;
- storage topology projection and ambiguity surfaces;
- shared-storage candidates and cluster mount visibility groups;
- presentation-only filesystem classification;
- policy, goals, requirements, approvals, and decisions as scoped authority
  concepts;
- capability preconditions called `baseline` in code, scoped to action-plan
  precondition inventory rather than environmental topology baselines;
- projection snapshots and derived index snapshots as cached read models, not
  historical baselines;
- lens-like interpretation and view surfaces.

None is a general operational baseline for visibility continuity.

### 8. Which candidate model best preserves existing authority boundaries?

Model B best preserves authority boundaries because it requires explicit
selection of the reference condition. However, the repository evidence also
supports investigating a boundary-preserving hybrid in which historical
continuity can suggest a candidate baseline, while declaration, projection, or
lens framing determines how the reference is used. This audit does not select a
winner because the repository does not yet contain decisive authority for one
model.

## Baseline-related concepts discovered

Baseline-like concepts discovered during inspection:

1. **Measurement current samples**: volatile predicates resolve to latest current
   samples rather than aggregate history.
2. **Durable fact support**: durable predicates aggregate supporting facts and
   confidence.
3. **Append-only ledger history**: historical observations remain available even
   when projected measurement samples are pruned.
4. **Stale fact refresh recommendations**: expired support creates advisory
   refresh pressure.
5. **Storage cluster mount groups**: projection-only grouping of where a mount
   path is currently visible.
6. **Shared-storage candidates**: projection-only interpretation from observable
   filesystem fields.
7. **Storage topology ambiguities**: unresolved interpretation pressure without
   facts, ownership, identity, or topology authority.
8. **Presentation-only filesystem classification**: view-oriented classification
   that explicitly avoids topology truth.
9. **Goals, policy, requirements, approvals, decisions**: scoped sources of
   should-like authority, none currently generalizing to mount visibility
   expectations.
10. **Capability precondition baseline**: a code-local use of `baseline` for
    capability precondition IDs, not environmental baselines.
11. **Projection snapshots and derived index snapshots**: cached read models
    derived from ledger-backed State, not reference-state baselines.
12. **Lens-like bounded interpretation**: architecture vocabulary that could
    frame baseline as interpretation, but not a formal primitive today.

## Recommended next investigation

No implementation is recommended here. The next investigation should determine
which authority source, if any, may select a baseline reference condition without
turning it into expectation. Suggested investigation questions:

1. Is a baseline always operator-selected, or can Seed present candidate
   baselines derived from ledger history with explicit caveats?
2. If history-derived candidate baselines are allowed, what evidence threshold or
   provenance shape is required to avoid accidental expectations?
3. Does a baseline need persistence, or can it remain an ephemeral lens/view
   interpretation for a specific operator question?
4. Should baseline comparison read ledger history directly, or only use current
   State and existing projections?
5. How should a baseline-deviation concern be worded so it never implies
   `should continue` without an expectation authority?
6. What is the minimal authority vocabulary needed to distinguish:

```text
reference condition
candidate baseline
accepted baseline
expectation
concern
```

These are investigation questions only, not implementation recommendations.

## Non-conclusions

This audit does not conclude that:

- a baseline ontology should be implemented;
- baseline records should be added to State;
- expectation records should be implemented;
- continuity history should be retained in current State;
- alerts, HomeOps, SeedOps, or operator dashboards should be created;
- example_host_b should see mount M;
- mount M is owned by example_host_b or any other host;
- loss of M caused ingestion unevenness;
- historical continuity is sufficient to create operational requirement;
- baseline must be declared in all cases;
- baseline must be a projection or lens in all cases;
- concerns require expectations.

The narrow conclusion is that baseline is plausibly a missing architectural
concept between continuity and expectation, but only if it is kept as a
comparison reference rather than a hidden should-authority.
