---
status: audit
scope: expectation, continuity, and concern design-space investigation
created: 2026-06-17
---

# Expectation / Continuity / Concern Design Space Audit

## Status

Investigation only. No implementation changes were made to expectations, alerts,
topology monitoring, continuity tracking, HomeOps surfaces, lenses, views,
ingestion, state projection, fact support, measurement retention, stale fact
handling, storage topology projection, availability projection, current-facts
lookup, inference rules, predicate catalogs, or tests.

Short answer: repository authority does **not** currently contain a general
operational expectation concept that can say `example_host_b should see mount M`.
It contains current observations, current measurement support, optional expiry
for facts, stale-fact refresh recommendations, goals, capabilities,
verification status, read projections, and ambiguity surfaces. Those are
expectation-adjacent, but none is an explicit topology or visibility expectation.

The current implementation also does not preserve enough projected measurement
history to let expectations safely emerge from 180 days of repeated observation:
projected measurement history is intentionally bounded to the most recent sample
per canonical subject, predicate, and dimensions by default. The append-only
ledger remains authoritative history, but current State is not a continuity
model.

Therefore, under repository authority, the audit question remains open as a
design-space question rather than an implemented behavior. Evidence favors a
boundary-preserving interpretation: expectation is distinct from continuity and
concern, and any future expectation semantics would need explicit authority
about whether they are declared, inferred-with-caveat, or confirmed. This audit
does not select a winning model.

## Audit question

```text
Can expectations emerge from observation history?

Or must expectations be explicitly declared?
```

More generally:

```text
What is an expectation?
```

under repository authority.

## Prior findings reconciled

This audit treats these required documents as investigation inputs:

- `docs/filesystem_measurement_identity_boundary_audit.md`
- `docs/measurement_ownership_boundary_audit.md`
- `docs/ownership_model_design_space_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/lens_view_reconciliation.md`

The reconciled findings remain consistent with inspected repository evidence:

```text
visibility
    !=
ownership

visibility
    !=
operational concern

measurement subject
    !=
entity identity

ownership
    is not currently the strongest missing concept
```

The latest reconciliation's stronger gap is also supported:

```text
observed visibility
    vs
expected visibility
    vs
operator-significant deviation
```

The repository can currently express observed visibility through measurement
facts and read projections. It can express some ambiguity around storage
visibility without converting it into ownership. It cannot express expected
visibility or operator-significant deviation as first-class operational concepts.

## Repository evidence inspected

Implementation and catalog evidence inspected:

- `seed_runtime/facts.py`
- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/inference_rules.py`
- `seed_runtime/inference_catalog.py`
- `seed_runtime/predicate_catalog.py`
- `predicate_catalog/core.json`
- `inference_catalog/core.json`
- `seed_runtime/relationship_catalog.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/observation_normalizers.py`
- `seed_runtime/predicate_normalizers.py`
- `seed_runtime/integrity_summary.py`

Relevant tests inspected by repository search and targeted reading:

- `tests/test_observation_sources.py`
- `tests/test_predicate_normalizers.py`
- `tests/test_observation_normalizers.py`
- `tests/test_inference_catalog.py`
- `tests/test_ansible_inventory_source.py`
- `tests/test_capability_inventory.py`
- `tests/test_rule_inventory.py`
- storage/state-summary/current-facts tests located through repository search

Relevant documentation inspected or reconciled:

- the five required input documents listed above
- `docs/continuity_frontier.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/storage_measurement_current_fact_regression_audit.md`
- `docs/availability_vocabulary_audit.md`
- `docs/prediction_forecasting_and_future_claims_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/capability_verification_promotion_reconciliation.md`

## Candidate models

### Model A: Historical Expectation

```text
repeated observation
    ->
continuity
    ->
expectation
```

Example:

```text
example_host_b has seen mount M
for 180 days

therefore expectation emerges
```

#### Strengths

- It matches a common operator intuition: a long-running observed pattern can
  become operationally meaningful.
- It does not require the operator to predeclare every intended visibility edge.
- It could explain why losing a historically visible mount may deserve attention
  even when no ownership relation is known.
- It aligns with the latest gap framing if used carefully: current observation
  can be compared against an observation-derived baseline.

#### Risks

- The repository's prediction/forecasting boundary warns against turning past
  evidence into future claims without explicit authority. A historical pattern
  can support `has often been observed`; it does not automatically support
  `should continue`.
- Current State intentionally retains only bounded measurement samples by
  default, so State cannot currently substantiate `180 days` of repeated
  filesystem visibility without rereading ledger history or another history
  source.
- Repetition can be accidental. A mount visible for 180 days might be expected,
  deprecated, misconfigured, or merely incidental.
- Treating continuity as expectation risks collapsing three different concepts:
  survival of a pattern, normative obligation, and operator concern.

#### Compatibility with repository authority

Partially compatible as an investigation hypothesis, not as current authority.
The append-only ledger can preserve observation history, but the projected State
model deliberately reduces measurements to current samples for support and read
projection. Historical repetition can be evidence for continuity, but repository
authority does not currently promote it to expectation.

### Model B: Declared Expectation

```text
operator declares:

example_host_b
should see
mount M
```

Expectation exists only because it was explicitly stated.

#### Strengths

- Best preserves the repository's existing caution around goals, policy,
  recommendations, ownership, prediction, and unsupported inference.
- Cleanly distinguishes `was seen` from `should be seen`.
- Avoids treating incidental observations as operational requirements.
- Gives operator-significant deviation a clear reference point.

#### Risks

- It may miss important emergent operational concerns when no expectation has
  been declared.
- It may impose high operator modeling burden before useful concern surfaces can
  exist.
- It can make Seed blind to historically stable visibility losses except as raw
  observation changes or ambiguity.

#### Compatibility with repository authority

Strongly compatible with existing boundary preservation, but not currently
implemented as a topology/visibility expectation. The repository has explicit
operator-goal concepts and policy/authority vocabulary, but no implemented
predicate or relationship with the semantics `subject should see target`.

### Model C: Hybrid

```text
history suggests expectation

operator confirms expectation
```

#### Strengths

- Preserves evidence discipline: history can suggest, but operator confirmation
  supplies authority.
- Avoids silently converting observation into obligation.
- Supports an intermediate category such as candidate expectation or unresolved
  concern without making it truth.
- Fits the repository's broader pattern of ambiguity surfaces and caveated
  candidates, such as shared-storage candidates that are explicitly not topology
  truth or ownership.

#### Risks

- Requires careful vocabulary so `suggests` does not become hidden prediction or
  hidden expectation.
- Requires a boundary between observation continuity evidence and confirmed
  expectation authority.
- Could create operator-facing pressure that behaves like an alert unless that
  boundary is preserved.

#### Compatibility with repository authority

Architecturally plausible, but not implemented. It best matches existing
caution around candidates, ambiguity, and operator authority if kept as a design
space rather than an implementation conclusion.

### Model D: No Expectation Concept

Repository remains visibility-only.

#### Strengths

- Exactly preserves current implemented boundaries.
- Avoids prediction, normative claims, alert semantics, and ownership inference.
- Keeps read projections deterministic over projected facts.

#### Risks

- A loss of historically meaningful visibility can only be reported as current
  absence, stale evidence, conflict, or ambiguity. It cannot be classified as a
  deviation from what should be visible.
- Useful concern surfaces become limited to evidence quality, staleness,
  ambiguity, conflicts, and current observed health/availability. They cannot
  answer why `example_host_b no longer sees mount M` matters unless that concern is
  encoded elsewhere.
- The example_host_b scenario's operator-significant part is hard to explain without
  either expectation, goal context, or declared operational concern.

#### Compatibility with repository authority

Fully compatible with current implementation, but incomplete for the scenario's
`operator should eventually be informed` clause.

## Continuity analysis

Under repository authority, continuity is not simply stored history. The
continuity frontier treats continuity as survival of a question, gap, finding,
relationship, or working position across change, with persistence and lineage as
possible evidence rather than proof.

For runtime measurements, current State does not currently preserve full
continuity evidence. The `StateProjector` has a `measurement_history_limit` with
default `1`, and measurement retention keeps only recent samples per canonical
subject, predicate, and dimensions in projected State. `FactSupport` for
measurements is explicitly `current_sample`, not aggregate support across many
historical values. Durable facts aggregate support; measurements do not.

Consequences:

- Continuity of a mount's visibility might be reconstructible from the
  append-only ledger if historical events are retained and queryable.
- Continuity is largely discarded from projected State for volatile measurements
  by default.
- Current projections can show current visibility, current counts, and current
  ambiguity; they do not show `example_host_b saw M continuously for 180 days`.
- Staleness can indicate that a fact's evidence has expired, but it does not
  mean a former visibility pattern should still hold.

Therefore, continuity can be determined only by consulting historical evidence
outside the default current State projection, or by changing the question to a
current one. It is not currently a first-class State concept for filesystem
visibility.

## Expectation analysis

An expectation, in this design space, is not merely a fact that something was
observed. It is the reference condition against which observed visibility can be
compared to identify deviation.

Under repository authority, an expectation would need to answer at least:

```text
what subject is expected to see what target?
under what scope or dimensions?
according to whose authority?
for what time or freshness window?
what counts as satisfied, unknown, stale, or deviating?
```

No inspected predicate, relationship, projection, lens, or view currently has
that full semantics.

### Expectation-like concepts discovered

| Concept | Exists today? | Why it is expectation-like | Why it is not this expectation |
|---|---:|---|---|
| Fact expiry / staleness | Yes | Encodes freshness limits and refresh pressure. | It says evidence is old, not that a topology condition should hold. |
| Stale fact refresh recommendations | Yes | Suggests a capability to refresh stale knowledge. | It is about evidence maintenance, not expected visibility. |
| Goals | Yes | Can express desired outcomes and relevance. | A goal is operator-owned context, not a mount visibility assertion. |
| Policy / requirements vocabulary | Partly in docs | Can express constraints or requirements. | No implemented topology expectation relation was found. |
| Capability verification | Yes | Distinguishes verified/provider-reported/unverified capability evidence. | Verification status is about capability support, not `example_host_b should see M`. |
| Availability status | Yes | Expresses scoped current up/down/unknown evidence. | It is observed/projected availability, not an expectation of future or intended availability. |
| Current-facts behavior | Yes | Provides best current belief or current samples. | It has no missing-expected comparison. |
| Storage topology ambiguity | Yes | Surfaces uncertainty about observed filesystem topology. | It explicitly avoids topology truth, ownership, and expectations. |
| Inference rules | Yes | Derive health from availability and management facts. | Existing rules preserve subject and do not derive expectations. |
| Predicate catalog | Yes | Classifies predicates as durable facts or measurements. | No expectation predicate was found. |

### Fact, relationship, projection, lens, view, or other?

Repository evidence does not clearly select one representation.
Architectural fit differs by meaning:

- If an expectation is asserted by an operator or policy authority, it resembles
  a durable fact or relationship with provenance and authority.
- If an expectation is a comparison result, it resembles a read projection over
  observed state and expectation authority.
- If an expectation is merely a bounded operator question, it could be lens-like
  vocabulary, but lenses do not create new State authority.
- If an expectation is only a view presentation, it would be too weak to explain
  deviation semantics because views should not invent authority.

This audit does not choose a representation. It only finds that current
repository authority lacks the concept required to compare expected visibility
with observed visibility.

## Concern analysis

A concern is not the same as expectation. A concern is operator-significant
pressure: something may deserve attention, investigation, clarification, or
communication.

Current repository surfaces can already create some concern without expectation:

- stale facts can create refresh concern;
- conflicts can create evidence reconciliation concern;
- graph issues can create structural concern;
- storage topology ambiguities can create clarification concern;
- endpoint availability down can create current health concern for that endpoint;
- capability unverified/stale states can create capability-confidence concern.

But the example_host_b example's specific concern is a deviation concern:

```text
example_host_b used to see mount M
example_host_b no longer sees mount M
this matters because example_host_b was expected to see M, or because history suggests
that losing M may be operator-significant
```

Without an expectation or an explicitly caveated candidate expectation, the
repository can surface only `currently not visible`, `stale`, `ambiguous`, or
`down` evidence. It cannot say `deviation from expected visibility`.

## Operational example analysis

Scenario:

```text
example_host exports storage

example_host_b mounts storage

example_host_b has historically seen the mount

example_host_b loses visibility

ingestion becomes uneven

operator should eventually be informed
```

### What current repository authority can express

- Prometheus or local observation can produce filesystem measurement facts on a
  measurement subject, often an endpoint-shaped Prometheus instance for
  Prometheus metrics.
- Filesystem measurements can include dimensions such as mountpoint, device,
  and filesystem type.
- Storage projection can show current complete filesystem rows when both free
  and total measurements exist with matching subject and dimensions.
- Storage topology projection can group where a mountpoint path is currently
  visible and can surface ambiguity from observed filesystem fields.
- Availability projection can represent endpoint-scoped `availability_status`
  and derived same-subject health.
- Current-facts lookup can answer current fact questions, subject to predicate
  cardinality, dimensions, expiry, and alias boundaries.

### What current repository authority cannot express

- `example_host exports storage` as authoritative storage topology, unless some
  existing explicit fact or relationship asserts it in the current data.
- `example_host_b is intended to mount storage from example_host` as a requirement.
- `example_host_b should see mount M` as an expectation.
- `example_host_b losing M is an operator-significant deviation` without an expectation,
  goal, or declared concern context.
- `ingestion becomes uneven because of storage visibility loss` as causality,
  unless separately supported by evidence.

### Concepts required to explain the scenario

| Clause | Required concept | Existing status |
|---|---|---|
| `example_host exports storage` | storage topology/export relationship or fact | Not generally established by current storage measurements alone. |
| `example_host_b mounts storage` | observed filesystem visibility on example_host_b or its endpoint | Partly supported through filesystem measurement subject and dimensions. |
| `example_host_b has historically seen the mount` | observation history / continuity evidence | Ledger may contain history; current State mostly discards measurement history by default. |
| `example_host_b loses visibility` | observed current absence or changed current measurement set | Partly expressible by comparing current projections over time, not as a persisted continuity concept. |
| `ingestion becomes uneven` | ingestion health/quality measurement or operational symptom | Not established by filesystem projection alone. |
| `operator should eventually be informed` | concern/notification/attention semantics | Not implemented; not derivable from visibility alone. |

### Ownership or expected visibility?

The example does not require ownership as the first missing concept. It requires
expected visibility or a confirmed concern relation. Knowing who owns the storage
could help route responsibility, but the deviation is explainable as:

```text
example_host_b was expected to see mount M
example_host_b currently does not see mount M
therefore there is a visibility deviation
```

That statement does not require knowing that example_host owns the storage. It does
require knowing what `expected` means and who authorized it.

## Boundary preservation analysis

### Continuity vs expectation vs concern

| Concept | Repository-authority meaning | Boundary |
|---|---|---|
| Continuity | Survival of a pattern, relation, inquiry, or working position across time/change, supported by evidence but not identical to storage. | Does not by itself mean `should continue`. |
| Expectation | A reference condition for comparison: what should be visible, true, fresh, or maintained under some authority and scope. | Does not by itself mean alert, ownership, or causality. |
| Concern | Operator-significant pressure to investigate, clarify, communicate, or act. | Can arise from expectation deviation, staleness, conflict, ambiguity, or goals, but is not identical to any one of them. |

### Can a deviation be detected without first defining an expectation?

A change can be detected without expectation. A missing current observation can
be detected if prior/current snapshots are compared. Staleness can be detected
from expiry. Ambiguity can be detected from current projection shape.

A **deviation from expectation** cannot be detected without some expectation or
baseline semantics. Otherwise the repository can only say `different from a
prior observation` or `not currently observed`, not `unexpected`.

### Can expectation emerge from observation history without introducing prediction?

Only in a weak, caveated sense. History can support a statement like:

```text
example_host_b has repeatedly observed mount M in the past
```

It can also support a candidate baseline if the repository defines such a
baseline. But the step from `has repeatedly observed` to `should observe` is a
future-oriented or normative claim unless explicitly bounded as a candidate,
assumption, or operator-confirmed expectation. Under current repository
authority, silently making that step would introduce prediction or obligation.

### Which candidate model best preserves existing boundaries?

Repository evidence does not clearly support selecting a winning model.
Boundary preservation ranks the models as follows without recommending
implementation:

- Model D preserves current implementation exactly but cannot explain the full
  operational example.
- Model B preserves authority most strictly if expectations are needed, because
  it avoids silent inference from visibility history.
- Model C appears most compatible with existing candidate/ambiguity patterns if
  future work wants history to inform operator-confirmed expectations.
- Model A is the riskiest under current authority because it most directly turns
  repeated observation into `should` semantics.

## Architectural risks

1. **Prediction leakage:** historical observation can become an implicit future
   claim if not caveated.
2. **Normativity leakage:** `was visible` can become `should be visible` without
   operator or policy authority.
3. **Alert leakage:** concern surfaces can become alerting without declared
   thresholds, timing, escalation, or responsibility.
4. **Ownership relapse:** expectation may be confused with ownership even though
   expected visibility does not require owner knowledge.
5. **Identity collapse:** mount visibility on an endpoint can be mistaken for
   host identity or stable storage identity.
6. **Projection authority creep:** a read projection or lens can accidentally
   create new State authority.
7. **History overclaim:** current State's bounded measurement retention can be
   misread as sufficient evidence for long-term continuity.
8. **Causality overclaim:** uneven ingestion can be correlated with mount
   visibility loss without being caused by it.

## Recommended next investigation

Investigation only; no implementation recommendation is made here.

The next useful audit would be a narrow authority inventory for expectation-like
language across goals, policy, requirements, capability verification, stale fact
refresh, and topology documents, asking:

```text
Which existing authority, if any, may state `should`?

Can `should` apply to visibility without becoming prediction, alerting, or
ownership?

What evidence would distinguish historical baseline, declared expectation,
confirmed expectation, and operator concern?
```

A second follow-up could inspect ledger-level measurement event history to
answer whether long-running visibility continuity is recoverable in practice
from existing event retention, separately from projected State.

## Non-conclusions

- This audit does not implement expectations.
- This audit does not implement alerts.
- This audit does not implement topology monitoring.
- This audit does not implement continuity tracking.
- This audit does not implement HomeOps surfaces.
- This audit does not implement lenses or views.
- This audit does not recommend a new predicate, relationship, schema, or API.
- This audit does not conclude that ownership is needed for the example_host_b example.
- This audit does not conclude that history alone can create an expectation.
- This audit does not conclude that expectations must be declared; it finds that
  current repository authority does not already implement implicit expectations.
