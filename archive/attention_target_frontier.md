---
doc_type: frontier
status: exploratory
domain: attention target ontology
defines:
  - attention target frontier
  - candidate attention target
  - trigger target boundary
  - attention inquiry target boundary
  - attention working state boundary
  - attention frontier boundary
  - acquisition target tension
depends_on:
  - attention_trigger_frontier.md
  - selection_and_attention_frontier.md
  - inquiry_frontier.md
  - operations_frontier.md
  - capability_self_acquisition_readiness_audit.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - continuation_context_and_working_state_reconciliation.md
  - active_context_and_working_set_reconciliation.md
  - context_composition_reconciliation.md
  - selection_rationale_reconciliation.md
  - capability_gap_and_operator_bridge_reconciliation.md
  - capability_need_acquisition_reconciliation.md
  - handoff_consumption_activation_reconciliation.md
---

# Attention Target Frontier

## Purpose

The Attention Trigger Frontier investigated:

```text
What causes attention to move?
```

This frontier investigates the companion question exposed by that work:

```text
When attention becomes active, what object is actually being attended to?
```

The motivating tension is:

```text
Trigger for what?
```

The repository may currently be mixing things that activate attention with
things that receive attention. This document tests whether `attention target` is
a meaningful architectural concept, or whether existing vocabulary such as
question, goal, need, gap, tension, inquiry object, working state, active
context, selection, relevance, or frontier already explains the phenomenon.

This is ontology discovery only. It does not design planners, attention
systems, schedulers, acquisition engines, workflow systems, runtime behavior,
schemas, read models, routes, provider ranking, tool selection, context
algorithms, projections, event appends, or tests.

Repository authority wins over this document. Existing reconciliations remain
authoritative for their settled boundaries. Existing frontiers remain
exploratory and not implementation-ready.

---

## Starting Observation

The trigger frontier found candidate triggers such as:

```text
operator request
contradiction
tension
repeated failure
risk
anomaly
ambiguity
operator burden
```

Those candidates explain why attention may move, but not necessarily what
attention moves toward. A repeated failure may trigger attention, but the object
of attention may be the unresolved need, the unmet goal, the deficient
capability, or the failure pattern itself. A contradiction may trigger
attention, but the attended objects may be incompatible claims, the relationship
between them, the authority boundary that allowed both to appear, or the
question that asks how to reconcile them.

The central hypothesis to test is therefore:

```text
Triggers explain why attention moved.
Targets explain what attention moved toward.
```

This formulation is useful only if it avoids collapsing target into trigger,
inquiry, selection, relevance, active context, or working state.

---

## Existing Authority That Constrains This Frontier

### Foundational Ontology

Seed remains claim-centric and evidence-bounded. Observations, evidence,
claims, facts, relationships, projections, assessments, recommendations,
decisions, operators, questions, goals, policy, authority, explanation,
capabilities, and handoffs already have settled or partially settled roles.

An attention target must not silently become truth, evidence, authority,
priority, recommendation, action, or execution. A thing can receive attention
without being true, important, actionable, authorized, or safe to mutate.

### Attention Trigger Frontier

The trigger frontier characterizes a trigger as a candidate explanation for why
something moved from available, latent, or merely represented into active focus.
It explicitly leaves open whether goals, needs, gaps, questions, failures, and
burdens are triggers, acquisition origins, inquiry objects, or some mixture.

This document accepts that uncertainty and asks the downstream question:

```text
What is the something that becomes active?
```

### Selection And Attention Frontier

The selection and attention frontier distinguishes attention as actual focus
from selection, relevance, priority, frontier, gap, and tension. This document
must preserve that boundary. A target is not selected merely because it exists,
and selection rationale is not identical to target identity.

A possible target can be relevant but unattended. A current target can later be
rejected as irrelevant. Attention target language must therefore avoid becoming
a relevance system.

### Inquiry Frontier

The inquiry frontier characterizes inquiry as active or preserved pursuit of
unresolved understanding. If inquiry is pursuit, then an inquiry usually appears
to need an object of pursuit. But it is not settled whether that object should
be called an attention target, an inquiry object, a question, a tension, a gap,
or a frontier.

This frontier treats inquiry as a neighboring concept, not a subsystem to be
designed.

### Operations Frontier

The operations frontier preserves vocabulary for what happens to represented
knowledge without promoting every verb into a runtime operation. Target language
faces the same risk. `Attend to`, `focus on`, `inspect`, `pursue`, `resume`, and
`promote` may describe participant behavior without requiring a new operation
kind.

### Capability Self-Acquisition Readiness Audit

The readiness audit found the acquisition starting object unresolved. Candidate
origins included goals, needs, gaps, tensions, questions, repeated failures,
operator burden, and frontiers. Attention target language may help explain why
these candidates recur, but it must not assert a capability acquisition
lifecycle or engine.

---

## Method

This investigation uses four tests:

1. **Object test**: does the candidate name what attention is about, rather
   than why attention moved?
2. **Separability test**: can the candidate receive attention without being the
   trigger, and can it trigger attention without being the target?
3. **Non-collapse test**: does target language avoid becoming inquiry,
   selection, relevance, priority, authority, active context, or working state?
4. **Usefulness test**: does target language explain recurring examples better
   than existing vocabulary alone?

If a candidate fails the object test, it may be a trigger, condition, rationale,
or evidence rather than a target. If it fails the non-collapse test, a separate
`attention target` term may not be worth preserving.

---

## Candidate Attention Target Inventory

The prompt supplied these candidates:

```text
goal
need
gap
question
tension
contradiction
ambiguity
frontier
capability deficiency
unresolved failure
recommendation
risk
anomaly
claim
relationship
assessment
operator request
```

The investigation adds several candidate refinements:

```text
operator intent
unmet goal
unresolved need
evidence gap
support gap
scope gap
incompatible claims
ambiguous identity
ambiguous topology
uncertain relationship
failure pattern
automation opportunity
burdened operator activity
unsafe next move
missing bridge
capability acquisition question
selection candidate
active context element
working-state item
```

The refined list is intentionally over-inclusive. Some entries are likely
ordinary descriptions rather than ontology terms. Some may be targets only after
another object frames them.

---

## Candidate Target Evaluation

| Candidate | Target reading | Counterpressure | Current characterization |
| --- | --- | --- | --- |
| Goal | Attention can focus on the desired outcome to be satisfied or clarified. | A request may trigger attention before any goal is represented; a goal can remain latent. | Strong target candidate when the outcome itself is under focus. Not universal. |
| Need | Attention can focus on a requirement that must be satisfied. | Need may be inferred only after attention has moved to a request, failure, or gap. | Strong target candidate, especially downstream of request or failure. |
| Gap | Attention can focus on missing evidence, understanding, capability, support, or bridge. | Gap is relational and depends on a frame such as goal, question, claim, or capability. | Strong but frame-dependent target candidate. |
| Question | Attention can focus on a question to answer or preserve. | A question can also trigger attention and can be the inquiry form itself. | Strong target and inquiry-object candidate; boundary remains blurred. |
| Tension | Attention can focus on unresolved pressure between concepts, claims, scopes, or needs. | Tension often explains why attention moved rather than what concrete object is inspected. | Strong target when the tension is itself the subject of exploration. |
| Contradiction | Attention can focus on incompatibility between claims. | The actual targets may be the claims, support, scope, or relationship rather than the contradiction label. | Better treated as a target complex: contradiction plus implicated claims and supports. |
| Ambiguity | Attention can focus on uncertain meaning, identity, scope, or topology. | Ambiguity can be a trigger; the target may be the thing whose identity or scope is ambiguous. | Strong target candidate when ambiguity is the object being resolved. |
| Frontier | Attention can focus on a named unresolved area. | Frontier may be a container or sustained condition, not a single object. | Likely collection or persistence form of targets rather than primitive target. |
| Capability deficiency | Attention can focus on missing or inadequate capability. | Deficiency requires evidence and authority boundaries; not every lack is acquisition-relevant. | Strong capability-facing target candidate, but not acquisition authorization. |
| Unresolved failure | Attention can focus on a failure event or repeated pattern. | Failure may merely trigger attention toward unmet goal, need, or capability deficiency. | Target only when failure pattern itself is under investigation. |
| Recommendation | Attention can focus on a surfaced recommendation. | Recommendation may be ignored; attending to it does not make it authority. | Target candidate when evaluating or deciding whether to accept it. |
| Risk | Attention can focus on potential harm, unsafe next move, or exposure. | Risk can also trigger attention; risk object may be the threatened claim, action, or context. | Strong target candidate when risk itself is being assessed. |
| Anomaly | Attention can focus on deviation from expected pattern. | The target may become the underlying cause, baseline, evidence, or affected entity. | Often initial target that may hand off attention to deeper targets. |
| Claim | Attention can focus on a proposition, especially its support, scope, confidence, or contradiction. | Claim attention must not become truth arbitration without evidence and authority. | Strong foundational target candidate. |
| Relationship | Attention can focus on relation identity, direction, support, or ambiguity. | Relationship may be projected and scope-bound; attention should not over-promote it. | Strong target candidate in ontology and graph work. |
| Assessment | Attention can focus on an evaluation, confidence, caveat, recommendation, or status. | Assessment is not evidence or authority by itself. | Target candidate when evaluating evaluation quality or consequences. |
| Operator request | Attention can focus on the request text, intent, constraints, or response obligation. | Request often triggers attention and wraps goal, question, need, or command. | Both strong trigger and possible target, but usually decomposes into intent, question, goal, or need. |
| Operator intent | Attention can focus on what the operator is trying to achieve. | Intent may be underdetermined and must not be invented beyond evidence. | Useful target refinement for request cases. |
| Incompatible claims | Attention can focus on the specific claims in conflict. | Conflict may be apparent because of scope or language mismatch. | Strong target refinement for contradiction cases. |
| Failure pattern | Attention can focus on recurrence, not just isolated failure. | Pattern recognition requires evidence; recurrence may amplify rather than define target. | Useful target when repeated failure is the object of diagnosis. |
| Automation opportunity | Attention can focus on a potential bridge from burden to capability. | Opportunity is not need, adoption, or authority. | Useful derived target after burden is visible. |
| Active context element | Attention can focus on an item currently included in context. | Context inclusion is not identical to attention. | Usually working-state/context vocabulary is enough. |
| Working-state item | Attention can focus on something preserved for continuation. | Working state includes constraints and next moves, not only targets. | Neighboring concept, not synonym. |

---

## Trigger Versus Target

The minimal model under test is:

```text
Trigger
    ↓
Attention
    ↓
Target
```

This model survives as an explanatory sketch, but only if treated as
many-to-many and context-relative.

### Are triggers and targets distinct?

They are often distinct:

```text
repeated failure
    triggers attention toward
unmet need or capability deficiency
```

```text
operator burden
    triggers attention toward
automation opportunity or missing bridge
```

```text
contradiction
    triggers attention toward
incompatible claims, support, or scope
```

The distinction is useful because it prevents a cause of focus from being
mistaken for the object that focus should inspect.

### Can the same object be both?

Yes. A question can trigger attention and also be the object pursued. A risk can
trigger attention and also be the object assessed. An operator request can make
itself the immediate attended object before it is decomposed into goal, need,
question, constraint, or command.

This dual role is why `attention target` cannot be defined merely as "not a
trigger." The safer distinction is role-relative:

```text
trigger role
    why focus moved in this episode

target role
    what focus is about in this episode
```

The same represented thing may occupy both roles in one episode or different
roles across episodes.

### Can multiple triggers activate one target?

Yes. A capability deficiency may receive attention because an operator request
failed, the failure repeated, operator burden became visible, and a risk was
recognized. Treating those as one trigger would hide provenance and weaken the
explanation.

### Can one trigger activate many targets?

Yes. A contradiction can activate attention toward multiple claims, their
evidence, the relationship between them, the scope boundary, a projection rule,
and a response caveat. A single weather request can activate the request, the
operator's goal, the need for current weather data, capability support, and
response constraints.

Therefore a target model must not assume one trigger produces one target.

---

## Critical Examples

### Example 1: Weather Request

Operator asks:

```text
Tell me the weather.
```

Likely trigger:

```text
operator request
```

Possible attended targets, in sequence or in parallel:

```text
request text
operator intent
weather information goal
current-location or specified-location question
need for current weather evidence
capability support for weather lookup
response obligation and caveat boundary
```

The request is both trigger and immediate target. But after interpretation,
attention likely moves toward the operator's goal and the information need. If
current weather capability is unavailable, attention may move again toward a
capability gap. That gap is not necessarily the original target; it is a target
created or exposed during attempted satisfaction.

Current finding:

```text
Trigger: operator request.
Primary target: operator's weather-information need or goal.
Secondary possible target: capability gap if support is missing.
```

This example argues against treating `request`, `goal`, `need`, and `gap` as
rival universal targets. They can be different layers of the same attention
episode.

### Example 2: Repeated Failure

Seed repeatedly fails to satisfy a request.

Possible trigger:

```text
repeated failure
```

Possible targets:

```text
failure pattern
unresolved operator need
unmet goal
missing capability
missing bridge
bad interpretation
unsafe or unavailable execution path
```

The failure itself is a target only if the investigation is about why the
failure recurs. If the work instead asks what remains unsatisfied, the target is
the unmet need or goal. If the work asks what Seed cannot currently do, the
target is capability deficiency or missing bridge.

Current finding:

```text
Repeated failure is usually a trigger and evidence source.
It becomes the target only when the failure pattern itself is investigated.
```

### Example 3: Contradiction Discovery

Two claims appear incompatible.

Possible trigger:

```text
contradiction or apparent contradiction
```

Possible targets:

```text
claim A
claim B
relationship between claims
supporting evidence
scope mismatch
confidence boundary
projection or wording that made them appear incompatible
```

The contradiction label may be too coarse to be the whole target. Attention may
need to inspect the implicated claims and their support without prematurely
settling truth.

Current finding:

```text
Contradiction can be both trigger and target complex.
The concrete targets are usually the incompatible claims, scopes, relationships,
and supports.
```

### Example 4: Operator Burden

Operator repeatedly performs the same task.

Possible trigger:

```text
visible or reported operator burden
```

Possible targets:

```text
burdened activity
automation opportunity
missing deterministic utility
capability need
operator bridge
workflow friction
```

The burden itself may initially receive attention, especially if the task is to
understand operator work. If the question becomes whether Seed needs better
support, the target shifts to automation opportunity, capability need, or
missing bridge. None of these imply adoption or implementation.

Current finding:

```text
Burden is often the trigger.
The target is often the burdened activity or possible bridge, not an acquisition
engine.
```

### Example 5: Architectural Discovery

Storage ambiguity repeatedly appears.

Possible triggers:

```text
ambiguity
recurrence
projection confusion
unsafe interpretation
```

Possible targets:

```text
ambiguous storage identity
mount versus storage topology
relationship vocabulary
identity uncertainty
topology understanding
projection boundary
```

The target is not merely `ambiguity` in the abstract. It is the ambiguous
identity, topology, or relationship boundary that prevents safe interpretation.
If recurrence persists, the area may become a frontier.

Current finding:

```text
Ambiguity can trigger attention.
The target is the specific uncertain identity, topology, or relationship.
A frontier may preserve the sustained unresolved area.
```

---

## Relationship To Inquiry

A simple downstream sketch is:

```text
Attention
    ↓
Inquiry
```

This sketch is useful but incomplete.

### Does inquiry require an attention target?

Active inquiry appears to require some object or frame of pursuit. The object
may be a question, tension, gap, claim, relationship, ambiguity, or failure
pattern. Without any target-like object, inquiry becomes indistinguishable from
general alertness or passive availability.

However, a formal `attention target` term may not be required if `inquiry
object`, `question`, `tension`, or `gap` already supplies the object.

### Can inquiry exist without one?

Preserved inquiry can exist without current attention in the sense that a
documented question or frontier may remain dormant. Active inquiry without any
object appears incoherent. What can exist without current attention is a stored
inquiry candidate, not active pursuit.

### Is the inquiry object itself the target?

Often yes. In an inquiry episode, the inquiry object and attention target may be
two names for the same role:

```text
what inquiry pursues
    ≈
what attention is about
```

But they are not perfect synonyms. Attention can focus on a concrete claim,
request, or risk before an inquiry is formed. Inquiry adds pursuit structure:
question, scope, method, evidence expectations, preservation, and authority
boundaries.

Current finding:

```text
Attention target is a plausible pre-inquiry or within-inquiry role.
Inquiry object may be the more precise term once pursuit is structured.
```

---

## Relationship To Capability Acquisition

The model to evaluate is:

```text
Attention Target
    ↓
Gap Investigation
    ↓
Acquisition Candidate
```

This model is useful as a descriptive possibility, not as a lifecycle.

### Where the model helps

It explains why acquisition-origin candidates are plural. Attention might first
land on a request, then an unmet need, then a capability gap, then a candidate
capability. In that sequence, `goal`, `need`, `gap`, `failure`, and `burden` are
not rival universal origins. They are possible targets at different depths.

Example:

```text
operator request
    triggers attention toward
unmet information need
    exposes
capability support gap
    motivates
candidate capability consideration
```

### Where the model overreaches

The model becomes unsafe if it implies that every attended gap should produce an
acquisition candidate. Repository authority already separates need, gap,
capability, recommendation, adoption decision, authority, command, and
execution. Attention does not authorize acquisition. A target does not become a
need merely because it is attended. A gap does not become an adoption decision
because it is visible.

### Current acquisition finding

A safer formulation is:

```text
Some acquisition investigations may begin after attention lands on a
capability-relevant target.
```

The target may be an unmet need, repeated failure, operator burden, missing
bridge, capability deficiency, or unsafe next move. But capability acquisition
still requires evidence, scope, authority, candidate evaluation, adoption
boundaries, and execution constraints outside this frontier.

---

## Target Versus Working State

Working state preserves continuation position: what must remain active, known,
unresolved, constrained, or next for safe resumption. An attention target may be
part of working state, but working state is broader.

### Is a target part of working state?

Often yes. If current work must continue safely, the current target should be
preserved in working state or active context. For example, a frontier handoff may
need to preserve the contradiction being explored or the gap being investigated.

### Is working state a collection of active targets?

No. Working state can include:

```text
current target
selection rationale
constraints
authority boundaries
known evidence
excluded paths
next safe move
open risks
handoff position
```

Only some of these are targets. Others explain how to continue attending safely.

### Can targets exist without entering working state?

Yes. A fleeting target may receive attention during a local episode and never be
preserved. A dormant candidate may be target-like in retrospect but not enter
working state until selected for continuation. Conversely, working state may
preserve a deferred issue that is not the current target.

Current finding:

```text
Attention target is narrower than working state.
Working state may preserve targets, but also preserves context, constraints,
rationale, and continuation safety.
```

---

## Target Versus Frontier

A frontier is a named unresolved area preserved for further investigation. It
may contain targets, result from targets, or become a target.

### Is a frontier a target?

Sometimes. A participant can attend to a frontier as the object of work, as this
document attends to the attention target frontier. In that case the frontier
label is the target of a documentation episode.

### Is a frontier a collection of targets?

Often. A frontier may collect questions, tensions, candidate concepts,
examples, unresolved boundaries, evidence gaps, and future reconciliation tasks.
The frontier is then a container or preservation form rather than a single
object.

### Is a frontier a sustained attention condition?

Yes, this may be the strongest reading. A frontier marks a region where
attention has been sustained or preserved because resolution is not yet safe.
It can become dormant, resumed, narrowed, reconciled, or rejected. Its existence
does not imply current priority.

Current finding:

```text
A frontier is not identical to an attention target.
It is often a preservation structure for sustained, recurring, or resumable
attention around multiple targets.
```

---

## Target Versus Selection, Relevance, And Active Context

### Target versus selection

Selection chooses, includes, excludes, orders, or narrows candidates. Attention
target names what current focus is about. Selection may determine a target, and
a target may force later selection, but neither contains the other.

A selected item may remain unattended. An attended item may not have been
formally selected. A target may emerge through interruption, surprise,
contradiction, or operator request before selection rationale exists.

### Target versus relevance

Relevance describes relationship to a goal, question, context, or need. A thing
can be relevant without receiving attention. A thing can receive attention and
later prove irrelevant. Therefore target language must not become a relevance
classification.

### Target versus active context

Active context is the material available or composed for current work. An
attention target may be represented in active context, but active context also
contains background, constraints, evidence, caveats, and nearby objects. A
context item is not automatically a target.

Current finding:

```text
Target is focus-aboutness.
Selection is choice or inclusion.
Relevance is relation to purpose.
Active context is composed support for current work.
```

---

## Potential Finding Tested

Hypothesis:

```text
Triggers explain why attention moved.
Targets explain what attention moved toward.
```

### What survives

The framing survives as a useful distinction. It explains why repeated failure,
burden, contradiction, and request can activate attention while the attended
object may be need, goal, claim, relationship, capability deficiency, or
ambiguity. It also prevents acquisition-origin candidates from being collapsed
into one starting object.

### What does not survive

The framing is too simple if read as a linear pipeline. Triggers and targets are
roles, not necessarily different entities. One thing can be both. Multiple
triggers can activate one target. One trigger can activate many targets. Targets
can shift during interpretation. Some targets are complexes rather than single
objects.

### Revised framing

A safer formulation is:

```text
A trigger is a role an object or condition plays in explaining why focus moved.
A target is a role an object, relation, gap, question, or area plays as what
focus is about.
```

Both roles are episode-relative. Neither role implies truth, authority,
priority, action, acquisition, or implementation.

---

## Consolidated Findings

1. Attention targets appear meaningful as an exploratory concept, but not as a
   reconciled ontology object.
2. The strongest target candidates are goal, need, gap, question, tension,
   ambiguity, claim, relationship, capability deficiency, failure pattern,
   risk, anomaly, operator intent, and frontier-as-container.
3. Operator request is usually a trigger and immediate target wrapper; it often
   decomposes into intent, goal, question, need, constraint, or command.
4. Contradiction is often a trigger and a target complex; the concrete targets
   are usually incompatible claims, their support, scope, and relationship.
5. Repeated failure is usually a trigger and evidence source; it is a target
   when the failure pattern itself is investigated.
6. Operator burden is usually a trigger; targets may include burdened activity,
   missing bridge, automation opportunity, or capability need.
7. Ambiguity can be trigger or target; the more concrete target is often
   ambiguous identity, topology, scope, or relationship.
8. Trigger and target are distinct roles, not mutually exclusive object kinds.
9. One object can be both trigger and target in the same episode.
10. Multiple triggers can activate one target, and one trigger can activate many
    targets.
11. Inquiry appears to require a target-like object for active pursuit, but
    `inquiry object` may be the better term once pursuit is structured.
12. Capability acquisition may begin after attention lands on a
    capability-relevant target, but attention target is not acquisition origin,
    authority, candidate selection, adoption, or execution.
13. Working state can preserve attention targets, but is broader than a
    collection of targets.
14. A frontier may be a target, a collection of targets, or a sustained
    attention preservation structure.
15. Target differs from selection, relevance, and active context: focus-aboutness
    is not choice, relation-to-purpose, or context inclusion.
16. Implementation would be premature because target boundaries remain blurred
    with inquiry object, working state, frontier, selection, relevance, and
    capability acquisition.

---

## Required Tensions Preserved

| Tension | Why it remains unresolved |
| --- | --- |
| Trigger vs target | The distinction is useful, but the same object can occupy both roles. |
| Target vs inquiry object | Active inquiry seems to need a target-like object, but inquiry object may be the more precise term once pursuit is structured. |
| Target vs working state | Working state may preserve targets, but also preserves constraints, evidence, rationale, and continuation position. |
| Target vs frontier | A frontier can be a target, container of targets, or sustained attention condition. |
| Goal vs target | A goal can be attended, but may also be inferred from a request or remain latent. |
| Need vs target | A need can be attended, but may be discovered only after attention moves elsewhere. |
| Gap vs target | A gap can receive attention, but it is relational and requires a frame. |
| Contradiction vs target | Contradiction can trigger attention, but concrete targets are often claims, support, scope, or relationship. |
| Target vs selection | Selection can determine focus, but target names what focus is about, not the act of choosing. |
| Target vs relevance | Relevant things can remain unattended, and attended things can prove irrelevant. |
| Target vs active context | Active context can contain targets plus non-target support material. |
| Request vs target | A request can be an immediate target and trigger, but often decomposes into intent, goal, need, question, or constraint. |
| Failure vs target | Failure may be the target only when the failure pattern itself is under investigation. |
| Burden vs target | Burden may activate attention toward a burdened activity, bridge, opportunity, or capability need. |
| Risk vs target | Risk can be both why attention moves and what is assessed. |
| Anomaly vs target | Anomaly may be the initial target, but attention may shift to baseline, cause, evidence, or affected entity. |
| Capability deficiency vs target | A deficiency can be attended without becoming an acquisition candidate or authorized adoption. |

---

## Why Implementation Would Be Premature

Implementation would be premature for several reasons:

- attention target is not a reconciled ontology object;
- target identity is episode-relative and may shift during interpretation;
- trigger and target roles can be occupied by the same object;
- target complexes may include claims, relationships, evidence, scope, risks,
  and questions;
- target detection could easily become a planner, scheduler, prioritization
  system, recommendation system, or context algorithm;
- inquiry object vocabulary may already cover structured pursuit cases;
- working state and active context already preserve continuation needs and
  should not be replaced by an attention system;
- capability acquisition boundaries require evidence, authority, adoption, and
  execution constraints not supplied by attention target language;
- frontiers are exploratory preservation structures, not runtime queues.

The safe outcome is preserved ontology pressure, not machinery.

---

## Candidate Future Questions

Future documentation-only work could ask:

1. Is `attention target` needed as a term, or can `inquiry object`, `working
   state item`, `active context`, and existing goal/need/gap vocabulary cover the
   same ground?
2. Should handoff templates preserve what attention is currently about,
   distinct from why attention moved?
3. When a request is both trigger and target, what vocabulary best preserves the
   transition from request text to intent, goal, need, or question?
4. Are contradictions best represented as targets, target complexes, or triggers
   that point toward claims and support?
5. Can capability-relevant targets be discussed without creating acquisition
   lifecycle expectations?
6. Does a frontier preserve a target history, a current target, or an unresolved
   region independent of current attention?
7. Is target language helpful for explaining working state, or does it duplicate
   active context vocabulary?
8. What is the smallest documentation vocabulary needed to avoid confusing why
   focus moved with what focus is about?

---

## Final Characterization

Attention targets appear meaningful because Seed repeatedly distinguishes
between what exists, what becomes active, and what active work is about. The
concept helps explain why triggers such as request, burden, failure,
contradiction, anomaly, and ambiguity do not always name the object that should
be inspected.

A provisional characterization is:

```text
An attention target is a candidate role for the object, relation, gap, question,
claim, need, risk, ambiguity, or unresolved area that active focus is about in a
particular attention episode.
```

This characterization remains exploratory. Target is a role, not a settled
object kind. It may be occupied by a goal, need, gap, question, claim,
relationship, failure pattern, risk, anomaly, request, or frontier. It may be a
single object or a complex. It may be identical to the trigger, downstream of the
trigger, or one of several objects activated by the trigger.

The strongest current distinctions are:

```text
trigger
    why focus moved

target
    what focus is about

inquiry object
    what structured pursuit of unresolved understanding is about

selection
    inclusion, exclusion, ordering, or choice among candidates

relevance
    relation to a purpose, question, need, or context

active context
    composed support available for current work

working state
    bounded continuation position preserving active target, constraints,
    evidence, rationale, and next safe moves

frontier
    preserved unresolved region that may contain, become, or sustain targets

capability acquisition
    downstream possibility requiring gap evidence, authority, adoption
    boundaries, and execution constraints
```

Implementation would be premature. The correct current outcome is to preserve
attention targets as a frontier pressure and continue avoiding collapse among
trigger, target, inquiry object, selection, relevance, active context, working
state, frontier, and capability acquisition.
