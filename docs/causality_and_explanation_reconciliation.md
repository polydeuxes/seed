# Causality And Explanation Reconciliation

## Purpose

This document performs a documentation-only reconciliation of causality,
explanation, events, consequences, relationships, recommendations, and
historical reasoning.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify observations, facts,
relationships, projections, assessments, recommendations, decisions, commands,
actions, event systems, timeline systems, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established that events describe occurrences, changes
describe transitions, claims describe propositions, consequences describe
outcomes, recommendations derive relevance through consequences, and history
survives state change. A remaining architectural question is:

```text
What caused something?
```

Examples include:

```text
service became unavailable
filesystem detached
package removed
backup failed
host rebooted
```

The question is not merely whether one event appeared before another. Seed may
know that a filesystem detached before a service became unavailable without yet
knowing that the detachment caused the outage. Seed may know that a backup
failed and that data-loss risk increased without yet knowing whether the backup
failure was caused by storage, credentials, network partition, operator action,
or scheduler misconfiguration.

The architectural risk is over-collapse: treating sequence as cause, treating
correlation as explanation, treating consequences as causal facts, treating
ordinary relationships as causal proof, or treating recommendations as if they
prove their motivating hypotheses.

## Central Finding

The safest architectural answer is:

```text
Causality is a supported claim or hypothesis that one condition, event, change,
state, relationship, action, or mechanism contributed to producing another
condition, event, change, state, or outcome.
```

More compactly:

```text
Events describe occurrences.
Changes describe transitions.
Consequences describe outcomes.
Relationships connect entities or knowledge objects.
Explanations connect knowledge into an answer.
Causal claims assert productive contribution and require support.
```

Therefore:

```text
causality
  ≠ sequence alone
  ≠ correlation alone
  ≠ consequence by itself
  ≠ ordinary relationship by itself
  ≠ recommendation relevance by itself
  ≠ explanation text by itself
```

Seed may reason about causes, but it should preserve the modal and evidentiary
status of that reasoning. A cause may be known, likely, possible, hypothesized,
operator-provided, contradicted, superseded, or unknown. Unknown cause is a
valid and important state.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/event_and_change_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/goal_relevance_and_recommendation_generation_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/explainability_contract_characterization.md`
- `docs/explainability_audit.md`
- `docs/why_not_explanation_characterization.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`

## Boundary Summary

| Concept | Primary role | Answers | Must not become |
| --- | --- | --- | --- |
| Event | Occurrence in a temporal and contextual scope | What happened? | Cause, consequence, current state, recommendation |
| Change | Transition between distinguishable states or values | What became different? | Event identity, contradiction, causal proof |
| Consequence | Outcome, impact, or risk arising from a condition or occurrence | What did, could, or may result? | Cause, goal, recommendation, proof of mechanism |
| Relationship | Normalized edge between entities, artifacts, concepts, or claims | What is connected to what? | Causal proof, ownership, behavior, explanation |
| Explanation | Read-oriented answer that connects support, claims, relationships, temporal context, and interpretation | Why is this answer being presented? | Preserved truth by itself, causal fact by itself, action authority |
| Causal claim | Supported or hypothesized assertion of productive contribution | What produced or contributed to what, with what support? | Sequence, correlation, consequence, recommendation |
| Assessment | Evidence-backed interpretation of a condition | What does the knowledge indicate? | Cause, decision, command, action |
| Recommendation | Advisory relevance path from condition/consequence to goal | What should be considered and why does it matter? | Causal proof, decision, approval, command |
| History | Preserved occurrence and temporal knowledge | What happened or was known over time? | Causal understanding by itself |

## 1. What Is Causality?

Causality is the concept of productive contribution: one thing helped bring
about, enable, trigger, prevent, worsen, mitigate, or otherwise materially shape
another thing.

Architecturally, a causal assertion is best understood as a claim with a
special semantic burden:

```text
Causal claim: X caused, contributed to, enabled, prevented, aggravated, or
mitigated Y within scope S, under support E, with uncertainty U.
```

It may connect many kinds of objects:

```text
Event -> Event
Event -> Consequence
State -> Event
State -> Consequence
Change -> State
Relationship -> Consequence
Action -> Change
Mechanism -> Outcome
Absence of expected condition -> Failure
```

Examples:

```text
filesystem detachment caused service unavailability
expired credentials contributed to backup failure
host reboot caused process restart
missing mount prevented backup destination writes
configuration change triggered service reload failure
```

A causal claim is not merely an ordinary relationship. It asserts more than an
edge. It asserts that the source side had productive relevance to the target
side. That assertion requires support appropriate to its strength.

A causal claim is also not merely an assessment, although an assessment may
include or depend on causal reasoning. For example, `storage unavailable` may be
an assessment; `storage unavailable because filesystem detached` is an
explanatory causal interpretation; `filesystem detachment caused the outage` is
a causal claim.

The important architectural consequence is that causality should be represented
or described with its warrant, not smuggled into neutral event order,
relationship names, or recommendation prose.

### Causality as claim, relationship, explanation, or assessment

Causality can appear through several architectural surfaces, but it should not
be identified exclusively with any one of them:

- **As a claim:** the assertion that X caused Y is a proposition requiring
  support.
- **As a relationship:** a causal claim may be normalized as an edge-shaped
  claim such as `caused`, `contributed_to`, or `enabled`, but this edge remains
  evidence-backed and uncertainty-bearing.
- **As an explanation:** an explanation may cite a causal claim or causal
  hypothesis to answer a why question.
- **As an assessment:** an assessment may judge that a causal hypothesis is
  likely, possible, unsupported, contradicted, or unknown.

The conceptual anchor should be:

```text
Causality is productive contribution.
Causal claim is the asserted proposition about that contribution.
Causal relationship is one possible representation of the claim.
Causal explanation is one possible use of the claim in an answer.
Causal assessment is one possible evaluation of the claim's support.
```

## 2. What Is an Explanation?

An explanation is a read-oriented interpretive answer that connects preserved
knowledge to a question.

It answers:

```text
Why is this claim, state, relationship, recommendation, absence, selection, or
interpretation being presented this way?
```

Examples:

```text
service unavailable because filesystem detached
backup failed because storage unavailable
package absent because it was removed at T
capability unverified because no current capability_verified fact is present
recommendation relevant because failed backup increases recoverability risk
```

An explanation may include:

```text
subject
question or claim being explained
supporting observations, evidence, facts, and relationships
relevant events and temporal ordering
selection or projection rules
competing or conflicting support
causal claims or causal hypotheses
consequences and goal relevance
uncertainty, caveats, and missing evidence
```

An explanation is not necessarily a causal fact. Some explanations are
support explanations:

```text
Seed believes X because source S reported X at T.
```

Some are selection explanations:

```text
This value is current because it is the latest non-expired support.
```

Some are absence explanations:

```text
No current belief is shown because no matching support exists in the selected
scope.
```

Some are recommendation explanations:

```text
Investigate backups because the failed backup may threaten the recovery point
objective.
```

Some are causal explanations:

```text
The service became unavailable because the filesystem it depends on detached.
```

Thus, explanations are interpretations or read models over preserved knowledge,
not new runtime truth by themselves. They can cite projections, relationships,
claims, events, consequences, and causal hypotheses, but the explanation text
should not silently upgrade any cited item into a proven cause.

### Are explanations projections, relationships, causal claims, interpretations, or something else?

An explanation is best treated conceptually as an interpretation assembled for a
question. It may be implemented by or exposed through a projection-like read
surface, but the explanation itself is not the projection's authority. It may
cite relationships, but it is not the relationship. It may contain causal
claims, but it is not automatically a causal fact. It may summarize an
assessment, but it should preserve the assessment's support and uncertainty.

The safest boundary is:

```text
Explanation = question-relative knowledge connection.
Causal claim = supported assertion of productive contribution.
Projection = selected read view over preserved knowledge.
Relationship = normalized edge.
Assessment = interpreted condition or confidence judgment.
```

## 3. Relationship Between Events And Causality

Events describe occurrences. Causality connects occurrences, states, changes,
conditions, actions, mechanisms, or outcomes through productive contribution.

Example:

```text
Event A: filesystem detached at T1
Event B: service became unavailable at T2
```

The sequence `T1 before T2` may be relevant evidence, but it is not sufficient
for causality.

### Does sequence imply causality?

No.

Sequence only establishes ordering within the precision and reliability of the
timestamps. It can support candidate generation:

```text
filesystem detached before service unavailable
therefore detachment is a possible cause to investigate
```

It does not by itself support:

```text
filesystem detachment caused service unavailability
```

A later event may have an unrelated cause, a shared upstream cause, a coincident
cause, or no known connection to the earlier event.

### Does timing imply causality?

No.

Timing can strengthen or weaken a hypothesis, but timing alone remains
insufficient. Close temporal proximity may make a hypothesis plausible. Wide
separation may make it less plausible. Neither proves nor disproves causality
without domain context and support.

Examples:

```text
host rebooted at 10:00
backup failed at 10:01
```

This timing may justify a hypothesis that reboot disrupted the backup. It may
also be coincidental if the backup failed because of expired credentials or an
unavailable remote endpoint.

### What evidence is required?

Causal support should be proportionate to claim strength. Useful support may
include:

- temporal ordering with adequate timestamp precision;
- domain mechanism showing how X could produce Y;
- dependency or topology relationships connecting affected entities;
- observations of intermediate states or failure modes;
- logs, traces, metrics, or audit records linking X to Y;
- absence of stronger competing causes within the relevant scope;
- recurrence evidence showing repeated X/Y pairing under similar conditions;
- operator or system reports explicitly attributing cause;
- successful intervention evidence, such as restoring X resolving Y; and
- counterfactual evidence, such as Y not occurring when X is absent under
  otherwise similar conditions.

Not every causal claim requires every form of evidence. However, strong causal
language should require more than event order. Weak causal language may be
appropriate when support is partial:

```text
possible cause
candidate cause
likely contributor
reported cause
known cause
unknown cause
```

## 4. Relationship Between Causality And Relationships

Relationships normalize edges between entities, artifacts, concepts, or claims.
Relationship promotion preserves an evidence-backed edge; it does not prove
truth, behavior, ownership, or authority by itself.

Ordinary relationships include:

```text
depends_on
connected_to
monitored_by
runs_on
listens_on
imports
owned_by
```

These relationships may be causally relevant, but they are not causal claims by
default.

Example:

```text
Relationship: service depends_on filesystem
Event: filesystem detached
Event: service became unavailable
```

The `depends_on` relationship supplies a plausible mechanism. It helps explain
why filesystem detachment could affect service availability. But the dependency
relationship alone does not prove that the detachment caused this specific
outage. Additional support is needed, such as service errors referencing the
mount, health checks failing immediately after detachment, or recovery after
reattachment.

A causal relationship differs from an ordinary relationship because it asserts
productive contribution in a scoped occurrence or outcome:

```text
Ordinary relationship: service depends_on filesystem
Causal claim: filesystem detachment caused service outage during incident I
```

The first can be durable structural knowledge. The second is usually temporal,
incident-scoped, evidence-sensitive, and uncertainty-bearing.

Causal relationships should therefore carry or reference:

```text
cause candidate or source
caused or affected target
causal verb or contribution type
scope, incident, interval, or context
supporting evidence
mechanism or dependency path when available
confidence or modal status
competing hypotheses or caveats when relevant
```

## 5. Relationship Between Causality And Consequences

Consequences describe outcomes, impacts, or risks that did, could, or may result
from a condition or occurrence.

Examples:

```text
Event: filesystem detached
Consequence: service unavailable

Event: backup failed
Consequence: elevated data-loss risk

State: disk full
Consequence: writes may fail
```

Consequences are causally adjacent, but they are not automatically causal
claims. The consequence says what outcome matters or may follow. The causal
claim says what produced or contributed to that outcome.

A consequence may be:

- **observed:** service unavailable was observed after detachment;
- **inferred:** service unavailability likely resulted from detachment;
- **projected:** continued detachment may prevent recovery;
- **hypothetical:** if detachment recurs, the service may fail again; or
- **risk-oriented:** failed backup increases exposure until a successful backup
  is confirmed.

Only some consequence statements are causal. For example:

```text
Consequence: data-loss risk is elevated after backup failure.
```

This is an outcome/risk statement. It does not necessarily assert the cause of
the backup failure. It may rely on a known consequence model: lack of recent
backup increases recovery risk. That model is explanatory, but it should not be
confused with a root-cause claim about why the backup failed.

Consequences can be explanatory without being root-causal. They often explain
why an event matters:

```text
The backup failure matters because it may compromise recoverability.
```

That statement does not explain what caused the backup failure. It explains the
backup failure's relevance to a goal.

## 6. Relationship Between Causality And Recommendations

Recommendations connect assessed conditions and consequences to operator-owned
goals. Causal reasoning contributes to recommendation relevance by helping Seed
explain why a suggested investigation, mitigation, or decision may matter.

Example:

```text
Event: backup failure
Consequence: elevated data-loss risk
Goal: preserve recoverability
Recommendation: investigate backup pipeline
```

The recommendation does not require Seed to know the root cause of the backup
failure. It may be relevant because a consequence threatens a goal. However,
causal hypotheses can shape the recommendation:

```text
Hypothesis: backup failed because storage was unavailable
Recommendation: investigate storage availability and backup destination writes

Hypothesis: backup failed because credentials expired
Recommendation: inspect backup credentials and renewal path

Unknown cause: backup failed, cause unknown
Recommendation: investigate backup pipeline with priority on recent errors and
infrastructure dependencies
```

Recommendation relevance should preserve the distinction between:

```text
why the condition matters
what may have caused the condition
what should be investigated or considered
who may decide or act
what commands, if any, are authorized
```

A causal hypothesis may justify an investigation recommendation even when it is
not established enough to justify a definitive remediation recommendation.

Examples:

```text
Safe: storage detachment is a possible cause; investigate mount and service logs.
Unsafe overstatement: storage detachment caused the outage; remounting storage
will resolve the incident.
```

The second statement requires stronger support because it asserts cause and
predicts remedy.

## 7. Evidence Required For Causal Claims

Seed should distinguish at least four causal-support categories.

### Observed causality

Observed causality exists when support directly records or demonstrates the
causal connection, not just the endpoints.

Examples:

```text
trace shows request failure caused by connection refused to dependency
service log reports startup failed because required mount /data is missing
backup tool reports failure reason: destination filesystem unavailable
reattachment followed by successful health check confirms observed recovery path
```

Even observed causality may remain source-scoped. A tool-reported reason is
strong evidence, but it still has source provenance and may be contradicted.

### Inferred causality

Inferred causality exists when Seed combines evidence, domain rules,
relationships, timing, and observations to conclude that a cause is likely.

Example:

```text
filesystem detached before outage
service depends_on that filesystem
service errors reference missing path
service recovered after filesystem reattached
```

This can support a likely-cause assessment, especially if competing hypotheses
are weaker. It should still preserve the inference path.

### Hypothesized causality

Hypothesized causality exists when there is enough plausibility to investigate
but insufficient support to assert likely or known cause.

Example:

```text
host reboot occurred shortly before backup failure
backup failure logs are missing
backup process may have been interrupted by reboot
```

A hypothesis is useful. It should be labeled as such.

### Operator-provided causality

Operator-provided causality exists when an operator asserts or records a causal
interpretation.

Example:

```text
operator note: outage caused by storage array maintenance
incident report: root cause was expired certificate
```

Operator-provided cause is evidence with source authority characteristics. It
may be high value, but Seed should not treat it as automatically verified unless
the relevant authority and verification boundaries support that interpretation.
It should remain attributable:

```text
reported by operator O
recorded in incident report R
accepted by authority A if applicable
contradicted or corroborated by evidence E if available
```

### Evidence strength and claim language

Causal language should match support:

| Support state | Preferred language | Avoid |
| --- | --- | --- |
| Direct source or intervention evidence with corroboration | known cause, established cause | pretending no uncertainty exists |
| Strong inference with mechanism and supporting observations | likely cause, likely contributor | proven cause |
| Plausible but incomplete support | possible cause, candidate cause, hypothesis | caused |
| Operator report without independent verification | operator-reported cause, incident-reported cause | verified cause |
| Temporal ordering only | occurred before, preceded, candidate for investigation | caused |
| Correlation only | correlated with, co-occurred with | caused |
| No support | cause unknown | speculation as fact |

## 8. What Should Not Be Collapsed Together?

The following objects are distinct:

```text
Event:        service stopped
Relationship: service depends_on storage
Consequence: service unavailable
Explanation: service unavailable because storage detached
Causal Claim: storage detachment caused outage
```

They answer different questions:

| Object | Question answered |
| --- | --- |
| Event | What happened? |
| Relationship | What is connected to what? |
| Consequence | What outcome or risk followed or may follow? |
| Explanation | How is Seed connecting knowledge to answer the question? |
| Causal claim | What produced or contributed to what? |

Collapsing them causes architectural errors:

- treating a dependency as proof of an outage cause;
- treating an outage as proof that the dependency failed;
- treating an event's consequence as the event's root cause;
- treating explanatory prose as preserved truth;
- treating a recommendation as proof of the hypothesis it investigates;
- treating event order as a causal chain;
- treating historical co-occurrence as established mechanism;
- erasing unknown-cause states;
- overstating support and misleading operators; and
- making later contradictory evidence difficult to represent.

A safe reconciliation keeps each object separately addressable:

```text
Event E1: storage detached at T1.
Relationship R1: service depends_on storage.
Event E2: service became unavailable at T2.
Consequence C1: service outage affected availability goal.
Explanation X1: outage is explained by E1 + R1 + E2 with support S.
Causal claim K1: E1 likely caused or contributed to E2, support S, uncertainty U.
Recommendation M1: investigate storage detachment and restore stable attachment.
```

The same knowledge may participate in several objects, but participation is not
identity.

## 9. Role Of Uncertainty

Causal uncertainty is not a failure state. It is often the correct state.

Seed should communicate causal status with explicit modality:

```text
known cause
likely cause
possible cause
candidate cause
reported cause
hypothesized cause
contributing factor
correlated event
preceding event
unknown cause
```

The difference matters operationally:

```text
Known cause: act on established remediation path if authorized.
Likely cause: prioritize remediation or investigation, preserve caveats.
Possible cause: investigate; do not present as root cause.
Correlated event: note as context; do not use causal language.
Unknown cause: preserve facts and recommend investigation if relevant.
```

Seed should also communicate what is missing:

```text
No direct evidence links the reboot to the backup failure.
The storage dependency makes detachment a plausible cause, but service logs are
missing.
The operator reported a cause, but Seed has not independently corroborated it.
The events are temporally ordered, but the timestamp precision is insufficient
to establish which occurred first.
A competing hypothesis remains: credentials expired before the storage event.
```

Uncertainty should be preserved in explanations and recommendations. A concise
answer may say:

```text
The cause is unknown. Storage detachment is a possible contributor because it
preceded the outage and the service depends on that filesystem, but Seed lacks
service log evidence linking the two.
```

This is more useful and safer than either silence or unsupported certainty.

## 10. Relationship Between Causality And History

History preserves occurrences and temporal knowledge. Causality connects
occurrences or conditions through supported productive contribution.

History may exist without causal understanding:

```text
T1 filesystem detached
T2 service unavailable
T3 host rebooted
T4 backup failed
```

This timeline is valuable even if Seed does not know what caused what. It can
support audit, incident reconstruction, recurrence detection, and candidate
hypothesis generation.

Causality may connect historical objects when support justifies the connection:

```text
filesystem detached at T1 caused service unavailable at T2
host reboot at T3 interrupted backup job at T4
configuration change at T5 triggered reload failure at T6
```

The implications are:

- preserving history should not require causal conclusions;
- causal conclusions should not require deleting alternative history;
- later evidence may revise causal interpretation while leaving event history
  intact;
- a timeline is not a causal graph;
- a causal graph is not a complete history;
- event retention supports future causal analysis; and
- causal uncertainty should remain attached to the interpretation, not erased
  from the occurrences.

Example:

```text
Historical event: service stopped at 10:00.
Later evidence: operator stopped service intentionally for maintenance.
Revised causal interpretation: maintenance action caused service stop.
```

The stop event did not change. The causal explanation improved.

## Required Findings

### Sequence is not causality

Sequence establishes order, subject to timestamp quality. It can make a cause
candidate possible, but it does not prove productive contribution.

### Correlation is not causality

Correlation establishes co-occurrence, repeated association, or statistical
relationship. It can support investigation or probabilistic assessment, but it
does not by itself establish mechanism or cause.

### Explanations are not necessarily causal facts

An explanation may describe support, selection, absence, relevance, history, or
uncertainty. A causal explanation should cite or qualify its causal claim; other
explanations should not be read as root-cause assertions.

### Consequences are not necessarily causes

A consequence is an outcome, impact, or risk. It may be caused by an event, but
it is not itself the cause unless a separate causal claim supports that role.

### Causal claims require support

The stronger the causal language, the stronger the required support. Temporal
order, correlation, and ordinary relationships are useful inputs but not
sufficient by themselves for established cause.

### History may exist without causal understanding

Seed can preserve that events occurred without knowing why they occurred or how
they relate causally.

### Recommendations may rely on causal hypotheses

A recommendation can be relevant because a hypothesis is worth investigating,
not because the hypothesis is established. The recommendation should preserve
that distinction.

### Seed should preserve uncertainty when causes are not established

Unknown cause, possible cause, likely cause, and known cause are different
states. Explanations and recommendations should use language that matches the
support.

## Non-Goals

This reconciliation does not propose or require:

- a new causal schema;
- a new explanation schema;
- a new relationship kind;
- a new event model;
- a new consequence model;
- a new recommendation model;
- changes to observations, facts, relationships, projections, assessments,
  recommendations, decisions, commands, actions, event systems, timeline
  systems, or tests;
- automatic causal inference from event order;
- automatic causal inference from correlation;
- automatic root-cause analysis;
- automatic conversion of explanations into causal facts;
- automatic conversion of consequences into causal claims;
- automatic remediation based on causal hypotheses; or
- changes to runtime semantics.

## Implementation Implications

Because this is a documentation-only boundary audit, implementation implications
are limited to interpretive constraints for future design and review:

1. Future designs should not use sequence or correlation alone as established
   causal support.
2. Causal language should preserve modality: known, likely, possible,
   hypothesized, reported, correlated, preceding, or unknown.
3. Explanations should identify whether they are support explanations,
   selection explanations, relevance explanations, causal explanations, or mixed
   explanations.
4. Consequence reasoning should remain separate from root-cause reasoning.
5. Recommendations may cite causal hypotheses, but should not present them as
   established causes unless support justifies that strength.
6. Ordinary relationships may provide mechanism or context, but should not be
   treated as proof of incident-specific causation.
7. Historical event preservation should be independent of causal interpretation.
8. Later evidence may revise causal claims without rewriting the occurrence
   history.
9. Unknown cause should remain expressible and useful.

These are boundary constraints, not requests to modify runtime behavior.

## Architectural Invariants

The findings support the following architectural invariants:

```text
Events describe occurrences.
Changes describe transitions.
Consequences describe outcomes, impacts, or risks.
Relationships connect entities, artifacts, concepts, or claims.
Explanations connect knowledge into question-relative answers.
Causal claims assert productive contribution and require support.
Sequence alone does not justify causality.
Correlation alone does not justify causality.
Ordinary relationships alone do not justify causality.
Consequences are distinct from causes.
Recommendations may rely on causal hypotheses without proving them.
Unknown cause is a valid state.
History and causality are different concerns.
A timeline is not a causal graph.
Causal interpretation may change while event history remains stable.
Uncertainty should be preserved when causes are not established.
```

## Example Reconciliations

### Filesystem detached and service unavailable

```text
Event A: filesystem /data detached at T1
Relationship: service S depends_on /data
Event B: service S unavailable at T2
Consequence: availability goal threatened
```

Safe interpretations:

- the detach event preceded the outage if timestamp support is adequate;
- the dependency relationship provides a plausible mechanism;
- the outage consequence explains why the event matters;
- the detachment is a possible or likely cause only if supporting evidence is
  strong enough; and
- the cause remains unknown if the dependency and timing are the only support.

Unsafe interpretation:

```text
T1 before T2, therefore detachment caused outage.
```

### Backup failed with elevated data-loss risk

```text
Event: backup failed
Consequence: recovery point objective may be at risk
Recommendation: investigate backup pipeline
```

The recommendation is relevant even if the root cause is unknown. Causal
hypotheses may prioritize investigation, but the risk consequence is not itself
a root-cause claim.

### Host reboot and package removed

```text
Event A: host rebooted
Event B: package removed
```

The reboot and removal may share a maintenance window, but co-occurrence does
not establish that reboot caused removal or removal caused reboot. Seed should
preserve the events, note the temporal relationship if relevant, and avoid
causal language unless support links them.

### Operator-provided root cause

```text
Operator note: service outage caused by storage maintenance
Event: storage maintenance occurred
Event: service unavailable
```

The operator note is evidence of a reported cause. Seed may present it as
operator-reported, accepted, corroborated, or contradicted depending on authority
and support. It should not silently erase provenance or uncertainty.

## Conclusion

Seed may reason about causes by preserving the boundary between occurrence,
transition, outcome, edge, explanation, and causal assertion.

The key reconciliation is:

```text
An event is an occurrence.
A change is a transition.
A consequence is an outcome or risk.
A relationship is an edge.
An explanation is a question-relative connection of knowledge.
A causal claim is an evidence-backed or hypothesis-labeled assertion of
productive contribution.
```

Causal reasoning is valuable for incident analysis, historical understanding,
recommendation relevance, and operator trust. It is also easy to overstate.
Seed should therefore make causal support explicit, distinguish sequence and
correlation from causation, keep consequences distinct from causes, allow
unknown cause as a valid state, and preserve uncertainty whenever causes are not
established.
