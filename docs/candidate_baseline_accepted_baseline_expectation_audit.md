---
status: audit
scope: candidate baseline, accepted baseline, expectation, continuity, concern, and authority investigation
created: 2026-06-17
---

# Candidate Baseline / Accepted Baseline / Expectation Audit

## Status

Investigation only. No implementation changes were made to baselines,
expectations, concerns, alerts, HomeOps, SeedOps, topology monitoring,
projection behavior, lenses, views, requirements, policy, goals, approvals,
decisions, capability verification, staleness handling, or verification evidence.

Short answer: repository evidence supports **candidate baseline** as distinct
from raw continuity evidence, because a candidate baseline selects historical or
observed continuity as a comparison reference for a question. Repository evidence
also supports the possibility of **acceptance** as a separate authority boundary,
because the repository already distinguishes candidates from promotions,
recommendations from decisions, and proposals from acceptances. However, current
repository authority does not contain a general operational `accepted baseline`
concept for topology visibility.

Therefore, the audit cannot conclude that accepted baseline is an implemented or
canonical concept. It can conclude that if the concept is introduced later, the
safest boundary-preserving meaning would be:

```text
candidate baseline
    = evidence-supported comparison reference candidate

accepted baseline
    = authority-selected comparison reference for a scoped purpose

expectation
    = authority-backed stance that a condition should hold, continue, or be
      anticipated under a named authority path
```

Under that reading, accepted baseline does **not** automatically mean `should
continue`. It means `compare against this reference for this scoped
investigation, view, assessment, or decision context`. Transforming it into an
expectation would require additional should-bearing authority such as a policy,
requirement, declared operator intent, accepted goal-to-condition relation,
design invariant, or other explicit normative source.

## Audit question

```text
What is the difference between

candidate baseline
accepted baseline
expectation?
```

More specifically:

```text
What authority, if any,
is required to move
from candidate baseline
to accepted baseline?
```

Operational example used throughout:

```text
node116 historically observes mount M
current visibility of M disappears
historical evidence suggests node116-sees-M is a useful comparison reference
operator is investigating whether the change matters
```

## Prior findings reconciled

Required documents reconciled:

- `docs/baseline_continuity_expectation_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/expectation_continuity_concern_design_space_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/lens_view_reconciliation.md`

The reconciled findings remain compatible:

1. Observation can support visibility; visibility can support continuity; neither
   automatically creates expectation.
2. Baseline is not identical to continuity, because baseline frames or selects a
   comparison reference while continuity only says a pattern survived or recurred.
3. Baseline is not identical to expectation, because expectation requires a
   named should-bearing or anticipation-bearing authority source.
4. History may support candidate baselines but does not authorize expectation by
   itself.
5. Concern can arise from ambiguity, visibility change, stale support, degraded
   evidence quality, or operator pressure without an expectation claim.
6. Lens/view concepts can present bounded interpretation over projected State,
   but they do not add State, truth, policy, or execution authority.

The established chain is therefore refined as:

```text
Observation
    -> Visibility
    -> Continuity evidence
    -> Candidate baseline
    ? authority selection
    -> Accepted baseline
    ? should-bearing authority
    -> Expectation
```

The question marks are the relevant authority boundaries. The repository does
not currently justify deleting either question mark.

## Files inspected

Required documents:

- `docs/baseline_continuity_expectation_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/expectation_continuity_concern_design_space_audit.md`
- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/lens_view_reconciliation.md`

Additional documentation inspected for authority, continuity, staleness,
verification, projection, and work-position boundaries:

- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/capability_verification_promotion_reconciliation.md`
- `docs/prediction_forecasting_and_future_claims_reconciliation.md`
- `docs/current_work_position_frontier.md`
- `docs/continuity_frontier.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/state_summary_authority_reconciliation.md`

Implementation evidence inspected:

- `seed_runtime/models.py`
- `seed_runtime/state.py`
- `seed_runtime/state_views.py`
- `seed_runtime/capability_promotion_readiness.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/policy.py`
- `seed_runtime/runtime_trace.py`

## Candidate baseline analysis

A candidate baseline is stronger than continuity evidence but weaker than an
accepted reference or expectation.

Continuity evidence says:

```text
node116 has repeatedly or historically observed mount M
```

A candidate baseline says:

```text
node116-sees-M may be a useful comparison reference for this investigation
```

The difference is selection and purpose. Continuity evidence may exist in large
quantity without being relevant to the active question. A candidate baseline is
continuity or historical evidence framed as potentially useful for comparison.
It remains candidate because no authority has yet accepted it as the reference
for the current investigation, view, assessment, or decision.

### Required question 1: What makes something a candidate baseline rather than continuity evidence?

A candidate baseline requires at least:

1. evidence of survival, recurrence, prior currentness, or historical support;
2. a bounded comparison question;
3. a reason the historical pattern might be relevant to that question;
4. caveats that it is not yet normative.

For node116, the raw continuity evidence is `node116 historically observed mount
M`. The candidate baseline is `use historical node116-sees-M as the reference
against which current disappearance is compared`.

### Required question 2: Can a candidate baseline exist without human involvement?

Yes, as a candidate. Repository boundaries around capability candidates and
promotion-readiness support this shape: evidence-derived candidates may exist
without becoming verified capabilities, selected capabilities, policy decisions,
or execution authority. By analogy, history-derived candidate baselines may be
machine-surfaced as possible comparison references, provided they retain their
candidate status and do not become accepted references or expectations.

For node116, a read-only inspection could notice that `node116-sees-M` has strong
historical support and current visibility is absent. That would justify a
candidate comparison reference, not an accepted baseline and not `node116 should
see M`.

## Accepted baseline analysis

An accepted baseline, if repository architecture later recognizes it, would be
an authority-selected comparison reference. It would answer:

```text
For this scope and purpose, compare current or future observations against this
reference condition.
```

It would not by itself answer:

```text
This condition should continue.
```

Current repository concepts resembling this boundary include:

- action plan acceptance, which changes a proposal's status without making it an
  executable command;
- refresh recommendation decisions, where acceptance/defer/reject selects a
  response without being the observation execution itself;
- capability promotion-readiness, which can report support for future promotion
  without performing promotion;
- policy approval gates, where approval authorizes a scoped behavior without
  proving environmental truth;
- goals, which can provide operator-owned relevance and desired-outcome context
  without selecting or authorizing actions.

These analogies support acceptance as a meaningful architectural boundary, but
not as a currently implemented baseline concept.

### Required question 3: What makes something an accepted baseline?

A candidate baseline would become an accepted baseline only when an authority
source selects it as the comparison reference for a named scope and purpose.
Possible authority paths include:

- operator acceptance for an investigation or view;
- decision record accepting the reference for an assessment;
- policy or requirement declaring a reference condition for a scope;
- workflow or review process recording that this reference should be used;
- verification or corroboration satisfying a predeclared acceptance rule.

The minimal acceptance record would need to preserve:

```text
reference condition
scope
purpose
accepting authority
supporting evidence
caveats
expiration or review conditions, if any
whether it is non-normative or expectation-bearing
```

### Required question 4: Can an accepted baseline exist without expectation?

Yes, if acceptance is scoped to comparison rather than normativity.

For node116, an operator might accept `node116-sees-M` as the investigation
baseline because historical evidence makes it useful for comparing the current
disappearance. That does not assert that node116 is required or intended to see
M. It only says the historical state is the reference for evaluating the change.

### Required question 5: Does accepting a baseline implicitly say `should continue` or merely `compare against this reference`?

Repository boundaries favor `compare against this reference`. Treating accepted
baseline as `should continue` would collapse acceptance into expectation and
would conflict with prior findings that history alone does not authorize should.
If a future baseline acceptance interface wants acceptance to carry normative
force, it would need to say so explicitly and name the should-bearing authority.

## Expectation analysis

Expectation is the first concept in this chain that can carry `should continue`
when supported by the right authority. Prior audits already found that current
repository authority has several should-like concepts, but no general
operational topology expectation that can say:

```text
node116 should see mount M
```

An expectation requires a source capable of taking an anticipatory or normative
stance. Depending on scope, that source could be an operator declaration, policy,
requirement, accepted design invariant, goal-derived requirement, external model,
or inference path with caveats. Expectation must retain provenance,
uncertainty, and scope. It should not be treated as truth merely because it is
represented.

For node116, expectation would be a separate claim such as:

```text
Under requirement R or policy P, node116 should continue seeing mount M while
service S is active.
```

That claim cannot be derived from history alone.

## Authority analysis

The repository already preserves several authority boundaries relevant to
baseline acceptance:

| Concept | Closest role for baseline question | Boundary preserved |
| --- | --- | --- |
| Approval | Authorizes scoped action or behavior | Approval is not environmental truth or expectation by itself. |
| Decision | Selects, accepts, rejects, defers, or escalates an option | Decision is not command, execution, goal, or fact truth. |
| Policy | Defines acceptable, required, prohibited, preferred, or approval-gated behavior | Policy can create requirements but is not identical to operator intent or evidence. |
| Goal | Operator-owned desired outcome | Goal provides relevance but does not select or authorize options by itself. |
| Requirement | Mandatory condition inside a scope | Strong candidate for transforming accepted baseline into expectation if it names the condition. |
| Verification | Evidence that a promotion or capability claim is supported | Verification support is not selection, policy, execution, or expectation. |
| Lens/view | Bounded interpretation or presentation over projected State | View presentation does not add truth or authority. |

### Required question 7: Which current repository concepts most closely resemble baseline acceptance?

The closest concepts are **decision** and **approval**, with support from policy
and verification. Decision is closest when the question is `which reference do
we accept for this investigation?` Approval is closest when using the accepted
baseline has governance implications. Policy or requirement is closest when the
accepted baseline is predefined by authority rather than selected ad hoc by an
operator. Verification is supporting evidence, not acceptance itself.

### Required question 10: What authority would be required to transform accepted baseline into expectation?

If accepted baseline and expectation remain distinct, transformation requires a
separate should-bearing source, for example:

```text
accepted baseline: compare current node116 visibility against historical
node116-sees-M

plus authority: requirement R says node116 must see M for service S

therefore expectation: node116 should see M while R applies
```

Acceptable authority paths could include:

- explicit operator declaration of intended state;
- policy rule or requirement naming the condition;
- accepted design invariant;
- goal plus validated supporting-condition model that authorizes the condition
  as necessary, not merely relevant;
- formal decision that records the baseline as normative and names the authority
  for doing so.

## Node116 example analysis

Scenario:

```text
node116 historically observes mount M
current visibility of M disappears
historical evidence suggests node116-sees-M is a useful comparison reference
operator is investigating whether the change matters
```

### Continuity

Continuity participates as historical survival or recurrence:

```text
node116-sees-M was observed across prior time or observations
```

It supports comparison but does not itself say whether disappearance is wrong.

### Candidate baseline

Candidate baseline participates as a proposed reference:

```text
Use node116's historical visibility of M as the reference for evaluating current
loss of visibility.
```

It can arise from history and may be surfaced automatically, but remains
non-normative.

### Accepted baseline

Accepted baseline would participate if an operator, decision, policy,
requirement, or workflow selects the candidate reference:

```text
For this investigation, compare current node116 mount visibility against the
historical node116-sees-M reference.
```

This could help the operator investigate significance before any expectation is
asserted.

### Expectation

Expectation would require extra authority:

```text
node116 should see M
```

or more safely:

```text
node116 should see M while service S or requirement R applies.
```

The repository evidence inspected does not provide that authority for the
example.

### Concern

Concern can arise earlier than expectation:

```text
current visibility deviates from an accepted or candidate baseline
operator is investigating whether the change matters
```

This is a concern because it is a potentially significant deviation, ambiguity,
or evidence-quality pressure. It need not claim that a requirement was violated.

### Required question 6: Would the node116 example benefit from accepted baseline semantics before expectation semantics?

Yes, conceptually. Accepted baseline semantics would let the system and operator
share a comparison reference without prematurely asserting a topology
expectation. This preserves the distinction between `historically normal for
node116` and `required for node116`.

### Required question 8: Can concern arise from deviation from an accepted baseline without asserting expectation?

Yes. A deviation from an accepted comparison reference can be operator-relevant
because it is a change from the reference condition. The concern is:

```text
this changed relative to the accepted reference and may matter
```

not necessarily:

```text
this violated a should
```

## Candidate models

### Model A: Candidate Baseline Only

```text
history -> candidate baseline
```

Repository-compatible as a conservative model. It preserves history as evidence
and avoids inventing acceptance or expectation. Its weakness is that all
consumers must interpret candidate baselines directly, which risks inconsistent
handling of scope, purpose, authority, and caveats.

For node116, this model says `node116-sees-M` is merely a candidate comparison
reference. Concern may be surfaced as candidate-baseline deviation, but no
accepted reference exists.

### Model B: Operator Acceptance

```text
history -> candidate baseline
operator -> accepted baseline
```

Repository-compatible as an architectural possibility. It resembles existing
operator-owned goals and decision/acceptance boundaries. It best explains how an
operator investigating node116 could say, without creating expectation, `yes,
compare against the historical node116-sees-M reference`.

Risk: operator acceptance must be scoped and caveated so it does not silently
become policy, requirement, command, or truth.

### Model C: Policy / Requirement Acceptance

```text
candidate baseline + policy or requirement -> accepted baseline
```

Repository-compatible when a policy or requirement actually names the acceptance
rule or reference condition. This model is stronger than Model B because it ties
acceptance to existing governance authority. It may be appropriate for regulated
or repeatable contexts, but the repository does not currently show a general
policy/requirement shape for operational mount baselines.

For node116, this model would need a rule such as `use the last accepted
storage-visibility reference for ingestion nodes` or `node116 must see M while S
is active`.

### Model D: Accepted Baseline Equals Expectation

```text
accepted baseline == expectation
```

Repository evidence mostly contradicts this model. It would collapse comparison
reference into should-bearing stance and would bypass established boundaries:
history does not authorize expectation, recommendation is not decision, decision
is not command, verification is not selection, and lens/view presentation is not
new authority.

Model D could be valid only in a specifically scoped future design where the
acceptance act explicitly says it is normative and names the authority that
permits that meaning. It is not supported as the default interpretation.

### Model E: No Baseline Acceptance Concept

Baselines remain advisory comparisons only; no acceptance layer exists.

Repository-compatible as a conservative outcome. It avoids inventing an
unimplemented concept. Its weakness is that it leaves no explicit way to record
that a candidate comparison reference has been selected for a scope. Consumers
would either keep treating all baselines as advisory candidates or drift toward
implicit acceptance.

For node116, this model can still support investigation, but the operator's
chosen comparison reference may not be preserved as a distinct authority event.

## Boundary preservation analysis

### Required question 9: Which candidate model best preserves authority boundaries?

Repository evidence does not clearly select a winning model. Boundary
preservation ranks the models by risk, not by implementation recommendation:

- Model A and Model E are safest against unauthorized expectation, because they
  avoid acceptance semantics.
- Model B preserves a useful middle boundary if operator acceptance is explicitly
  non-normative and scoped to comparison.
- Model C preserves boundaries when a policy or requirement explicitly supplies
  acceptance authority.
- Model D is unsafe as a default because it collapses accepted baseline into
  expectation.

The most important boundary is:

```text
accepted comparison reference
    !=
should-bearing expectation
```

unless the accepting authority explicitly says otherwise.

## Recommended next investigation

No implementation is recommended here. The next investigation should determine
whether repository architecture needs a preserved record for:

```text
accepted comparison reference for a scoped investigation
```

without introducing ontology or expectation semantics. Questions to investigate:

1. Is baseline acceptance a decision subtype, approval subtype, operator note,
   policy result, requirement result, or separate non-authoritative annotation?
2. What minimum provenance is required to prevent accepted baselines from being
   mistaken for requirements?
3. How should expiration, staleness, supersession, and review work for accepted
   comparison references?
4. Can lens/view surfaces present candidate and accepted references while
   preserving caveats?
5. What evidence sufficiency is needed before a candidate baseline is eligible
   for acceptance?
6. How should concern language distinguish candidate-baseline deviation,
   accepted-baseline deviation, and expectation violation?

## Non-conclusions

This audit does not conclude that:

- an accepted baseline concept must be implemented;
- expectations should be implemented;
- baselines should become topology monitoring;
- HomeOps or SeedOps surfaces should be created;
- node116 should see mount M;
- historical visibility is authoritative desired state;
- baseline acceptance is currently implemented;
- accepted baseline equals expectation;
- any candidate model is the winning model.

The strongest finding is narrower: accepted baseline is a meaningful candidate
architectural boundary **if** it means an authority-selected comparison reference
and not a should-bearing expectation.
