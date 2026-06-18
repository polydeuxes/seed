---
status: reconciliation
scope: observation, visibility, continuity, baseline, expectation, and concern architectural reconciliation
created: 2026-06-17
---

# Observation / Visibility / Continuity / Baseline / Expectation / Concern Reconciliation

## Status

Investigation only. This document does not implement baselines, expectations,
concerns, alerts, HomeOps, SeedOps, topology monitoring, ontology, runtime
behavior, projection changes, view changes, or operator surfaces.

This reconciliation treats the required input documents as repository
investigation authority and builds on their findings rather than rediscovering
them. No inspected evidence contradicts their central boundary findings.

Short answer: the repository supports a boundary-preserving progression from
observed reality toward operator-significant concern, but it does not support an
automatic progression from history to normative expectation.

The reconciled model is:

```text
Observation
    -> Visibility
    -> Continuity
    -> Candidate Baseline
    ? authority selection
    -> Accepted Baseline
    ? should-bearing authority
    -> Expectation
```

Concern may emerge at several points in or beside that chain. It does not have
to wait for expectation. A visibility change, continuity break, baseline
deviation, accepted-reference deviation, expectation violation, ambiguity,
staleness, degraded evidence quality, or operator investigation context can all
be concern-producing without collapsing into the same concept.

## Purpose

The purpose of this reconciliation is to explain how the incrementally
discovered concepts relate:

```text
observation
visibility
continuity
candidate baseline
accepted baseline
expectation
concern
```

It answers the audit question:

```text
What is the complete progression
from observed reality
to operator-significant concern?
```

It also classifies concepts as:

- descriptive;
- interpretive;
- authority-bearing;
- normative.

The required operational example used throughout is:

```text
example_host_b historically observes mount M
example_host_b stops observing mount M
ingestion becomes uneven
operator investigates
```

## Prior findings reconciled

Required inputs reconciled:

- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/expectation_continuity_concern_design_space_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/baseline_continuity_expectation_audit.md`
- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/lens_view_reconciliation.md`

The prior findings are mutually compatible:

1. Observation and visibility are evidence-facing concepts. They answer what was
   observed and what is currently visible.
2. Visibility is distinct from ownership, target identity, expectation, and
   concern.
3. Continuity is stronger than isolated observation because it recognizes
   persistence, recurrence, survival, or remaining visible across observations;
   it is still not a should-claim.
4. A candidate baseline is stronger than raw continuity because it frames a
   historical or observed condition as a possible comparison reference for a
   question.
5. An accepted baseline, if later recognized by repository architecture, would
   require authority selection and would mean only that a reference has been
   selected for a scoped purpose.
6. Expectation requires should-bearing or anticipation-bearing authority. History
   alone can support candidate expectations or candidate baselines, but it cannot
   authorize `should continue` by itself.
7. Concern can exist without expectation. Ambiguity, changed visibility,
   degraded evidence quality, stale support, investigation pressure, and
   baseline deviation can matter to an operator before any normative expectation
   exists.
8. Lens/view language can explain bounded interpretation over projected State,
   but it does not create new State authority, truth authority, policy authority,
   expectation authority, or execution authority.

## Files inspected

Required reconciliation inputs:

- `docs/visibility_target_ownership_concern_reconciliation.md`
- `docs/expectation_continuity_concern_design_space_audit.md`
- `docs/should_authority_expectation_audit.md`
- `docs/baseline_continuity_expectation_audit.md`
- `docs/candidate_baseline_accepted_baseline_expectation_audit.md`
- `docs/lens_view_reconciliation.md`

Additional repository evidence inspected directly or via prior reconciled
findings:

- `docs/continuity_frontier.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/storage_topology_ambiguity_and_operator_clarification_reconciliation.md`
- `docs/storage_measurement_current_fact_regression_audit.md`
- `docs/availability_vocabulary_audit.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/prediction_forecasting_and_future_claims_reconciliation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/state_summary_authority_reconciliation.md`
- `seed_runtime/state.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/policy.py`
- `seed_runtime/facts.py`

## Concept inventory

| Concept | Existing repository status | Classification | Authority shape |
| --- | --- | --- | --- |
| Observation | Existing evidence concept | Descriptive / pure evidence | Source and event provenance authority |
| Visibility | Existing evidence/read-projection concept | Descriptive, with scoped interpretation when grouped | Observation/projection authority |
| Continuity | Existing architectural frontier, not general topology implementation | Interpretive over evidence | Historical evidence authority, not normative authority |
| Candidate baseline | Investigational concept supported by prior audits | Interpretive over evidence | Candidate framing; no acceptance authority |
| Accepted baseline | Investigational, not current general topology concept | Authority-bearing comparison reference | Requires authority selection for scope and purpose |
| Expectation | Partially existing only in scoped should-like forms; no general topology expectation | Normative / should-bearing | Requires named should-bearing or anticipation-bearing authority |
| Concern | Investigational/operator-significance concept; concern-like pressures exist | Interpretive and operator-significant; may be authority-adjacent | Requires scoped significance, not necessarily should authority |

## Concept definitions

### Observation

Observation answers:

```text
What was observed?
```

Observation is pure evidence. In the example_host_b example, observation includes
records that example_host_b or a example_host_b-scoped endpoint reported filesystem evidence
for mount M at particular times, and later records that do not include that
visible mount.

Observation does not say:

```text
example_host_b owns M
example_host_b should see M
M is operationally required
missing M is an alert
```

### Visibility

Visibility answers:

```text
What is currently visible?
```

Visibility is descriptive when it reports current observed presence or absence.
It can become lightly interpretive when read projections group visible endpoints,
mount paths, or dimensions to answer a bounded question, but the authority still
comes from observation and projection evidence.

For example_host_b:

```text
historical visibility: example_host_b saw mount M
current visibility: example_host_b no longer sees mount M
```

Visibility does not require ownership. The same mount-like evidence may be
visible through one endpoint, absent from another endpoint, ambiguous across
subjects, or grouped as a candidate without any claim about who owns the storage.

### Continuity

Continuity answers:

```text
What has persisted,
recurred,
or remained visible?
```

Continuity is interpretation over evidence. It recognizes that a pattern has
survived across time or repeated observations. It is stronger than a single
observation and weaker than a baseline or expectation.

For example_host_b:

```text
example_host_b historically observed mount M repeatedly or over an extended interval
```

Continuity does not say:

```text
therefore example_host_b should keep seeing M
therefore loss of M is a violation
therefore M is the accepted comparison reference
```

### Candidate Baseline

Candidate baseline answers:

```text
What historical condition
appears useful as a comparison reference?
```

A candidate baseline is interpretation over evidence. It takes continuity or
historical evidence and frames it as potentially useful for comparison in a
bounded question.

For example_host_b:

```text
historical example_host_b-sees-M appears useful as the reference condition
when investigating the current disappearance of M
```

Candidate baseline is not pure evidence because it includes selection and
purpose. It is not authority-bearing in the accepted-reference sense because no
recognized authority has selected it as the reference. It is not normative
because it does not say the condition should continue.

### Accepted Baseline

Accepted baseline answers:

```text
What comparison reference
has been selected for a scoped purpose?
```

Accepted baseline is authority-bearing, but not necessarily normative. It means
an authority has selected a comparison reference for a named scope, purpose,
view, assessment, or investigation.

For example_host_b:

```text
for this investigation, compare current example_host_b mount visibility
against the historical example_host_b-sees-M reference
```

That statement selects a comparison reference. It still does not necessarily say:

```text
example_host_b should see M
```

The accepted baseline boundary is important because comparison authority and
should authority are separable.

### Expectation

Expectation answers:

```text
What condition
should continue,
hold,
or be anticipated?
```

Expectation is normative or should-bearing when it says a condition should hold
or continue. Repository evidence supports scoped should-like authority in policy,
goals, requirements, approvals, decisions, validation expectations, refresh
recommendations, and capability verification boundaries, but it does not contain
a general operational topology expectation that can currently say:

```text
example_host_b should see mount M
```

For example_host_b, expectation would require a named authority path, such as an
operator-owned declared expectation, requirement, policy, accepted design
invariant, or other explicit authority record that connects example_host_b and M.

### Concern

Concern answers:

```text
What deviation,
ambiguity,
risk,
or change
is significant to an operator?
```

Concern is operator-significant interpretation. It may arise from evidence,
continuity, baseline comparison, expectation violation, ambiguity, degraded
knowledge quality, or operational context such as uneven ingestion.

For example_host_b:

```text
example_host_b stopped seeing M
historical continuity made that disappearance notable
ingestion became uneven
operator investigation made the change significant
```

Concern does not automatically imply expectation. It can exist as pressure to
investigate without asserting that any rule was violated.

## Authority boundaries

### Evidence boundary

Observation and basic visibility remain on the evidence side of the boundary.
They carry source, time, subject, predicate, dimensions, and projection support.
They do not create ownership, topology truth, expectation, alerting, or policy.

### Interpretation boundary

Continuity, candidate baseline, and concern involve interpretation over evidence.
They select, compare, compress, or classify evidence for a question. This is the
same kind of boundary-preserving role described by lens/view reconciliation:
bounded interpretation can shape attention without creating new State authority
or operational truth.

### Selection authority boundary

Accepted baseline requires authority selection. The selected reference may be
operator-selected, decision-selected, policy-selected, requirement-selected, or
workflow-selected, but the authority must be named and scoped.

Crossing this boundary changes:

```text
this seems like a useful comparison reference
```

into:

```text
use this comparison reference for this scoped purpose
```

It does not by itself create a should-claim.

### Should-bearing authority boundary

Expectation requires should-bearing authority. Crossing this boundary changes:

```text
compare against historical example_host_b-sees-M
```

into something like:

```text
example_host_b should see M while condition C holds
```

Repository evidence requires this authority to be explicit and scoped. History,
visibility, continuity, and accepted comparison references do not automatically
supply it.

### Operator-significance boundary

Concern requires operator significance, not necessarily should authority. It can
be triggered by a change, ambiguity, unexplained deviation, stale knowledge,
ingestion unevenness, or an investigation context.

This boundary changes:

```text
there is a difference in evidence
```

into:

```text
this difference matters to an operator or investigation
```

## Example host operational example

### Observation

Historical observations report that example_host_b observed mount M. Later observations
or current projected evidence no longer show example_host_b observing mount M.

Evidence-level statement:

```text
example_host_b observed M before; current evidence does not show example_host_b observing M
```

### Visibility

Visibility describes current seen/not-seen status.

```text
M was visible from example_host_b historically
M is not currently visible from example_host_b
```

This remains compatible with other possibilities:

```text
M may still be visible elsewhere
M may be invisible because the mount disappeared
M may be invisible because observation failed
M may have moved, changed dimensions, or become ambiguous
```

Visibility alone does not choose among those explanations.

### Continuity

Continuity interprets historical evidence:

```text
example_host_b-sees-M persisted or recurred enough to be recognized as a historical
pattern
```

This makes the current disappearance more notable than a one-off absent sample,
but it still does not say the pattern should continue.

### Candidate Baseline

Candidate baseline frames the historical pattern as a possible comparison
reference:

```text
historical example_host_b-sees-M may be a useful baseline candidate for investigating
current example_host_b-not-seeing-M
```

This is appropriate when the operator investigates uneven ingestion because the
historical visibility pattern may help explain what changed.

### Accepted Baseline

Accepted baseline would require selection:

```text
for this ingestion unevenness investigation, use historical example_host_b-sees-M as the
comparison reference
```

That acceptance supports structured comparison, but it still does not assert
that example_host_b is required to see M.

### Expectation

Expectation would require an additional authority path:

```text
example_host_b should see M
```

Such a statement could be valid only if backed by a declared expectation,
requirement, policy, operator-owned intent, design invariant, or similar
should-bearing authority. Historical observation alone is insufficient.

### Concern

Concern emerges because the operator-significant situation combines several
signals:

```text
current visibility changed
historical continuity made the change notable
a candidate or accepted comparison reference may frame the deviation
ingestion became uneven
operator investigation makes the deviation operationally significant
```

If a valid expectation also exists, concern may sharpen into expectation
violation. Without expectation, concern can still exist as significant ambiguity
or unexplained operational change.

## Progression analysis

### Required question 1: Which concepts are pure evidence?

Pure evidence:

```text
observation
basic visibility
```

Observation is the clearest pure evidence concept. Basic visibility is evidence
when it reports what is currently visible from observed facts or projected
current support.

Caveat: visibility can be displayed through read projections that group or
summarize evidence. The grouped view is presentation/interpretation over evidence,
but the underlying visibility claim remains descriptive.

### Required question 2: Which concepts are interpretations over evidence?

Interpretations over evidence:

```text
continuity
candidate baseline
concern
lens-like visibility groupings or ambiguity summaries
```

Continuity interprets persistence or recurrence. Candidate baseline interprets a
historical condition as a possible comparison reference. Concern interprets a
difference, ambiguity, or risk as operator-significant.

### Required question 3: Which concepts require authority?

Authority-requiring concepts:

```text
accepted baseline
expectation
some forms of concern when recorded as operator-owned priority, decision, or
workflow status
```

Accepted baseline requires authority to select a comparison reference for a
scope. Expectation requires authority to say a condition should hold, continue,
or be anticipated. Concern can be observed as an interpretive pressure, but if it
is promoted to an operator-owned decision, priority, ticket, alert, or workflow
state, that promotion would require the relevant authority.

### Required question 4: Which concepts require should-bearing authority?

Should-bearing authority is required for:

```text
expectation
normative concern labels that assert violation or required remediation
```

Accepted baseline does not necessarily require should-bearing authority because
it can be only comparison-reference authority. Candidate baseline and continuity
do not require should-bearing authority.

### Required question 5: Can concern exist without expectation?

Yes.

Prior audits consistently support this answer. Concern can arise from visibility
change, continuity break, ambiguity, stale support, degraded evidence quality,
operator investigation pressure, or ingestion unevenness without any claim that a
condition should have held.

For example_host_b:

```text
example_host_b stopped seeing M and ingestion became uneven
```

is enough to create an operator-significant concern for investigation. It is not
enough to assert:

```text
example_host_b violated an expectation by not seeing M
```

### Required question 6: Can expectation exist without an accepted baseline?

Yes, if another should-bearing authority directly declares the expectation.

Examples of possible authority shapes:

```text
operator declares example_host_b should see M
policy requires example_host_b to see M under condition C
requirement states service S depends on example_host_b seeing M
accepted design invariant says M must be mounted on example_host_b
```

In those cases, an expectation can exist without first accepting a historical
baseline. The expectation authority comes from declaration, policy, requirement,
or invariant rather than baseline acceptance.

### Required question 7: Can an accepted baseline exist without expectation?

Yes.

An accepted baseline can select a comparison reference for investigation,
assessment, or view construction without saying the reference should continue.

For example_host_b:

```text
compare current visibility against historical example_host_b-sees-M
```

can be accepted for an investigation even if the operator has not asserted that
example_host_b must or should see M.

### Required question 8: Can candidate baselines emerge from history?

Yes, as candidates.

Historical observation and continuity can support candidate baselines:

```text
example_host_b historically saw M
therefore example_host_b-sees-M may be a useful comparison reference
```

The candidate must remain caveated. History can make a reference plausible; it
cannot by itself accept the reference for a scope or make the reference
normative.

### Required question 9: Does repository evidence support the progression?

The repository evidence supports the progression as an architectural model with
two authority gates:

```text
Observation
    -> Visibility
    -> Continuity
    -> Candidate Baseline
    ? authority selection
    -> Accepted Baseline
    ? should-bearing authority
    -> Expectation
```

The first three arrows are evidence-to-interpretation movement. The candidate
baseline step is an interpretive framing step. The accepted baseline step
requires authority selection. The expectation step requires should-bearing
authority.

The repository does not support removing either question mark. In particular,
repository evidence does not support:

```text
Continuity automatically becomes expectation
Candidate baseline automatically becomes accepted baseline
Accepted baseline automatically becomes expectation
Concern automatically means violation
```

### Required question 10: Where does concern emerge?

Concern can emerge at multiple points:

| Possible emergence point | Supported? | Boundary-preserving interpretation |
| --- | --- | --- |
| Visibility change | Yes | Current seen/not-seen changed; may warrant attention. |
| Continuity break | Yes | A previously persistent pattern stopped; notable without should. |
| Candidate baseline deviation | Yes | Current state differs from a plausible comparison reference. |
| Accepted baseline deviation | Yes | Current state differs from an authority-selected comparison reference. |
| Expectation violation | Yes | Current state conflicts with a should-bearing expectation. |
| Other | Yes | Ambiguity, stale evidence, degraded support, uneven ingestion, or operator investigation context may create concern. |

The strongest concern in the example_host_b example is not a single concept. It is a
compound operator-significant situation:

```text
visibility loss
+ historical continuity
+ possible or accepted comparison reference
+ uneven ingestion
+ operator investigation
```

If an expectation exists, the concern can additionally be described as an
expectation violation. If no expectation exists, it remains a concern because the
change is significant and ambiguous.

## Boundary preservation analysis

### Observation must not collapse into visibility

Observation records what was observed. Visibility is the current or scoped
readout of what is seen. Historical observations can exist even when current
visibility is absent.

### Visibility must not collapse into ownership

The example_host_b example can be investigated without asserting who owns mount M or
which host controls the underlying storage.

### Continuity must not collapse into expectation

Repeated historical visibility can make disappearance notable, but it cannot say
`should continue` without authority.

### Candidate baseline must not collapse into accepted baseline

A plausible comparison reference is not the same as an authority-selected
reference. Candidate status must remain visible.

### Accepted baseline must not collapse into expectation

A selected comparison reference is not automatically a normative requirement.
Comparison authority and should authority are distinct.

### Concern must not collapse into alerting or remediation

Concern explains operator significance. It does not implement alerts, choose
HomeOps or SeedOps behavior, authorize remediation, or require topology
monitoring.

### Lens/view interpretation must not create new authority

Lens-like interpretation can explain why a bounded question selects certain
facts, baselines, deviations, or concerns. It cannot create State authority,
truth authority, policy authority, or execution authority.

## Remaining open questions

1. Whether the repository should later introduce a first-class baseline concept
   is unresolved by this investigation.
2. Whether accepted baselines should be stored, derived, declared, or represented
   only in documents remains unresolved.
3. Which authority sources, if any, should be able to accept baselines remains
   unresolved.
4. Which authority sources, if any, should be able to create operational topology
   expectations remains unresolved.
5. How long-term observation history should be queried for continuity evidence
   remains unresolved, especially where projected State preserves current samples
   rather than a general continuity model.
6. Whether concern should remain an architectural vocabulary or become a
   first-class recorded concept remains unresolved.
7. How ingestion unevenness should be causally related to mount visibility loss
   remains unresolved; this reconciliation treats the relationship as an
   investigation context, not a proven cause.

## Conclusion

The repository-authoritative reconciliation is:

```text
observed reality
    becomes observation evidence;
observation evidence
    supports current visibility;
visibility over time
    supports continuity interpretation;
continuity and history
    can support candidate baselines;
candidate baselines
    require authority selection to become accepted baselines;
accepted baselines
    require should-bearing authority to become expectations;
concern
    may emerge from changes, breaks, deviations, ambiguity, degraded evidence,
    uneven ingestion, or expectation violations, depending on which authority
    boundaries have been crossed.
```

For the example_host_b example, the repository can safely say that historical
example_host_b-sees-M evidence and current example_host_b-not-seeing-M evidence create a
visibility change and possible continuity break. That history can support a
candidate baseline. An accepted baseline would require scoped authority
selection. A `example_host_b should see M` expectation would require additional
should-bearing authority. Operator-significant concern can exist before that
expectation if the visibility loss, continuity break, ingestion unevenness, or
ambiguity matters to the operator's investigation.

This preserves the required boundaries among evidence, interpretation,
authority, expectation, and concern without implementing any new mechanism.
