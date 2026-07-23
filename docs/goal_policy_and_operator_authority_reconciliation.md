# Goal Policy And Operator Authority Reconciliation

## Purpose

This document performs a documentation-only reconciliation of goals, policy,
operator authority, intent ownership, authorization boundaries, and the
relationship between recommendations, decisions, commands, actions, and approved
objectives.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify
routing, modify capabilities, modify commands, modify actions, modify approvals,
modify policies, modify authentication, modify authorization systems, modify
projections, modify assessments, modify recommendations, or modify tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established that Seed is claim-centric, operators are
intent-centric, questions bridge intent and claims, assessments interpret
knowledge, recommendations relate knowledge to intent, decisions are distinct
from recommendations, and commands are distinct from actions.

The remaining question is:

```text
Why is a recommendation relevant?
```

Example:

```text
Assessment: low disk space
Recommendation: investigate storage utilization
```

That recommendation is incomplete unless Seed can explain the relevance path:

```text
Relevant to which goal?
Requested by which operator or interaction?
Constrained by which policy?
Permitted under which authority?
```

The central boundary is:

```text
Seed may relate knowledge to operator objectives; Seed must not silently invent
operator objectives.
```

## Central Finding

Seed should preserve a chain of distinct concepts:

```text
operator
  -> intent
  -> goal
  -> policy
  -> recommendation
  -> decision
  -> command
  -> action
```

This chain is not a pipeline in which each layer automatically authorizes the
next. It is a conceptual dependency chain for explanation, constraint, and
auditability. The useful shorthand is:

```text
Operators own intent.
Goals express desired outcomes.
Policy constrains acceptable behavior.
Authority determines what may occur.
Recommendations relate knowledge to goals.
Decisions select among alternatives.
Commands request execution.
Actions change reality.
```

Goals answer what outcome is desirable. Policy answers which behavior is
acceptable. Authority answers who or what may bind Seed or the environment to a
choice or execution. Recommendations answer what could be considered in light of
knowledge and a goal. Decisions answer what has been selected, rejected,
deferred, or escalated. Commands answer what bounded execution is requested.
Actions answer what actually happened or changed.

Therefore, a recommendation should explain both:

1. its evidence path; and
2. its goal relevance path.

A recommendation that can only explain evidence may be true to the knowledge but
unmoored from operator purpose. A recommendation that can only explain purpose
may be desirable but unsupported. Seed needs both boundaries without collapsing
them.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/operator_intent_question_and_claim_interface_reconciliation.md`
- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/capability_authority_and_execution_boundary_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/impact_overview_authority_reconciliation.md`
- `docs/state_summary_authority_reconciliation.md`
- `docs/operation_support_boundary_reconciliation.md`
- `docs/policy_pending_action_inventory.md`
- `docs/pending_action_lifecycle_inventory.md`
- `docs/recommendation_selection_boundary.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/documentation_authority_reconciliation.md`
- `docs/architecture_principles.md`
- `docs/invariants.md`

## Boundary Summary

| Concept | Primary owner | Primary role | Answers | Must not become |
| --- | --- | --- | --- | --- |
| Operator | Human, organization, or delegated principal | Source of intent and possible authority | Who is engaging or authorizing Seed? | Hidden policy, automatic execution, evidence source by default |
| Intent | Operator domain, optionally represented at the interface | Purpose, concern, task, or motivation | Why is the operator engaging Seed? | Claim, policy, authorization, decision, action |
| Goal | Operator-owned objective represented for reasoning | Desired outcome or target state | What outcome is desirable? | Recommendation, approval, policy, command, action |
| Policy | Governance / constraint domain | Rules, constraints, permissions, prohibitions, approval requirements, and preferences | What behavior is allowed, required, disallowed, or preferred? | Intent, goal, evidence, recommendation, action result |
| Authority | Authorization boundary spanning operators, policy, and bounded Seed components | Power to decide, approve, request, execute, or communicate within scope | Who or what may make this transition? | Desirability, evidence, policy text alone, implementation capability |
| Recommendation | Advisory domain | Suggested possible response related to knowledge and a goal | What could be considered, and why is it relevant? | Decision, approval, command, action, operator objective |
| Decision | Selection / commitment domain | Accepted, rejected, deferred, escalated, or chosen option | What has been selected under authority and constraints? | Goal, policy, command, action |
| Command | Execution-request domain | Bounded request to perform an operation | What execution is being requested? | Approval, execution result, action |
| Action | Environment / execution-effect domain | Executed operation or externally visible mutation | What happened or changed? | Decision rationale, command intent, recommendation |

## 1. What Is A Goal?

A goal is an explicit desired outcome, target state, or objective that gives
operator intent a more durable or evaluable form.

Examples include:

```text
maintain service availability
preserve data
reduce operational risk
deploy software
answer a question
restore service
prepare for a change window
minimize cost
preserve historical evidence
```

A goal is not merely a phrase that appears in a response. Architecturally, a
goal has three important properties:

1. **Outcome orientation:** it describes a desired condition, not a specific
   execution step.
2. **Relevance function:** it allows knowledge to be evaluated as relevant,
   irrelevant, urgent, blocking, helpful, risky, or conflicting.
3. **Decision context:** it influences which options are attractive, but it does
   not itself select or authorize an option.

Goals belong primarily to the **operator domain**. Seed may represent goals when
an operator states them, when a workflow carries them, when an interface needs to
explain recommendation relevance, or when preserved decision records need to show
which objective a decision served. That representation does not transfer
ownership of the goal to Seed.

Seed may reason about goals in the limited sense of relating preserved knowledge,
assessments, risks, options, and constraints to an objective. Seed should not
silently create a goal and then use that invented goal to justify advice,
priority, decision selection, or execution.

The safest definition is:

```text
A goal is an operator-owned desired outcome that Seed may represent and reason
about for relevance, explanation, and decision context without owning it.
```

### Goal classification

Goals are not purely Seed-domain because Seed is claim-centric rather than
objective-owning. Goals are not entirely outside Seed because operator-facing
reasoning, recommendations, explanations, and decisions may need to reference
which objective was being served. Therefore goals are best classified as:

```text
operator-owned objectives that may be represented at Seed's interface,
```

## 2. What Is Policy?

Policy is an explicit governance rule or constraint that defines acceptable,
required, prohibited, preferred, or approval-gated behavior for a scope.

Examples include:

```text
never modify production automatically
collect local observations automatically
require approval before package installation
preserve historical evidence
only use verified providers for registered operations
allow read-only local inventory collection without approval
retain provenance for promoted facts
```

Policy can express several kinds of governance:

| Policy expression | Meaning | Example |
| --- | --- | --- |
| Constraint | Limit on acceptable behavior | Do not mutate production automatically. |
| Permission | Explicit allowance within scope | Read-only local observations may run automatically. |
| Prohibition | Explicit disallowance | Never delete historical evidence. |
| Requirement | Mandatory condition before proceeding | Package installation requires approval. |
| Preference | Ordering or default when multiple allowed choices exist | Prefer verified local providers. |
| Escalation rule | Condition requiring human or higher authority | Ask operator before high-impact change. |
| Preservation rule | Requirement to retain evidence, rationale, or history | Preserve decision support and provenance. |

Policy may reference objectives, but policy is not the objective itself. For
example, `preserve historical evidence` can be expressed as a policy requirement
and may also serve a goal of auditability. The architectural role differs:

```text
Goal: historical evidence remains available and trustworthy.
Policy: do not delete historical evidence; retain provenance records.
```

Policy may also encode authority rules, but policy is not identical to
authority. A policy can state that an operator approval is required. The actual
authority comes from the recognized operator role, delegated principal, or
bounded system component acting within policy. Policy names and constrains the
authority path; it does not magically create all authority by existing as text.

The safest definition is:

```text
Policy is scoped governance over behavior, authority use, constraints,
preferences, and approval requirements. It constrains what may occur; it does
not replace operator intent or goals.
```

## 3. What Is Authority?

Authority is the recognized power to make a transition binding within a defined
scope. It answers whether a person, policy rule, or Seed subsystem may perform a
specific role such as communicate a projection, create an assessment, propose a
recommendation, record a decision, request execution, execute a command, or
mutate an environment.

Authority is not one thing. It is layered:

| Authority kind | Belongs primarily to | Meaning |
| --- | --- | --- |
| Intent authority | Operator | The operator may state purpose, need, concern, and desired outcomes. |
| Goal authority | Operator, possibly organization through delegation | The operator or organization owns the objective Seed is serving. |
| Knowledge authority | Seed knowledge components within evidence rules | Seed may preserve, select, project, and explain supported claims within its knowledge boundaries. |
| Assessment authority | Seed interpretive components within scoped rules | Seed may interpret knowledge under explicit frames without deciding or acting. |
| Advisory authority | Seed advisory surfaces within evidence, goal, and policy boundaries | Seed may suggest options, caveats, and relevance without approving them. |
| Policy authority | Governance source accepted for the scope | Policy may constrain, require, permit, deny, or escalate behavior. |
| Decision authority | Operator, delegated principal, or explicit policy automation | A recognized authority may select, reject, defer, approve, or escalate an option. |
| Command authority | Authorized requester plus command validation path | A command may be requested only when the requester and policy allow it. |
| Execution authority | Execution subsystem within registered capability and policy bounds | A bounded executor may perform the authorized operation and record results. |

Operators own intent and goals. Operators may also hold decision and command
authority depending on role, scope, environment, and policy. Operators do not
create knowledge authority merely by stating a claim; operator-provided reports
may be input evidence or observations, but claim support still requires evidence
and provenance boundaries.

Seed owns only bounded functional authority assigned by architecture:

```text
communicate preserved knowledge
interpret scoped knowledge
surface advisory options
validate requests
record events
execute registered operations only through authorized execution paths
```

Seed does not own the operator's objectives. Seed also does not acquire
decision or mutation authority merely because it can compute a recommendation.

Policy owns no physical execution and no human intent. Policy's authority is
normative: it constrains, permits, denies, requires, or escalates transitions
when accepted for the relevant scope. Policy can authorize some low-risk
automation if the governance model explicitly grants that authority, but the
policy rule and the executing component remain separate.

The critical distinction is:

```text
Authority determines what may occur. Goals determine what is desirable. Evidence
determines what is supported. These are different questions.
```

## 4. Relationship Between Intent And Goals

Intent is the operator's purpose for engaging Seed. A goal is a desired outcome
that expresses, refines, or stabilizes that purpose.

Example:

```text
Intent: keep services healthy
Goal: maintain service availability
```

The relationship is close but not identical:

| Relationship | Meaning |
| --- | --- |
| Expression | A goal may express broad intent in outcome-oriented form. |
| Refinement | A goal may narrow vague intent into something evaluable. |
| Durability | A goal may persist across several questions, assessments, recommendations, or decisions. |
| Comparison | Multiple goals may compete, such as restore quickly versus minimize risk. |
| Context | A goal provides context for recommendation relevance and decision tradeoffs. |

Intent can be immediate and conversational:

```text
Why is this service unhealthy?
```

A goal can be more durable:

```text
maintain service availability during the incident
```

A single intent may imply several candidate goals, but Seed should not silently
choose among them when the distinction matters. For `keep services healthy`,
possible goals include maintaining availability, reducing error rates, reducing
latency, preserving data, avoiding risky changes, or improving observability.
Those goals can imply different recommendations.

Therefore:

```text
Goals are operator-owned desired outcomes that may express or refine intent;
they are not identical to intent and do not by themselves authorize action.
```

## 5. Relationship Between Goals And Recommendations

Recommendations may depend on goal context because relevance is not determined
by evidence alone.

Example:

```text
Assessment: storage risk elevated
Goal: preserve service availability
Recommendation: investigate storage consumption and capacity pressure
```

The assessment explains what the knowledge indicates. The goal explains why that
assessment matters. The recommendation proposes a possible response.

The same assessment can produce different recommendations under different goals:

| Assessment | Goal | Possible recommendation |
| --- | --- | --- |
| Storage risk elevated | Preserve service availability | Investigate largest consumers and capacity headroom. |
| Storage risk elevated | Preserve evidence | Avoid deletion; snapshot or archive evidence before cleanup. |
| Storage risk elevated | Minimize cost | Review retention policy and identify low-value growth. |
| Storage risk elevated | Prepare deployment | Defer deployment or verify rollback space before proceeding. |
| Storage risk elevated | Answer a question | Explain support, freshness, thresholds, and affected entities. |

This does not mean every recommendation must wait for a fully formalized goal.
Seed can present weakly scoped recommendations when the operator's purpose is
clear from the interaction, but the recommendation should be honest about its
scope:

```text
Assuming the goal is to preserve service availability, consider investigating
storage consumption.
```

If the goal is ambiguous or materially changes the advice, Seed should ask for
clarification or present alternatives rather than silently selecting an
objective.

A recommendation's explainability should therefore include:

```text
evidence: observations, facts, relationships, assessment, freshness, caveats
goal relevance: the objective this option serves
policy status: whether the option appears allowed, disallowed, or approval-gated
authority status: who or what could decide or request the next transition
```

## 6. Relationship Between Goals And Decisions

A decision is a selection among alternatives, including accepting, rejecting,
deferring, escalating, or choosing an option. A goal is the desired outcome that
informs the selection.

Example:

```text
Goal: preserve service availability
Recommendation: investigate storage consumption
Decision: outage investigation approved
```

Goals influence decisions by supplying evaluation criteria:

- Does this option advance the desired outcome?
- Does it conflict with another goal?
- Is it proportional to the risk or urgency?
- Is it acceptable under policy?
- Is the authorized decision-maker allowed to select it?

Goals differ from decisions in several ways:

| Goal | Decision |
| --- | --- |
| Desired outcome | Selected option or disposition |
| Can span many interactions | Occurs at a particular point in a lifecycle |
| Explains desirability | Records selection, rejection, deferral, or escalation |
| Operator-owned | Authority-owned by operator, delegated principal, or explicit policy automation |
| Does not request execution | May lead to command request if authorized |

Goals do not authorize decisions by themselves. A goal can make a decision
rational, desirable, or urgent, but a decision still requires decision authority
and policy compatibility. For example, `restore service quickly` may make a
restart attractive, but it does not authorize restarting production if policy
requires approval.

The boundary is:

```text
Goals guide decision selection; authority authorizes decision selection; policy
constrains decision selection.
```

## 7. Relationship Between Policy And Decisions

Policy constrains recommendations, decisions, commands, and actions without
replacing goals.

Example:

```text
Goal: restore service quickly
Policy: production changes require approval
Recommendation: consider restarting the affected service
Decision: request approval or choose a read-only diagnostic first
Command: run approved diagnostic collection
Action: diagnostics executed
```

Policy affects each layer differently:

| Layer | Policy role |
| --- | --- |
| Recommendation | Label options as allowed, prohibited, risky, approval-gated, or requiring clarification. |
| Decision | Constrain which options may be selected and which authority is required. |
| Command | Validate whether the execution request is allowed, scoped, and approved. |
| Action | Bound what may be executed and require result recording, audit, or rollback handling. |

Policy can prevent a desirable option from being selected or executed. Policy can
also allow low-risk automatic behavior when explicitly granted. Neither case
turns policy into intent. Policy may say `do not modify production
automatically`; it does not say the operator's goal is unimportant. It says that
serving the goal must follow an approved path.

The important distinction is:

```text
Policy constrains the means. Goals describe desired ends. Decisions select a
policy-compatible path toward an end.
```

## 8. Can Seed Possess Goals?

Seed should not possess goals in the same sense that operators possess goals.
Seed should not own objectives such as `maintain availability`, `reduce risk`,
`minimize cost`, or `deploy software` unless those objectives are explicitly
provided by an operator, organization, workflow, or policy-governed configuration
as context for Seed's advisory or execution boundaries.

Seed may do several goal-related things without owning goals:

| Seed may... | Boundary |
| --- | --- |
| Represent goals | Only as declared, selected, inferred-with-caveat, or workflow-provided context. |
| Reason about goals | Only to explain relevance, compare options, surface tradeoffs, or detect ambiguity. |
| Preserve goals | Only as part of transparent interaction, decision, audit, or workflow context. |
| Execute toward goals | Only after authorized decisions and commands, through bounded capabilities. |
| Ask about goals | When ambiguity affects relevance, policy, or authority. |
| Refuse goal misuse | When an objective would require disallowed behavior or unsupported authority. |

Seed should not:

```text
silently invent operator objectives
retrofit a goal to justify a recommendation
convert a recommendation into an objective
use an assumed goal to bypass policy
use goal desirability as authorization
hide conflicting goals
claim an action served a goal without preserving the decision path
```

There is one limited sense in which Seed can have architectural objectives: Seed
may have design obligations such as preserving evidence, maintaining boundary
integrity, avoiding unsupported claims, or respecting policy. Those are not
operator task goals. They are system invariants and governance constraints.
Calling them `Seed goals` risks confusion. Prefer:

```text
Seed invariants
Seed obligations
architectural constraints
policy requirements
```

Thus the central answer is:

```text
Seed may reason about, preserve, and act within operator-owned goals. Seed
should not silently own or invent those goals.
```

## 9. What Should Not Be Collapsed Together?

The following concepts must remain distinct:

```text
Intent: keep systems healthy
Goal: maintain availability
Policy: no automatic production changes
Assessment: outage risk elevated
Recommendation: investigate outage
Decision: outage investigation approved
Command: run diagnostic collection
Action: diagnostics executed
```

They are distinct because each answers a different architectural question:

| Concept | Question answered | Collapse risk |
| --- | --- | --- |
| Intent | Why is the operator here? | Treating motive as evidence or approval. |
| Goal | What outcome is desired? | Treating desirable outcome as selected action. |
| Policy | What behavior is acceptable? | Treating constraints as objectives or intent. |
| Assessment | What does knowledge indicate? | Treating interpretation as remediation. |
| Recommendation | What could be considered? | Treating advice as decision or approval. |
| Decision | What has been selected? | Treating selection as execution. |
| Command | What execution is requested? | Treating request as result or as policy approval. |
| Action | What changed? | Treating effects as rationale or authorization. |

The most dangerous collapses are:

1. **Goal into recommendation:** `maintain availability` becomes `restart the
   service` without comparing alternatives.
2. **Recommendation into decision:** `consider restart` becomes `restart
   approved` without decision authority.
3. **Policy into intent:** `approval required` is misread as `the operator wants
   approval workflow` rather than a constraint on serving the goal.
4. **Authority into policy:** a written rule is treated as sufficient authority
   even when the actor, role, scope, or approval evidence is missing.
5. **Decision into command:** `investigation approved` becomes an unbounded
   execution request.
6. **Command into action:** `run diagnostics` is reported as if diagnostics
   actually ran.
7. **Action into evidence of wisdom:** a completed mutation is treated as proof
   that the recommendation was correct.

Preserving these boundaries allows Seed to explain not only what it knows, but
why an option was relevant, who selected it, how it was constrained, and what
actually occurred.

## 10. Authority Chain And Required Transitions

The conceptual authority chain is:

```text
operator
  ↓ states or delegates
intent
  ↓ expresses or refines
 goal
  ↓ constrained by
policy
  ↓ informs and bounds
recommendation
  ↓ selected by authorized actor or policy automation
decision
  ↓ translated into bounded request
command
  ↓ executed by authorized capability
action
```

This chain contains several different transition types:

| Transition | Requires authority? | Required boundary |
| --- | --- | --- |
| Operator -> intent | Yes, source attribution | Seed should know whose intent is represented or whether intent is inferred. |
| Intent -> goal | Sometimes | If goal is inferred, Seed should mark it as assumption or ask clarification when material. |
| Goal -> policy | Not a derivation | Policy does not come from the goal; policy applies from governance scope. |
| Policy -> recommendation | Yes, advisory constraint authority | Recommendation should account for allowed, prohibited, approval-gated, or unknown status. |
| Recommendation -> decision | Yes, decision authority | Advice cannot select itself; an authorized actor or explicit automation must decide. |
| Decision -> command | Yes, command/request authority | Selection must be translated into a bounded, validated request. |
| Command -> action | Yes, execution authority | A registered capability or execution path must be authorized and must record results. |

The chain should also preserve negative transitions:

```text
recommendation rejected
decision deferred
policy requires approval
command refused
action failed
authority missing
goal ambiguous
```

Those states are not errors in the architecture. They are evidence that the
boundary is visible.

## Recommendation Relevance Contract

A recommendation should be able to answer the following questions without
collapsing into a decision:

1. **What knowledge supports it?**
   - observations, facts, relationships, assessments, confidence, freshness,
     contradiction state, and provenance;
2. **Which goal makes it relevant?**
   - declared goal, workflow goal, operator-stated intent, or clearly labeled
     assumption;
3. **Which alternatives were considered or why is the option scoped?**
   - read-only investigation, remediation, escalation, deferral, or refusal;
4. **What policy status applies?**
   - allowed, prohibited, approval-required, risk-gated, unknown, or not yet
     evaluated;
5. **Who could decide?**
   - operator, delegated principal, explicit policy automation, or no current
     authority;
6. **What would be the next boundary?**
   - decision, clarification question, approval request, command proposal, or no
     action.

This contract is conceptual. It does not require a new schema in this document.
It states the architectural information that future representations should not
obscure.

## Non-Goals

This reconciliation does not require or recommend immediate implementation of:

- new goal schemas;
- new policy schemas;
- new authority models;
- new approval systems;
- new recommendation records;
- new decision records;
- new command or action behavior;
- new runtime routes;
- new tests;
- changes to authentication or authorization;
- changes to projections, assessments, recommendations, commands, or actions.

It also does not define a full policy language, role model, planning system,
autonomous agent loop, remediation engine, or workflow engine.

## Implementation Implications

The findings imply documentation-level guardrails for future work:

1. Recommendation explanations should not only cite evidence; they should also
   state the goal or assumed goal that makes the recommendation relevant.
2. If the goal is inferred and materially affects advice, the inference should be
   visible, caveated, or converted into a clarification question.
3. Policy status should be represented as a constraint on an option, not as proof
   that the option is desirable.
4. Authority status should be represented as permission for a transition, not as
   proof that the transition is wise.
5. Decisions should preserve the selected goal context when that context matters
   to the selection rationale.
6. Commands should remain bounded execution requests and should not absorb the
   goal, recommendation, or decision record.
7. Actions should report execution and effects without rewriting the rationale
   that led to them.
8. Seed invariants should be named as invariants, obligations, or policy
   requirements rather than hidden Seed-owned goals.

These implications are not implementation instructions for this change. They are
architectural constraints for preserving conceptual boundaries if future designs
introduce explicit goal, policy, recommendation, decision, command, or action
representations.

## Architectural Invariants

This reconciliation supports the following invariants:

1. Operators own intent.
2. Goals express desired outcomes.
3. Goals are primarily operator-owned, even when represented by Seed.
4. Seed may reason about goals without owning them.
5. Seed should not silently invent operator objectives.
6. Policy constrains acceptable behavior.
7. Policy is not intent.
8. Policy constrains action without replacing goals.
9. Authority determines what may occur, not what is desirable.
10. Authority is not policy.
11. Desirability, support, permission, and execution are distinct concerns.
12. Assessments interpret knowledge; they do not choose responses.
13. Recommendations may depend on goals.
14. Recommendations relate knowledge to goals; they are not goals.
15. Recommendations should explain both evidence and goal relevance.
16. Decisions select among alternatives; they are not goals.
17. Goals may influence decisions but do not authorize decisions.
18. Commands request execution; they are not decisions or actions.
19. Actions change reality; they are not recommendations, decisions, or commands.
20. Boundary-preserving systems should preserve negative outcomes such as
    refusal, deferral, missing authority, policy denial, and ambiguity.

## Conclusion

A recommendation is relevant when it connects supported knowledge to an
operator-owned goal under applicable policy and authority constraints. Evidence
alone can justify that an assessment is supported, but it cannot prove which
objective matters. A goal can explain desirability, but it cannot authorize a
decision or action. Policy can constrain acceptable means, but it does not
replace intent. Authority can permit transitions, but it does not decide what is
desirable.

Seed's architectural responsibility is therefore to preserve the separations:

```text
intent is owned
goals are desired
policy constrains
authority permits
knowledge supports
assessments interpret
recommendations advise
decisions select
commands request
actions mutate
```

Seed may help operators connect knowledge to objectives. It must not silently
become the owner of those objectives.
