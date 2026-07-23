# Goal Relevance And Recommendation Generation Reconciliation

## Purpose

This document performs a documentation-only reconciliation of goal relevance,
recommendation justification, recommendation generation boundaries,
consequence reasoning, and the relationship between assessments, goals, and
recommendations.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify recommendation generation,
assessments, decisions, policies, capabilities, commands, actions, projections,
authority systems, planners, routing, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established that operators are intent-centric, Seed is
claim-centric, questions bridge intent and claims, goals are operator-owned
desired outcomes, Seed may reason about goals without owning them,
recommendations are distinct from assessments, recommendations are distinct
from decisions, and recommendations should explain both an evidence path and a
goal relevance path.

The remaining question is:

```text
What makes a recommendation relevant?
```

Example:

```text
Assessment:     filesystem free space critically low
Goal:           maintain service availability
Recommendation: investigate storage utilization
```

The architectural problem is not merely whether the assessment is supported.
The assessment may be well supported while a proposed response is irrelevant to
the operator's current purpose. The missing explanation is the path from an
interpreted condition to an operator-owned desired outcome.

## Central Finding

Recommendation relevance is an advisory relationship, not a property owned by a
single object in isolation.

The safest architectural definition is:

```text
Recommendation relevance is the traceable relationship by which an evidence-backed
assessment is connected, through one or more possible consequences, to an
operator-owned goal such that the recommended consideration could reasonably
help preserve, restore, investigate, improve, or decide about that goal.
```

The useful chain is:

```text
Assessment
  -> Consequence
  -> Goal Relevance
  -> Recommendation
  -> Decision
  -> Command
  -> Action
```

The shorter operational shorthand is:

```text
Assessments identify conditions.
Consequences describe possible outcomes.
Goals express desired outcomes.
Recommendations connect assessed conditions to goals.
Decisions select among recommendations or alternatives.
Commands request execution.
Actions change reality.
```

A recommendation is justified only when Seed can explain both:

```text
Evidence path:        what supports the assessment or condition?
Goal relevance path:  why does that condition matter for this goal?
```

A recommendation may still be tentative, low confidence, policy-disallowed, or
unauthorized. Relevance does not provide confidence, authority, approval, or
execution permission. It only explains why the suggestion matters.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/goal_policy_and_operator_authority_reconciliation.md`
- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/explainability_audit.md`
- `docs/why_not_explanation_characterization.md`
- `docs/operation_support_boundary_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/claim_support_frontier.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/invariants.md`

## Boundary Summary

| Concept | Primary role | Answers | Must not become |
| --- | --- | --- | --- |
| Assessment | Evidence-backed interpretation of a condition | What does the knowledge indicate? | Goal, recommendation, decision, command, action |
| Consequence | Possible, observed, inferred, or projected outcome of a condition | What could or did result from this condition? | Goal, policy, decision, command |
| Goal | Operator-owned desired outcome | What outcome does the operator want to preserve or achieve? | Seed-owned truth, policy, authorization, command |
| Recommendation | Advisory connection between condition, consequence, and goal | What should be considered, and why does it matter? | Assessment, decision, approval, command, action |
| Decision | Selection, rejection, deferral, or escalation of an option | What option is chosen or declined? | Recommendation, command effect, action result |
| Policy | Constraint or rule over allowed behavior | What is permitted, required, forbidden, or constrained? | Goal, relevance, confidence |
| Authority | Right to decide, approve, request, or execute | Who or what may choose or act? | Relevance, evidentiary support, confidence |
| Confidence | Degree of warrant or uncertainty for a claim or interpretation | How sure is Seed about this assertion? | Relevance, authority, policy |

## 1. Recommendation Relevance

Recommendation relevance is the relationship that makes a recommendation matter
to a goal in light of an assessment.

It is not owned solely by the assessment because the same assessed condition can
matter differently under different operator goals. For example:

```text
Assessment: disk nearly full
Goal A:     maintain service availability
Relevant recommendation: investigate storage utilization or reduce write pressure

Goal B:     preserve forensic evidence
Relevant recommendation: snapshot storage state before cleanup

Goal C:     reduce cloud spend
Relevant recommendation: examine retention and storage allocation patterns
```

The assessment identifies a condition. It does not, by itself, determine which
operator outcome matters.

Recommendation relevance is also not owned solely by the goal. A goal such as
`maintain service availability` does not make every availability-related action
relevant. Relevance requires an assessed condition or plausible consequence that
connects the current knowledge state to that goal.

Recommendation relevance is not owned solely by the recommendation either. A
recommendation must carry or reference its relevance path, but it cannot create
that relevance merely by asserting it. The relevance path must be traceable to:

```text
assessment support
consequence reasoning
goal context
recommendation rationale
```

Recommendation relevance is therefore best modeled conceptually as a relation
among assessment, consequence, goal, and recommendation. Policy and authority
may constrain whether a relevant recommendation can be offered, selected, or
executed, but policy and authority are not the same as relevance.

### Relevance test

A recommendation is relevant when Seed can answer all of the following:

1. What assessed condition motivates the recommendation?
2. What consequence is possible, observed, inferred, or projected from that
   condition?
3. Which operator-owned goal would that consequence threaten, advance, delay,
   preserve, or clarify?
4. How would considering the recommendation help the operator reason about,
   preserve, restore, improve, or decide about that goal?
5. What assumptions, uncertainty, and alternatives affect the relevance claim?

If Seed cannot answer the goal relevance questions, the output may still be an
assessment, an alert, a generic next-step hint, or an investigative option, but
its recommendation relevance is under-explained.

## 2. Consequence Boundary

A consequence is an outcome that can follow from, coincide with, or be implied
by an assessed condition.

Examples:

```text
service outage
degraded performance
data loss
increased operational risk
missed recovery objective
operator workload increase
```

A consequence is not automatically a claim, assessment, projection, or
recommendation. Its classification depends on how Seed represents and supports
it.

| Consequence form | Meaning | Example |
| --- | --- | --- |
| Observed consequence | The outcome has evidence as something that happened or is happening | `service unavailable` supported by endpoint observations |
| Inferred consequence | The outcome is concluded from rules or relationships over evidence-backed claims | `dependent service affected` inferred from dependency and outage facts |
| Projected consequence | The outcome is estimated as a possible future state under assumptions | `disk exhaustion likely within N hours` |
| Explanatory consequence | The outcome is used to explain why a condition matters, without claiming it has occurred | `low free space can increase outage risk` |

Consequences are therefore best understood as explanatory constructs that may be
promoted into claims, assessments, or projections when the architecture provides
support and authority for that stronger status.

The phrase `service outage` can be:

```text
an observed claim when evidence shows outage;
an assessment when Seed interprets evidence as outage;
a projected consequence when Seed estimates future outage risk;
an explanatory consequence when Seed says why disk exhaustion matters.
```

The architecture should avoid treating all consequence language as the same
kind of object. Doing so would collapse explanation, observation, projection,
and recommendation.

## 3. Assessments And Consequences

Assessments interpret knowledge under a scoped evaluative frame. Consequences
state what may result from the assessed condition or what outcome gives the
assessment operational significance.

Example:

```text
Assessment:            disk nearly full
Potential consequence: service interruption
```

The consequence may be:

- **Observed** if service interruption is separately evidenced.
- **Inferred** if dependency, capacity, or service-behavior knowledge supports
  the conclusion.
- **Projected** if Seed estimates the future outcome under trend or threshold
  assumptions.
- **Explanatory** if Seed only uses the possible outcome to explain why the
  assessment deserves attention.

An assessment does not require a consequence to exist as an observed fact. A
condition can be assessed before its harmful outcome occurs. Conversely, an
observed consequence can motivate assessment of causes, such as `service outage`
leading to assessment of `disk nearly full`, `network partition`, or `process
crash`.

The safe relationship is:

```text
Assessment identifies or interprets a condition.
Consequence describes the possible or actual outcome that makes the condition matter.
```

A consequence should not be represented as a recommendation. `Service outage
risk increased` is not the same as `investigate storage utilization`. The first
states possible significance; the second suggests a response.

## 4. Goals And Consequences

A goal is an operator-owned desired outcome. A consequence is an actual or
possible outcome that may support, threaten, clarify, or be irrelevant to that
goal.

Example:

```text
Goal:        maintain service availability
Consequence: service interruption
```

The consequence establishes goal relevance because it describes a state that is
in tension with the desired outcome. If the operator's goal is to maintain
availability, then a possible service interruption matters. If the operator's
goal is to preserve forensic evidence, the same interruption may matter for a
different reason: preserving state before remediation may be more relevant than
immediate cleanup.

Goals establish relevance by supplying an evaluative target:

```text
desired outcome -> outcome to avoid, preserve, improve, restore, or investigate
```

Without a goal, Seed can still say that a condition is unusual, risky, stale,
unsupported, contradictory, or policy-constrained. But explaining why a
recommendation matters requires either an explicit goal, an interaction-scoped
operator concern, or a clearly declared default objective.

Goals are not policies. A goal such as `maintain availability` says what the
operator wants. A policy says what is permitted, required, forbidden, or
constrained. A goal may motivate action, but it does not authorize action.

## 5. Goals And Recommendations

Recommendations are advisory suggestions that connect assessed conditions to
operator goals through consequence reasoning.

Example:

```text
Goal:           preserve data
Assessment:     backup failures observed
Consequence:    recovery point objective may not be met; data loss risk increases
Recommendation: investigate backup pipeline
```

The recommendation is relevant because the assessment points to a consequence
that threatens the goal. It is justified only to the extent that Seed can explain
both the assessment support and the relevance path.

Recommendations often require goal context to be fully justified. The same
assessment can produce different recommendations under different goals:

```text
Assessment: backup failures observed

Goal: preserve data
Recommendation: investigate backup pipeline and verify recoverability

Goal: reduce alert fatigue
Recommendation: inspect backup alert thresholds and duplicate notifications

Goal: minimize change risk during a freeze
Recommendation: defer non-urgent remediation and collect non-invasive evidence
```

This does not mean every recommendation must wait for a bespoke goal object.
Some recommendations can rely on explicit workflow goals, declared system
objectives, operator questions, or documented default objectives such as
`maintain service availability` or `preserve data integrity`. When such defaults
are used, they should be visible rather than hidden.

## 6. Recommendation Justification Chain

The recommended explanation chain is:

```text
Assessment
  -> Consequence
  -> Goal Relevance
  -> Recommendation
```

Expanded:

```text
Evidence supports an assessment.
The assessment implies, increases risk of, or explains a consequence.
The consequence matters because it affects an operator-owned goal.
The recommendation is a possible response to investigate, preserve, restore,
improve, or decide about that goal.
```

Example:

```text
Evidence:       filesystem observations show free space at a critical threshold
Assessment:     filesystem free space critically low
Consequence:    writes may fail and services depending on writes may interrupt
Goal relevance: this threatens the operator goal of maintaining availability
Recommendation: investigate storage utilization
```

This chain is preferable to a direct assessment-to-recommendation jump because
it explains why this recommendation matters and why other recommendations may be
less relevant.

### Alternatives evaluated

#### Direct assessment to recommendation

```text
Assessment -> Recommendation
```

This is concise but incomplete. It can explain `what condition triggered the
suggestion`, but not `why this suggestion matters to the operator`.

#### Goal to recommendation only

```text
Goal -> Recommendation
```

This is under-supported. Goals alone do not show the current condition or why a
response is timely.

#### Assessment to goal only

```text
Assessment -> Goal
```

This can establish significance, but it does not explain why the proposed
response is the appropriate thing to consider.

#### Policy to recommendation

```text
Policy -> Recommendation
```

This can identify required or allowed behavior, but it should not replace goal
relevance. A policy may require escalation; it does not by itself prove the
recommendation is goal-relevant except through the policy's own stated purpose.

## 7. Relevance, Support, Authority, Policy, And Confidence

These terms should remain distinct.

| Term | Architectural meaning | Example question | Not the same as |
| --- | --- | --- | --- |
| Relevance | Relationship between condition, consequence, goal, and recommendation | Why does this matter for the goal? | Support, authority, confidence, policy |
| Support | Evidence, provenance, or rule basis for a claim or assessment | What backs this assertion? | Relevance or permission |
| Authority | Right to decide, approve, request, or execute | Who may choose or act? | Relevance or confidence |
| Policy | Normative rule constraining behavior | Is this allowed, required, or forbidden? | Goal or evidence support |
| Confidence | Degree of warrant or uncertainty | How reliable is this claim or interpretation? | Importance or authorization |

A high-confidence assessment can support an irrelevant recommendation. A highly
relevant recommendation can lack authority for execution. A policy-allowed
recommendation can have weak evidentiary support. A policy-required response can
still require explanation of the goal or obligation it serves.

Therefore:

```text
Support answers: why believe it?
Relevance answers: why does it matter?
Authority answers: who may decide or act?
Policy answers: what is allowed or required?
Confidence answers: how certain is Seed?
```

## 8. Recommendations And Decisions

A recommendation suggests a possible response. A decision selects, rejects,
defers, escalates, or otherwise records a choice about one or more options.

Example:

```text
Recommendation: investigate storage
Decision:       investigation approved
```

They are distinct because suggestion and selection have different authority
requirements. Seed may have advisory authority to explain a recommendation but
not decision authority to approve it. Even when automated decision-making is
allowed by policy, the decision should remain a separate auditable object so the
system can distinguish:

```text
what was suggested
why it was suggested
who or what selected it
under what authority it was selected
what command, if any, followed
what action, if any, changed reality
```

A recommendation can be relevant and still be rejected. A decision can accept an
option for reasons beyond the recommendation's relevance, such as maintenance
windows, risk tolerance, operator priorities, cost, or policy constraints.

## 9. Objects That Should Not Be Collapsed

The following concepts should remain separate:

```text
Assessment:     disk space low
Consequence:    outage risk increased
Goal:           maintain availability
Recommendation: investigate storage usage
Decision:       investigation approved
Command:        collect storage inventory
Action:         storage inventory executed
```

Reasons to preserve separation:

1. **Different truth conditions.** `Disk space low` is evaluated against
   observations or facts. `Maintain availability` is an operator objective.
   `Investigation approved` is a decision record.
2. **Different authority requirements.** Assessment requires interpretive
   authority. Decision requires decision authority. Command requires
   execution-request authority. Action requires execution authority and an
   actual effect or attempt.
3. **Different audit questions.** Operators need to ask why Seed believed a
   condition, why it mattered, why a response was suggested, who approved it,
   what was requested, and what happened.
4. **Different failure modes.** Evidence can be stale, relevance can be weak,
   authority can be missing, policy can forbid execution, command validation can
   fail, and actions can fail in the environment.
5. **Different reversibility.** Assessments and recommendations can usually be
   revised without mutating the environment. Commands and actions approach or
   cross the mutation boundary.

Collapsing these objects would make Seed less explainable, less auditable, and
less safe.

## 10. Can Seed Recommend Without A Goal?

Seed can produce several kinds of advisory output without a bespoke explicit
goal, but the strength of recommendation justification changes.

### Goal-dependent recommendations

Some recommendations require goal context because the same assessment supports
multiple possible responses.

Example:

```text
Assessment: sensitive files found in a workspace
Goal: reduce data exposure
Recommendation: review access controls

Goal: preserve investigation evidence
Recommendation: snapshot metadata before modification
```

Without a goal, Seed cannot fully justify which recommendation matters most.

### Goal-independent or default-goal recommendations

Some recommendations appear goal-independent because a default objective is
assumed, such as safety, data preservation, service availability, or maintaining
claim quality. Architecturally, these are better described as recommendations
with implicit or default goal context, not recommendations with no goal at all.

Example:

```text
Assessment: evidence for a current fact is stale
Default objective: maintain trustworthy current state
Recommendation: refresh observation
```

The default objective should be visible in the explanation when it materially
affects relevance.

### Condition-level next-step hints

Seed may also provide generic next-step hints that are not fully goal-justified.

Example:

```text
Assessment: disk nearly full
Hint: inspect large directories
```

This can be useful, but it should be presented as a condition-oriented
investigative option unless the goal relevance path is stated. If the operator
asks `why does this matter?`, Seed should either provide the goal relevance path
or acknowledge the missing goal context.

### Recommended boundary

Recommendations are conditionally goal-dependent:

```text
Every fully justified recommendation should have an explicit, implicit, or default
goal relevance path.
```

Seed may surface preliminary advisory options without a fully specified goal,
but those options should not pretend to be fully justified recommendations if
Seed cannot explain why they matter.

## Explainability Requirements

Recommendation explainability should include both paths:

```text
Evidence path
- evidence records, facts, projections, or observations supporting the assessment
- freshness, confidence, contradiction, and support limitations where relevant
- assessment rule, threshold, or interpretive frame where relevant

Goal relevance path
- goal or default objective used for relevance
- consequence that connects the assessment to that goal
- why the recommendation addresses, investigates, preserves, restores, or helps
  decide about the goal
- assumptions and uncertainty in the consequence or relevance path
- why-not notes for salient alternatives when selection or ranking is exposed
```

Seed should be able to answer:

```text
Why this recommendation?
Why not a different recommendation?
What assessment supports it?
What consequence makes it matter?
Which goal does it relate to?
Does relevance imply authority? No.
Does relevance imply confidence? No.
Does relevance imply policy permission? No.
```

## Non-Goals

This reconciliation does not require:

- new schemas;
- new recommendation generators;
- changes to assessment, decision, policy, command, action, projection,
  authority, planner, routing, or test behavior;
- promotion of consequences into first-class runtime objects;
- automatic goal inference;
- automatic remediation;
- hidden default goals;
- collapsing recommendation selection into action planning;
- treating relevance as execution permission.

## Implementation Implications

These findings do not require implementation work by themselves. If future work
chooses to implement recommendation relevance explicitly, the implementation
should preserve the following boundaries:

1. Store or expose the assessment support path separately from the goal
   relevance path.
2. Make any explicit, implicit, or default goal context inspectable.
3. Represent consequence reasoning without silently claiming that projected or
   explanatory consequences have occurred.
4. Keep recommendation, decision, command, and action records separate.
5. Keep relevance separate from support, confidence, policy permission, and
   authority.
6. Support `why this` and `why not` explanations without turning ranking into
   approval.
7. Preserve operator ownership of goals even when Seed reasons about them.

## Architectural Invariants

The findings support the following architectural invariants:

```text
Assessments identify conditions.
Consequences describe possible or actual outcomes.
Goals express operator-owned desired outcomes.
Recommendations connect assessments to goals through consequence reasoning.
Decisions select, reject, defer, or escalate recommendations or alternatives.
Commands request bounded execution.
Actions change reality or attempt to do so.

Recommendations are not assessments.
Recommendations are not decisions.
Recommendations are not commands.
Consequences are not goals.
Goals are not policies.
Goal relevance is not authority.
Goal relevance is not confidence.
Support is not relevance.
Policy permission is not recommendation justification.

The same assessment may have different relevance under different goals.
Every fully justified recommendation should explain why it matters.
Recommendation relevance should be traceable.
Recommendation explainability should include an evidence path and a goal
relevance path.
Goal ownership remains with the operator.
Seed may reason about goals without owning them.
```

## Conclusion

A recommendation becomes relevant when Seed can trace a relationship from an
evidence-backed assessment, through a possible or actual consequence, to an
operator-owned goal, and then explain how the suggested response helps the
operator reason about, preserve, restore, improve, or decide about that goal.

This relevance relationship is distinct from evidentiary support, confidence,
policy permission, and authority. Preserving those distinctions keeps Seed
claim-centric while allowing it to explain why advisory output matters to
operator-owned intent.
