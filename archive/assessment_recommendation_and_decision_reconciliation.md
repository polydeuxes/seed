# Assessment Recommendation And Decision Reconciliation

## Purpose

This document performs a documentation-only reconciliation of assessments,
recommendations, decisions, commands, actions, and their relationship to
projections.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify projections, observations,
facts, relationships, capabilities, plans, approvals, commands, actions, LLM
integrations, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established claim strength and assertion semantics,
operator interface and projection authority, relationship promotion,
corroboration and fact promotion, and trust and authority boundaries.

The remaining question is:

```text
What exists between a projection and a command?
```

Example projections can communicate:

```text
filesystem free space 5%
service unavailable
package installed
```

Those projections communicate knowledge. They do not, by themselves, answer:

```text
Is this a problem?
Should something be done?
What should be done?
Who should decide?
```

## Central Finding

Seed should preserve a chain of distinct concepts:

```text
Projection
  -> Assessment
  -> Recommendation
  -> Decision
  -> Command
  -> Action
```

The useful shorthand is:

```text
Projections communicate.
Assessments interpret.
Recommendations suggest.
Decisions select.
Commands request.
Actions mutate.
```

These are not synonyms. They represent increasing distance from knowledge
communication and increasing proximity to mutation. Authority requirements,
explainability requirements, and audit traceability should become stricter as
the chain approaches command and action.

The central boundary is:

```text
Knowledge and mutation are different concerns.
```

A projection may expose evidence-backed knowledge. An assessment may interpret
that knowledge as condition, risk, drift, or sufficiency. A recommendation may
suggest possible responses. A decision may select one response, defer, reject,
or escalate. A command may request execution through a bounded capability path.
An action is the execution effect or externally visible mutation that changes
reality or attempts to do so.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/conclusion_taxonomy_reconciliation.md`
- `docs/operation_support_boundary_reconciliation.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/audit/core_mvp_inventory_audit.md`

## Boundary Summary

| Layer | Primary verb | Primary question | Authority shape | Must not collapse into |
| --- | --- | --- | --- | --- |
| Projection | Communicates | What does the view expose from preserved knowledge? | Deterministic read-view authority | Assessment, recommendation, decision, command, action |
| Assessment | Interprets | What does this knowledge mean under a scoped condition or risk lens? | Evidence-backed interpretation authority | Command or remediation |
| Recommendation | Suggests | What responses could be considered? | Advisory authority, if any | Decision or approval |
| Decision | Selects | Which option is accepted, rejected, deferred, escalated, or chosen? | Decision authority or recorded operator/policy authority | Action or mutation |
| Command | Requests | What bounded execution is being requested? | Execution-request authority subject to validation and policy | Execution result |
| Action | Mutates | What was executed or what changed? | Execution authority plus environment effect | Decision rationale or command intent |

## 1. Projection

A projection is a deterministic read view over preserved knowledge structures.
It communicates what the view is authorized to select, group, filter, rank,
aggregate, or expose from observations, evidence, facts, relationships, and
related preserved state.

A projection may communicate:

```text
current selected fact values
support and provenance
confidence or assertion semantics when backed by projection rules
contradictions and integrity issues
relationships and related entities
observed timestamps and freshness signals
projection version and event lineage
```

A projection may not communicate as independent authority:

```text
unsupported conclusions
hidden evidence
new observation
live verification not performed by an observation path
operator approval
policy authorization
remediation choice
execution request
execution result
```

### Can projections contain recommendations?

Architecturally, no: recommendation is a distinct advisory layer, not projection
authority. A projection may expose recommendation records if such records already
exist as preserved knowledge and the projection is explicitly responsible for
showing them. That is different from the projection itself recommending.

For example, a future projection could show:

```text
recommendation R123 exists and is supported by assessment A456
```

It should not silently turn:

```text
filesystem free space 5%
```

into:

```text
you should delete files
```

unless that recommendation exists as an inspectable advisory object with support
and authority context.

### Can projections contain decisions?

Similarly, a projection may expose decision records, pending-action records, or
accepted-plan records that were already durably preserved. It may not make the
decision merely by presenting a current fact. Projection authority is selection
and communication authority, not decision authority.

## 2. Assessment

An assessment is an evidence-backed interpretation of projected or otherwise
preserved knowledge under a scoped evaluative frame.

It answers:

```text
What does this knowledge indicate?
```

Examples:

```text
low disk space detected
endpoint unreachable
configuration drift detected
observation sufficient for this claim
support is weak
contradiction affects current selection
```

Assessment describes knowledge and interpretation. It may also describe risk,
severity, sufficiency, uncertainty, contradiction, drift, or operational
significance. It does not request execution.

An assessment normally interprets one or more projections, facts, observations,
relationships, or support views. It should retain support sufficient to answer:

```text
Which knowledge was interpreted?
What rule, threshold, policy, comparison, or human rationale was used?
What scope does the assessment cover?
What caveats, contradictions, or freshness limits apply?
```

### Evidence required for assessment

An assessment should not exist as an unsupported assertion. At minimum, it needs:

```text
subject and scope
evidence or projection references
assessment predicate or criterion
assessment time or validity window
source of the interpretation
confidence, caveat, or strength when available
```

For example:

```text
Projection: filesystem free space 5%
Assessment: low disk space detected
Support: threshold free_space_percent < 10 for filesystem / at time T
```

The assessment is not the same object as the projection. The projection reports a
value. The assessment interprets that value under a threshold and scope.

## 3. Recommendation

A recommendation is an advisory suggestion for a possible response to an
assessment, condition, goal, gap, or operator question.

It answers:

```text
What could be done or considered?
```

Examples:

```text
investigate storage usage
inspect service logs
validate configuration
refresh the endpoint observation
ask the operator whether desired state changed
consider rollback only after drift is confirmed
```

Recommendation differs from assessment because assessment says what the
knowledge indicates, while recommendation suggests possible next steps.

```text
Assessment: endpoint unreachable.
Recommendation: inspect service logs and validate network path.
```

A recommendation may exist without a command. Many recommendations should remain
purely advisory, especially when evidence is incomplete, authority is missing,
risk is high, or multiple responses are plausible.

A recommendation may exist without execution authority. It may say:

```text
A reasonable next step is to inspect logs.
```

without saying:

```text
Seed is authorized to inspect logs now.
```

Recommendation authority, if present, is advisory authority. It is not approval,
selection, or execution authorization.

### Support required for recommendation

Every recommendation should explain why. The support may be an assessment,
operator goal, known capability gap, policy requirement, or explicit question.
A recommendation without support is indistinguishable from generic advice.

A recommendation can be generated directly from a projection in simple cases,
but it should still expose the interpretive bridge. For example:

```text
Projection: filesystem free space 5%
Recommendation: investigate storage usage
Reason: free space is below the low-space assessment threshold
```

In that case the assessment may be implicit in prose, but architecturally the
recommendation still depends on an assessment-like interpretation.

## 4. Decision

A decision is an authority-bearing selection among alternatives or lifecycle
outcomes.

It answers:

```text
Which option is selected, accepted, rejected, deferred, escalated, or considered sufficient?
```

Examples:

```text
issue accepted
remediation selected
observation sufficient
escalation required
storage investigation approved
action plan rejected
no-op selected
manual handoff selected
```

A decision differs from a recommendation because recommendation is advisory and
non-binding, while decision records a selected course, disposition, or lifecycle
state under some authority.

```text
Recommendation: inspect service logs.
Decision: service-log inspection approved for host web-01.
```

A decision differs from an action because selecting a path does not mutate the
world. A decision may authorize, reject, defer, or select a future command, but
it is not itself the command execution or its effect.

```text
Decision: package installation approved.
Action: package installed.
```

### Rationale required for decision

A decision should not exist without rationale. The rationale should identify:

```text
selected option
alternatives considered when relevant
supporting assessments or recommendations
authority source
scope and constraints
risk or policy outcome
operator approval when required
```

A decision may conclude that no command should be issued. Deferral, refusal,
manual ownership, no-op, or escalation are decisions when they select a lifecycle
path.

## 5. Command

A command is a bounded request for execution.

It answers:

```text
What operation is being requested, against what target, with what parameters, under what authority path?
```

Examples:

```text
run inventory
probe endpoint
execute package install
restart service
collect logs
```

A command differs from a recommendation because it is no longer merely advisory.
It is a request to do something.

A command differs from a decision because a decision selects or authorizes a
path, while a command expresses the concrete execution request on that path.

A command differs from an action because the command may fail validation, be
blocked by policy, wait for approval, be refused, time out, or be superseded. The
action is what actually happened or was attempted through the execution path.

A command should be traceable to a decision when it has state-changing potential
or material operational impact. Read-only commands may sometimes be initiated
from lower authority contexts, but they still require scope, capability,
validation, and policy boundaries appropriate to their risk.

## 6. Action

An action is an executed operation, attempted operation, or externally visible
mutation/effect.

It answers:

```text
What happened?
```

Examples:

```text
package installed
service restarted
firewall modified
file deleted
inventory executed
endpoint probe performed
```

Actions differ from commands because commands request execution; actions are the
execution attempt, effect, or recorded result. A command can be valid yet no
action occurs if approval is denied. An action can fail, partially succeed, or
produce observations without achieving the command's intended outcome.

Actions differ from decisions because decisions select or authorize; actions
mutate or attempt to mutate reality. Even read-only actions such as inventory or
probing can affect rate limits, logs, load, privacy, or external systems, so they
remain execution effects rather than mere knowledge.

Actions should be traceable to:

```text
command
validating capability or registered operation
policy result
decision or approval when required
operator or system authority
execution output and evidence extracted from the result
```

An action may create new observations. Those observations then re-enter the
knowledge path. The action itself should not be mistaken for a fact unless it is
preserved as evidence-backed event history and projected accordingly.

## 7. Authority Transitions

Authority requirements increase as Seed approaches mutation.

A useful gradient is:

| Layer | Typical authority requirement |
| --- | --- |
| Projection | Deterministic read-view authority over preserved knowledge |
| Assessment | Interpretive authority backed by evidence, declared criteria, or operator/policy context |
| Recommendation | Advisory authority backed by assessment, goal, or capability knowledge |
| Decision | Operator, policy, delegated system, or workflow authority to select an outcome |
| Command | Validated execution-request authority within capability, scope, and policy boundaries |
| Action | Execution authority plus approval, policy clearance, and runtime/tool boundaries appropriate to risk |

### When can Seed assess?

Seed can assess when it has sufficient evidence, projection support, or explicit
operator/policy criteria to interpret a condition within a scope. Assessment may
be automatic for declared thresholds or deterministic consistency checks, but it
must remain explainable and scoped.

### When can Seed recommend?

Seed can recommend when it can explain the advisory bridge from an assessment,
goal, capability gap, or operator question to a possible response. Recommendation
does not require execution authority, but it does require clarity that it is
advice rather than approval.

### When can Seed decide?

Seed can decide only within delegated decision authority. Some decisions may be
safe deterministic lifecycle outcomes, such as marking an observation
insufficient under explicit criteria. Other decisions, especially those that
select remediation, approve operational work, change trust/preference, or move
toward mutation, require operator or policy authority.

### When can Seed command?

Seed can command only when a request is routed through a supported capability,
validated operation, scope check, and policy path. A natural-language command
request from an operator is not itself enough to bypass validation, pending
action gates, approval boundaries, or registered-tool boundaries.

### When can Seed act?

Seed can act only when execution authority exists and the execution path permits
it. For state-changing or materially risky actions, operator approval or explicit
policy authorization must be preserved. The action must remain auditable and
traceable to the authority that allowed it.

## 8. Operator Role

The operator is not merely a source of observations. The operator may inspect,
question, declare intent, provide approval, reject recommendations, select
options, accept risk, or own manual action.

The operator role changes across layers:

| Layer | Inspectable without approval? | Usually requires operator authority? | Notes |
| --- | --- | --- | --- |
| Projection | Yes | No | Reading knowledge should be inspectable subject to access control. |
| Assessment | Yes | Usually no | Automatic or documented assessments can be inspectable if evidence and criteria are visible. |
| Recommendation | Yes | Usually no | Advice can be shown without approval, but must not imply authorization. |
| Decision | Inspectable yes; creation depends on scope | Often yes | Decisions that affect lifecycle, remediation, authority, or mutation need delegated authority. |
| Command | Inspectable yes; issuing depends on risk | Often yes | Command issuance must pass capability, validation, and policy gates. |
| Action | Result inspectable yes; execution depends on risk | Usually yes for mutation | Execution must follow approval/policy and preserve audit trail. |

Operator approval is not a world-state fact. It is authority evidence for a
workflow. For example:

```text
Operator approved storage investigation.
```

means the command path may be authorized under scope. It does not mean disk
space is low, the investigation succeeded, or remediation occurred.

## 9. Explainability Requirements

Explainability must survive throughout the chain.

### Projection explainability

A projection should expose or link to:

```text
source observations
facts or relationships selected
support and contradiction information
projection version and event lineage
selection rules or view responsibility
```

### Assessment explainability

An assessment should expose:

```text
interpreted projection or evidence
criterion, threshold, comparison, or rationale
scope and subject
risk/severity/sufficiency meaning
caveats and contradictions
```

An assessment without evidence is not an assessment; it is an unsupported claim.

### Recommendation explainability

A recommendation should expose:

```text
assessment or goal that motivates it
why the suggested response is relevant
known alternatives or uncertainty when material
required authority before command or action
expected next knowledge gained or risk reduced
```

A recommendation may be weak, provisional, or exploratory, but it should still
explain why it is being suggested.

### Decision explainability

A decision should expose:

```text
what was selected or rejected
why that option was chosen
who or what had authority
what evidence and recommendations informed it
what constraints, risks, or caveats apply
what downstream command/action is allowed or disallowed
```

A decision without rationale is an audit gap. It may still exist historically as
a recorded event, but architecturally it is insufficient for Seed's
explainability goals.

## 10. What Must Not Be Collapsed Together

The following chain contains six different objects:

```text
Projection: filesystem free space 5%
Assessment: low disk space
Recommendation: investigate storage
Decision: storage investigation approved
Command: run disk inventory
Action: inventory executed
```

They differ because:

| Object | Why it is distinct |
| --- | --- |
| Projection | Reports an evidence-backed value selected by a view. |
| Assessment | Interprets the value against a threshold or risk lens. |
| Recommendation | Suggests a possible response without selecting or executing it. |
| Decision | Records that an authority selected or approved a path. |
| Command | Requests a concrete bounded operation. |
| Action | Records execution or mutation resulting from the operation path. |

Collapsing these concepts creates specific failure modes:

| Collapse | Failure mode |
| --- | --- |
| Projection -> assessment | Read views silently become health or risk authorities. |
| Assessment -> recommendation | Every detected condition appears to imply a response. |
| Recommendation -> decision | Advice becomes approval without authority. |
| Decision -> command | Selection bypasses validation and capability scope. |
| Command -> action | Requests are mistaken for completed work. |
| Action -> fact | Execution effects become truth without evidence and projection. |

## Non-Goals

This reconciliation does not propose implementation work except where future
work needs vocabulary to preserve the documented boundaries.

It does not require:

```text
new schemas
new projection behavior
new assessment engine
new recommendation engine
new decision service
new command model
new action model
new approval flow
new ToolExecutor behavior
new LLM integration
new tests
```

It also does not require renaming existing runtime `Decision` or
artifacts. This document defines conceptual architectural boundaries that future
work should respect when naming or extending behavior.

## Implementation Implications

If future work touches these areas, it should preserve the following boundaries:

1. Projection code should not silently generate recommendations or decisions.
2. Assessment-producing code should preserve evidence, criteria, scope, and
   caveats.
3. Recommendation-producing code should mark outputs as advisory and explain why
   the recommendation follows from evidence or goals.
4. Decision-producing code should record authority, rationale, selected option,
   and alternatives where relevant.
5. Command issuance should be traceable to a decision or an explicit operator
   command request plus validation/policy path.
6. Actions should be traceable to command, policy, approval, execution context,
   and result.
7. LLM-mediated language may summarize or explain the chain, but must not become
   hidden authority for assessment, recommendation, decision, command, or action.
8. Operator-facing surfaces should label the layer they are showing: knowledge,
   interpretation, advice, selection, request, or execution result.

These are documentation implications, not implementation instructions for this
change.

## Architectural Invariants

The findings support the following invariants:

```text
Projections communicate.
Assessments interpret.
Recommendations suggest.
Decisions select.
Commands request.
Actions mutate.
```

```text
Knowledge and mutation are different concerns.
```

```text
Projection authority is not recommendation authority.
Recommendation authority is not decision authority.
Decision authority is not execution authority.
Execution authority is not proof of resulting world state.
```

```text
Assessment is not a command.
Recommendation is not a decision.
Decision is not an action.
Command is not proof of action.
Action is not proof of intended outcome.
```

```text
Authority should increase as state-changing potential increases.
```

```text
Every assessment should be supported by evidence or explicit criteria.
Every recommendation should explain why.
Every decision should explain why.
Every command with material operational impact should be traceable to a decision
or explicit operator request plus validation and policy.
Every action should be traceable to authority.
```

```text
Explainability must survive throughout the chain.
```

## Final Reconciliation

The object between projection and command is not one thing. It is a structured
sequence of interpretation, advice, and selection.

Projection tells Seed and the operator what is known under a view. Assessment
interprets that knowledge. Recommendation suggests responses. Decision selects a
path under authority. Command requests execution through a bounded capability.
Action records what executed or changed.

Seed should move from knowledge to potential action by preserving these
boundaries rather than collapsing them into a single fluent statement such as:

```text
Disk is low, so delete files.
```

A safer architectural chain is:

```text
Projection: filesystem free space 5%.
Assessment: low disk space under threshold X for filesystem Y.
Recommendation: investigate storage usage before remediation.
Decision: operator approved storage investigation within scope Z.
Command: run disk inventory with bounded read-only parameters.
Action: disk inventory executed; observations produced.
```

That chain keeps knowledge, interpretation, advice, authority, request, and
mutation distinct while still allowing Seed to progress from understanding to
responsible operation.
