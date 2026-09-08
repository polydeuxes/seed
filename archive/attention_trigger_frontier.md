---
doc_type: frontier
status: exploratory
domain: attention trigger ontology
defines:
  - attention trigger frontier
  - candidate attention trigger
  - attention trigger boundary
  - attention inquiry boundary
  - attention selection boundary
  - attention priority boundary
  - acquisition origin trigger tension
depends_on:
  - selection_and_attention_frontier.md
  - inquiry_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - operations_frontier.md
  - capability_self_acquisition_readiness_audit.md
  - capability_gap_and_operator_bridge_reconciliation.md
  - capability_need_acquisition_reconciliation.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - selection_rationale_vocabulary.md
  - selection_rationale_reconciliation.md
  - context_composition_vocabulary.md
  - context_composition_reconciliation.md
  - continuation_context_and_working_state_reconciliation.md
  - active_context_and_working_set_reconciliation.md
  - handoff_consumption_activation_reconciliation.md
  - handoff_template_and_continuation_protocol_reconciliation.md
---

# Attention Trigger Frontier

## Purpose

This document characterizes a documentation-only exploratory frontier exposed by
recent work on inquiry, selection, attention, working state, handoff lineage, and
capability self-acquisition readiness.

It investigates the question:

```text
What causes something to receive attention?
```

More specifically:

```text
What transforms a thing from existing into actively explored?
```

The document tests whether `attention trigger` is a meaningful architectural
concept. It does not assume that attention triggers exist as formal ontology
objects. It records evidence for and against preserving the concept for later
reconciliation.

This is ontology discovery only. It does not design planners, attention systems,
prioritization systems, recommendation systems, scheduling systems, acquisition
engines, workflow systems, runtime behavior, schemas, read models, routes,
provider ranking, tool selection, context algorithms, projection mutation, event
appends, or tests.

Repository authority wins over this document. Existing reconciliations remain
authoritative for their settled boundaries. Existing frontiers remain
exploratory and not implementation-ready.

---

## Background Finding

The capability self-acquisition readiness audit identified a central unresolved
tension:

```text
What is the acquisition starting object?
```

Candidate origins included:

```text
goal
need
gap
tension
question
repeated failure
operator burden
frontier
```

The audit did not reconcile these candidates. This frontier tests a possible
alternative explanation:

```text
Maybe these are not all acquisition origins.
Maybe many of them are attention triggers.
```

That hypothesis must not be accepted prematurely. A `goal`, `need`, or `gap`
may still be an acquisition origin in some contexts. A `request` may be the real
origin in others. A `contradiction` may be the object of inquiry rather than a
trigger. A `frontier` may represent sustained attention rather than the cause of
attention.

The safest current question is narrower:

```text
When something becomes active, what made it active?
```

---

## Existing Authority That Constrains This Frontier

### Foundational Ontology

Seed remains claim-centric. Observations, evidence, claims, facts,
relationships, projections, assessments, recommendations, decisions, operators,
questions, goals, policy, authority, explanation, capabilities, and handoffs
already have settled or partially settled roles.

An attention trigger must not silently become truth, evidence, authority,
policy, decision, command, execution, priority, or recommendation. Something can
trigger attention without being true, important, authorized, actionable, or safe
to pursue.

### Selection And Attention Frontier

The selection and attention frontier already distinguishes multiple neighboring
concepts:

```text
unknown
gap
tension
frontier
priority
selection
attention
relevance
```

It characterizes attention as actual focus and priority as normative ordering.
It also finds that gaps and tensions can exist without becoming frontiers, and
that frontiers can exist without being current priority.

This document does not replace that frontier. It asks a more specific upstream
question:

```text
If attention is actual focus, what caused actual focus to move here?
```

### Inquiry Frontier

The inquiry frontier characterizes inquiry as active or preserved pursuit of
unresolved understanding. It distinguishes tension, question, gap, finding,
frontier, working state, and inquiry lineage without formalizing an inquiry
runtime.

This document treats inquiry as a close neighbor. If inquiry is active pursuit,
attention may be the activation condition that makes pursuit possible. But this
is not settled. Inquiry may itself create attention, attention may create
inquiry, or both may be views of the same transition.

### Handoff And Continuation Lineage Frontier

Handoff work shows that continuation can fail even when information is preserved
if active position, unresolved tensions, selection rationale, navigation intent,
working state, or next safe move is lost.

That finding makes attention more than a private mental event. Something can be
available in the repository but not active in continuation. The distinction
between availability and activation is essential to any trigger concept.

### Operations Frontier

The operations frontier asks whether Seed needs vocabulary for what happens to
represented knowledge. Attention movement can be described operationally:

```text
notice
activate
select
promote
focus
defer
resume
```

This document does not promote those verbs into operations. It only observes
that attention movement looks event-like enough to raise an ontology question.

### Capability Self-Acquisition Readiness Audit

The capability audit found that Seed is ontology-mostly-present for future
capability self-acquisition but not architecturally or implementation ready. The
missing center is the bridge from unresolved goal, tension, gap, or need into an
evidence-backed capability gap and authorized adoption decision.

This document tests whether the missing center might partly involve attention:
before acquisition can begin, something must receive active consideration.
However, attention alone cannot justify acquisition, authority, adoption,
execution, or implementation.

### Architectural Status

Architectural status currently points toward bounded implementation cleanup and
warns against implementing unreconciled frontier ontologies, planners, workflow
systems, selection engines, response engines, acquisition logic, or runtime
routing.

Therefore this document must remain a frontier characterization. It may name
candidate triggers, distinctions, and tensions, but it must not prescribe a
system that detects, ranks, schedules, or acts on them.

---

## Method

This investigation reviewed the requested authoritative references and tested
the recurring transition:

```text
existing thing
    -> attended thing
        -> active inquiry / working state / frontier / acquisition consideration
```

The investigation looked for cases where a thing already existed but was not yet
active, then became active because some condition changed.

The analysis used three tests:

1. **Activation test**: did the candidate help explain why the thing became
   active rather than merely present?
2. **Non-collapse test**: does treating the candidate as a trigger avoid
   collapsing it into truth, authority, priority, inquiry, selection, or
   acquisition?
3. **Counterexample test**: can the candidate exist without triggering
   attention, or can attention move without that candidate?

If a candidate can exist without attention, it may still be a trigger family but
not a sufficient cause. If attention can move without it, it is not a necessary
cause.

---

## Initial Candidate Trigger Inventory

The prompt supplied the following candidates:

```text
goal
need
gap
tension
contradiction
ambiguity
uncertainty
question
repeated failure
operator burden
operator request
frontier
recommendation
prediction
risk
anomaly
```

The investigation adds several candidate refinements that appear necessary for
non-collapse:

```text
explicit instruction
constraint violation
authority boundary
missing support
surprise
recurrence
salience
continuation loss
handoff activation failure
external evidence arrival
federated challenge
proximity to current work
available capacity
unsafe next move
opportunity
commitment
```

Not all of these should become ontology terms. Some are ordinary explanations,
some are conditions, some are rationales, and some are consequences. The list is
intentionally over-inclusive so the frontier can reject candidates rather than
only collect them.

---

## Candidate Trigger Evaluation

| Candidate | Trigger reading | Counterpressure | Current characterization |
| --- | --- | --- | --- |
| Goal | A desired outcome can make some object relevant enough to attend. | Goals can remain idle, vague, impossible, or unauthorized. | Strong external or internal trigger candidate, but not sufficient by itself. |
| Need | A requirement can direct attention to satisfaction paths or missing support. | Needs may be known but deferred; some needs are inferred only after attention has already moved. | Strong candidate, but sometimes downstream of attention. |
| Gap | Missing evidence, capability, or understanding can draw attention. | Many gaps are known and ignored; a gap requires framing relative to a goal, question, or authority. | Strong trigger candidate when coupled to consequence, recurrence, or active work. |
| Tension | Incompleteness, surprise, inconsistency, or unresolved boundary pressure can draw attention. | Tensions can remain dormant; some attention begins from request rather than tension. | Very strong trigger candidate for inquiry, but not identical to inquiry. |
| Contradiction | Incompatible claims can demand reconciliation. | Apparent contradiction may be low consequence, already caveated, or outside current scope. | Strong internal trigger candidate, especially when it threatens truth, projection, or response integrity. |
| Ambiguity | Multiple possible meanings or scopes can require attention before safe continuation. | Ambiguity can be tolerated if consequence is low. | Strong trigger candidate when ambiguity blocks interpretation, navigation, or action. |
| Uncertainty | Unknown confidence or incomplete support can draw attention. | Uncertainty is everywhere; by itself it is too broad. | Weak alone; stronger when paired with risk, decision pressure, or inquiry. |
| Question | A directed ask can activate exploration. | Questions may be stored, unanswered, rhetorical, or low priority. | Strong trigger candidate and possible inquiry object; boundary remains unresolved. |
| Repeated failure | Recurrence can transform isolated failure into a pattern worth attending. | A single failure may already trigger attention; repeated failure may be evidence rather than trigger. | Strong historical trigger candidate; repetition amplifies attention and can create need/gap evidence. |
| Operator burden | Manual repeated work can draw attention to possible capability need. | Burden may remain invisible unless reported or observed. | Strong bridge candidate from human work to capability attention; not automatically acquisition. |
| Operator request | A direct request can make an object active immediately. | The request may express a goal, question, need, command, or constraint, so `request` may be wrapper rather than root. | Strong external trigger candidate; often the clearest attention mover. |
| Frontier | A named unresolved area can preserve attention over time. | A future frontier can exist without current attention; frontier may be result of attention, not trigger. | Likely sustained-attention artifact more than primitive trigger, though it can trigger later resumption. |
| Recommendation | A surfaced suggestion can redirect attention. | Recommendation is not authority and may be ignored. | Trigger candidate when surfaced to an actor; otherwise only latent guidance. |
| Prediction | A forecast can draw attention to expected future state. | Prediction may be speculative or low consequence; prediction is not observation. | Trigger candidate when linked to risk, opportunity, or preparation. |
| Risk | Potential harm can move attention even before failure. | Risk can be accepted, deferred, or outside authority. | Strong trigger candidate, but attention must not imply action. |
| Anomaly | A surprising deviation can cause attention. | Anomaly depends on baseline and may be noise. | Strong trigger candidate when baseline and consequence are credible. |
| Explicit instruction | An operator or authority can require attention to a subject. | Instruction may be invalid, impossible, or unauthorized in scope. | Strong trigger candidate; must remain distinct from permission to execute. |
| Constraint violation | Breach of documented boundary can draw attention. | Apparent violation may be misread or already accepted exception. | Strong internal trigger candidate, especially for architecture and policy boundaries. |
| Missing support | Unsupported claim or capability assertion can draw attention. | Missing support may be known but irrelevant. | Trigger candidate when support is needed for response, adoption, or authority. |
| Surprise | Unexpected result can draw attention before a question is articulated. | Surprise is participant-relative and may not be represented. | Useful pre-question trigger candidate, but difficult to formalize. |
| Recurrence | Repetition converts isolated events into patterns. | Recurrence is an amplifier, not always a source. | Better treated as trigger amplifier or historical trigger family. |
| Salience | Something stands out due to prominence, frequency, or presentation. | Salience can be misleading and not important. | Trigger candidate for actual attention, but dangerous if confused with priority. |
| Continuation loss | A later participant cannot resume safely. | Loss may be diagnosed only after attention has moved. | Strong trigger candidate for handoff and working-state inquiries. |
| External evidence arrival | New evidence can make a dormant issue active. | Evidence can arrive unnoticed or be irrelevant. | Strong external trigger candidate when evidence changes a live question. |
| Federated challenge | Another Seed or external participant disputes or extends a claim. | Challenge may lack authority or support. | Candidate external trigger for contradiction, provenance, and authority inquiries. |
| Proximity to current work | Adjacent issue receives attention because it blocks or shapes current work. | Proximity can cause scope creep. | Contextual trigger candidate; often explains low-priority attention. |
| Available capacity | A dormant topic may receive attention because capacity opens. | Capacity does not explain why that topic rather than another. | Enabling condition, not trigger by itself. |
| Unsafe next move | Attention shifts to the blocker that makes continuation unsafe. | Safety judgment may depend on policy and evidence. | Strong trigger candidate for continuation and architecture work. |
| Opportunity | A beneficial possibility can attract attention even without a failure. | Opportunity can become planning or recommendation if overdesigned. | Candidate trigger, especially for exploration; not acquisition authority. |
| Commitment | Prior promise, decision, or documented next step can reactivate attention. | Commitment may be superseded or unauthorized. | Historical/external trigger candidate; requires authority boundary. |

---

## Candidate Families Tested

### External Triggers

External triggers originate outside the currently active inquiry or working
state. Examples include:

```text
operator request
explicit instruction
imported evidence
federated challenge
new constraint
external deadline
operator report of burden
```

This family survives scrutiny only if `external` means external to the current
attention state, not necessarily external to Seed. An operator request is
external in a different way from imported evidence. A federated challenge is
external in a provenance sense. A policy update is external to an inquiry but may
be internal to the repository.

External triggers are strong explanations for sudden attention movement. They do
not by themselves settle priority, truth, or authority. A request can be refused,
clarified, deferred, or answered without acquisition. Imported evidence can be
ignored if unsupported or irrelevant.

### Internal Triggers

Internal triggers arise from represented or discovered conditions inside Seed's
knowledge, documentation, or working state. Examples include:

```text
contradiction
ambiguity
uncertainty
gap
missing support
constraint violation
anomaly
unsafe next move
```

This family is useful but broad. Internal triggers often require interpretation:
a contradiction must be recognized as incompatible, an anomaly must be measured
against a baseline, and a gap must matter relative to some goal, question,
claim, response, or authority boundary.

Internal triggers therefore may not be primitive causes. They may be recognized
conditions that become triggers only when coupled to salience, consequence,
current work, or operator question.

### Historical Triggers

Historical triggers depend on time, recurrence, or prior state. Examples include:

```text
repeated failure
recurring operator burden
recurring investigation
unresolved frontier
prior commitment
handoff continuation loss
stale capability support
```

This family is important because it explains why the same event may be ignored
once but attended after repetition. However, historical triggers are often
amplifiers rather than first causes. A repeated failure may trigger attention
because recurrence changes the object from `an event failed` to `a pattern of
failure exists`.

Historical triggers are especially relevant to capability acquisition readiness:
manual work, fallback use, and repeated failed resolution may produce evidence
that a durable need or gap should be represented. They still do not authorize
acquisition.

### Contextual Triggers

The supplied categories omit an important family: triggers created by active
context. Examples include:

```text
proximity to current work
blocker to next safe move
needed citation while writing
related frontier encountered during audit
context budget pressure
```

These explain why low-priority items may receive attention: they are near the
current work or block the next safe step. Contextual triggers also explain why
high-priority items may receive no attention: they are not in the active path,
capacity is absent, or a different blocker dominates.

### Salience Triggers

Another omitted family is salience. Something can receive attention because it
is prominent, frequent, surprising, visible in a summary, or repeatedly named.
This family is dangerous because salience can be projection artifact rather than
importance. Endpoint prominence investigations illustrate the general risk:
visibility can move attention before authority or importance is settled.

Salience is therefore a plausible trigger for actual attention, but it must be
kept separate from priority, truth, and value.

### Enabling Conditions That Are Not Triggers

Some candidates explain why attention can move but not why it moves to a
particular object. Examples include:

```text
available capacity
repository access
navigation path
sufficient context
operator availability
```

These are enabling conditions. They may be necessary in practice, but they are
not attention triggers unless they select or activate a particular object.

---

## Critical Example 1: User Request

Operator asks:

```text
Tell me the weather.
```

### What received attention?

Several objects may receive attention at different layers:

```text
operator request
    the immediate external event that becomes active

goal
    satisfy the operator's request for weather information

question
    what is the weather for the relevant location and time?

need
    obtain current weather data from an appropriate source

gap
    current working state lacks the requested weather answer

capability
    possible ability to retrieve weather data
```

### Which one triggered attention?

The strongest trigger is the operator request. The request causes the weather
subject to become active. The goal, question, need, and gap are interpretations
or decompositions of the request once attention has already moved.

However, the request is not the only meaningful object. If the operator says
only `weather`, a question may be needed to clarify location. If no weather data
capability is available, a capability gap may become active. If the request is
out of scope, authority or policy may receive attention.

### Finding

For a direct user request, attention appears to move first because of the
request. `Goal`, `need`, and `gap` are likely downstream framings, though they
can become secondary triggers when they expose missing support or unsafe
continuation.

This example argues against treating `goal` or `need` as universal acquisition
origins. A request can activate attention before a need is formally recognized.

---

## Critical Example 2: Repeated Failure

Seed repeatedly fails to satisfy a request.

### When did attention move?

There are at least three possible attention movements:

```text
first failure
    attention moves to the failed attempt

recognized recurrence
    attention moves from event to pattern

consequence framing
    attention moves from pattern to gap, need, or frontier
```

A single failure can trigger local attention: something went wrong now. Repeated
failure can trigger a different object: not merely `this attempt failed`, but
`this class of attempt repeatedly fails`.

### Did failure create attention?

Often yes, but only local attention. Failure draws attention to the immediate
breakdown. It may not create durable inquiry, frontier, or capability attention.

### Did repeated failure create attention?

Repeated failure appears to transform the attention object. The object is no
longer only an isolated failure; it becomes a pattern. That pattern may support a
capability gap, an operator bridge, a documentation audit, or a future frontier.

### Finding

Repeated failure is a strong historical trigger and amplifier. It may be one of
the clearest bridges from runtime or task-level experience into durable inquiry
or capability-gap consideration. It still does not automatically create a need,
justify acquisition, or authorize adoption.

---

## Critical Example 3: Operator Burden

Operator manually performs the same task repeatedly.

### What triggered attention?

Possible candidates:

```text
operator burden
recurring pattern
operator report
observed manual repetition
capability opportunity
missing automation support
```

The burden itself may exist before Seed attends to it. If the operator never
reports it and Seed does not observe it, the burden remains latent. Attention
moves when the burden becomes visible, represented, or connected to a current
question.

### Goal, pattern, or burden?

A goal may be inferred:

```text
reduce manual work
```

A pattern may be recognized:

```text
the same manual action recurs
```

A burden names the consequence for the operator:

```text
manual repetition costs time, effort, or reliability
```

These are not identical. The pattern is evidence-like. The burden is
value/consequence-like. The goal is desired change. Attention may be triggered
by any of them depending on what becomes visible first.

### Finding

Operator burden is a plausible attention trigger only after visibility. More
precisely, `visible recurring operator burden` is the stronger candidate. It can
activate capability inquiry, but it should not be collapsed into acquisition
priority or implementation authorization.

---

## Critical Example 4: Architectural Discovery

Storage topology repeatedly appears ambiguous.

### What transformed ambiguity into a frontier?

Ambiguity can exist passively. It becomes a frontier when it repeatedly blocks
safe interpretation, appears across investigations, threatens projection
accuracy, or cannot be resolved by existing authority.

Possible trigger chain:

```text
ambiguous storage evidence
    -> repeated interpretive uncertainty
        -> unsafe projection or claim boundary
            -> recognized architectural tension
                -> frontier characterization
```

The trigger may not be ambiguity alone. The stronger trigger is ambiguity plus
consequence:

```text
This ambiguity prevents safe claims about storage identity, mount identity, or
relationship projection.
```

### Finding

Architectural discovery suggests that frontiers are often produced by sustained
attention to a recurring unresolved tension. Ambiguity triggers attention when it
blocks interpretation or safe continuation. A frontier then preserves the active
edge rather than merely naming the original ambiguity.

---

## Critical Example 5: Contradiction

Two claims appear incompatible.

### What triggered attention?

Possible candidates:

```text
contradiction
uncertainty
risk
integrity concern
response safety concern
missing scope distinction
```

Contradiction is a strong trigger because Seed's claim-centered ontology depends
on preserving support, scope, and confidence. Incompatible claims can threaten
truth representation, response integrity, or projection safety.

However, contradiction often triggers attention through a more specific concern:

```text
Which claim is scoped incorrectly?
Which evidence supports each claim?
Is one claim false, stale, or over-promoted?
Can both be true under different scope?
What response caveat is required?
```

### Finding

Contradiction is a strong internal trigger. It may be the attention trigger, but
the inquiry object may become uncertainty, scope, evidence support, confidence,
or risk. Contradiction should not be collapsed into automatic rejection,
arbitration, or truth mutation.

---

## Attention Versus Inquiry

Candidate distinction:

```text
Attention:
    Something becomes active.

Inquiry:
    Active exploration occurs.
```

This distinction mostly survives scrutiny, with caveats.

### Why the distinction is useful

Attention explains activation:

```text
Why this thing now?
```

Inquiry explains pursuit:

```text
What unresolved understanding is being explored?
How does the investigation proceed, branch, preserve findings, or hand off?
```

A thing can receive attention without becoming a durable inquiry. For example, a
weather request receives attention and may be answered directly. A failure may
receive attention and be corrected locally without becoming an inquiry frontier.
An anomaly may be noticed and dismissed.

Conversely, inquiry likely requires attention. An inquiry that receives no
attention may exist only as preserved documentation or future frontier, not as
active exploration.

### Caveats

Attention and inquiry are not fully separable in practice. A question can both
trigger attention and constitute the initial inquiry object. A frontier can both
preserve inquiry and reactivate attention. During active work, attention may
move within inquiry as subquestions emerge.

### Current finding

The safest characterization is:

```text
Attention is activation of focus.
Inquiry is structured pursuit of unresolved understanding.
```

Attention can precede inquiry, occur inside inquiry, or resume inquiry. Inquiry
can generate new attention triggers as it exposes gaps, contradictions,
ambiguities, or risks.

---

## Attention Versus Selection

The selection and attention frontier already asks why one thing is selected
instead of another. This document narrows that to activation.

### Does selection create attention?

Sometimes. Selecting a document, frontier, evidence set, or next question can
make it active. Context selection can put information into the working set,
which makes attention more likely.

But selection can also occur without active attention. A future frontier can be
selected for preservation without being current work. A context item can be
selected as relevant but not become the focus. A recommendation can select a
candidate without anyone attending to it.

### Does attention create selection?

Sometimes. Attention may force selection because capacity is limited. Once a
thing becomes active, the participant selects supporting documents, evidence,
questions, and boundaries.

But attention can also be pre-selective. An anomaly may seize attention before a
candidate set or rationale exists. A user request may activate a subject before
formal selection occurs.

### Are they separate operations?

They are distinguishable but interlocked:

```text
attention
    actual focus or activation

selection
    inclusion, exclusion, ordering, or choice among candidates

selection rationale
    explanation of why that selection occurred or should be preserved
```

Attention may be an outcome of selection, an input to selection, or a competing
fact that selection rationale must explain.

### Current finding

Attention and selection should remain distinct. Selection can explain why a
candidate was included or ordered. Attention explains what is actually active.
An attention trigger explains why focus moved. These may align, but they can
also diverge.

---

## Attention Versus Priority

Priority is normative ordering under goals, constraints, authority, risk,
importance, and capacity. Attention is actual focus.

### Can attention diverge from priority?

Yes. The repository already preserves this distinction. Examples:

```text
A low-priority issue receives attention because it blocks the current sentence.
A visible anomaly receives attention before its importance is known.
A user request receives attention even if it is not architecturally important.
A high-priority cleanup receives no attention because the current task is a
documentation-only frontier.
```

### Can low-priority items receive attention?

Yes. Low-priority items can receive attention due to proximity, salience,
operator request, ambiguity, or an unsafe next move inside a bounded task.

### Can high-priority items receive none?

Yes. High-priority items can remain unattended because capacity is absent, the
operator selected a different task, required authority is missing, or the item is
not in active context.

### Current finding

Attention triggers describe actual activation, not what should be activated.
Priority may be one trigger input, but it is not identical to attention.
Treating attention as priority would over-authorize whatever happens to be
visible. Treating priority as attention would erase the practical reality that
many important things are not active.

---

## Attention Versus Working State

Working state is a current work-position, not repository state and not durable
architectural truth. Recent work suggests working state contains only a small
subset of repository knowledge.

### Is working state partially an attention artifact?

Yes, with care. Working state appears to contain what must remain active for
safe continuation:

```text
current frontier
active question
accepted boundaries
unresolved tensions
selected references
next safe move
known unsafe moves
```

Those are attention-shaped because they are not the whole repository. They are
the subset that matters now.

However, working state is not only attention. It also carries constraints,
status, references, and continuation safety. It is a structured continuation
artifact, not a raw focus log.

### Does attention determine active context?

Attention likely influences active context, but does not solely determine it.
Active context is shaped by task, authority, relevance, selection rationale,
context budgets, documentation boundaries, and safety. A participant may attend
to something inappropriate; active context should not automatically include it
as authoritative.

### Current finding

Working state is partly an attention artifact because it preserves the selected
active position needed for continuation. But it must remain distinct from
attention itself. Working state is bounded continuation state; attention is
actual focus; triggers are candidate explanations for movement into focus.

---

## Relationship To Capability Acquisition

The capability readiness audit left unresolved whether acquisition begins from:

```text
goal
need
gap
tension
question
repeated failure
operator burden
frontier
```

This document tests whether attention comes before acquisition.

### Does capability acquisition begin with attention?

A weak version survives scrutiny:

```text
Before acquisition can be considered, some capability-relevant object must
receive attention.
```

That object may be a request, need, gap, repeated failure, operator burden,
missing support, or frontier. Without attention, it remains latent.

A strong version does not survive:

```text
Capability acquisition begins with attention as a formal origin object.
```

Attention is too broad. Many attended things do not become acquisition. A
weather request may be satisfied by an existing capability. A contradiction may
lead to documentation reconciliation. A risk may lead to caveat or deferral.

### Are goal, need, and gap acquisition origins or attention triggers?

Current evidence suggests they can be either, depending on layer:

```text
As represented objects:
    goal, need, and gap may be acquisition-relevant objects.

As activation explanations:
    goal, need, and gap may trigger attention.

As lifecycle origins:
    none is proven to be universal.
```

A capability need may be the origin of acquisition once accepted as a durable
need. A gap may be the evidence-backed reason acquisition is considered. A goal
may explain why the need matters. But a request, repeated failure, or burden may
have moved attention before any of those was formalized.

### Acquisition-origin finding

The acquisition starting object remains unresolved. The attention-trigger
hypothesis improves the vocabulary by separating:

```text
what activated consideration
what object is being considered
what evidence supports a capability gap
what authority permits adoption
what decision selects a candidate
what execution, if any, is authorized
```

This separation is useful, but not reconciled. Implementation of acquisition
logic remains premature.

---

## Relationship To Frontiers

Candidate hypothesis:

```text
A frontier represents sustained attention over an unresolved area.
```

### Evidence supporting the hypothesis

Frontier documents tend to preserve:

```text
central question
unresolved tension
existing authority
candidate distinctions
examples
findings
unresolved tensions
implementation warnings
```

That looks like sustained attention. A frontier is not merely an unknown; it is
an unresolved area made durable for future exploration.

### Counterpressure

Not all frontiers are current attention. Future-frontier preservation explicitly
does not imply priority, sequencing, implementation readiness, or current work.
A frontier can be characterized and then become dormant. A frontier can also be
created because an operator requested a documentation investigation, not because
Seed autonomously sustained attention.

### Current finding

A frontier may be best characterized as:

```text
a preserved exploratory edge around an unresolved area that has received enough
attention to warrant durable characterization.
```

This is close to sustained attention, but not identical. `Frontier` preserves
the result of attention and enables resumption. It can also trigger future
attention when reopened.

---

## Trigger Versus Cause, Rationale, And Authority

The word `trigger` is risky because it can imply mechanical causation. This
frontier uses it cautiously.

### Trigger versus cause

A trigger is a candidate explanation for movement into attention. It may be one
factor among many. It is not necessarily a sufficient cause.

Example:

```text
Contradiction triggered attention.
```

This may mean:

```text
A contradiction was noticed, mattered to the current response, and made further
exploration necessary.
```

The contradiction alone may not have caused attention if it was hidden,
low-consequence, or already scoped.

### Trigger versus rationale

A trigger explains activation. A rationale explains why activation, selection,
or pursuit is justified, useful, safe, or appropriate.

Example:

```text
An anomaly triggered attention.
Risk to projection integrity justified continuing the investigation.
```

The trigger and rationale can differ. Salience may trigger attention, while
risk, authority, or relevance becomes the rationale for continuing.

### Trigger versus authority

A trigger does not authorize action. Operator request can trigger attention but
may still require policy checks. A need can trigger acquisition consideration but
not adoption. A risk can trigger inquiry but not mutation.

Current boundary:

```text
trigger = why focus moved
rationale = why selection or continuation makes sense
authority = what permits, constrains, or settles action/decision
```

---

## Potential Finding Tested

Hypothesis:

```text
Many things exist.
Few things receive attention.
Attention determines active inquiry.
```

### What survives

The first two statements survive strongly. Repository knowledge, unresolved
questions, gaps, and future frontiers are numerous. Active work is narrow.
Working state and active context preserve only a selected subset.

The third statement survives only in a weaker form. Attention is necessary for
active inquiry, but may not determine it alone. Inquiry is also shaped by
operator request, authority, relevance, selection, evidence, documentation
purpose, and safe continuation.

### Revised framing

A safer formulation is:

```text
Many things exist.
Few things become active.
Attention is the activation of focus.
Attention often enables inquiry, but inquiry requires additional structure:
question, scope, evidence, method, authority boundaries, and preservation.
```

---

## Consolidated Findings

1. Attention triggers are a meaningful exploratory concept, but not a reconciled
   ontology object.
2. The strongest trigger candidates are operator request, explicit instruction,
   tension, contradiction, ambiguity with consequence, gap with consequence,
   repeated failure, visible operator burden, risk, anomaly, missing support, and
   unsafe next move.
3. Some candidates are better treated as amplifiers or enabling conditions:
   recurrence, salience, proximity to current work, and available capacity.
4. Goals, needs, and gaps can be attention triggers, but they are not proven to
   be universal starting objects for acquisition or inquiry.
5. A direct operator request usually triggers attention before goal, need, or
   gap is formally decomposed.
6. Repeated failure often transforms attention from isolated event to pattern.
7. Operator burden triggers attention only when visible, reported, represented,
   or connected to current work.
8. Ambiguity becomes a frontier when it repeatedly blocks safe interpretation or
   continuation.
9. Contradiction is a strong internal trigger, but may lead to inquiry about
   scope, support, uncertainty, or risk rather than immediate truth arbitration.
10. Attention differs from inquiry: attention activates focus; inquiry pursues
    unresolved understanding.
11. Attention differs from selection: selection includes, excludes, orders, or
    chooses candidates; attention is actual focus.
12. Attention differs from priority: priority says what should receive focus;
    attention records what does receive focus.
13. Working state is partly attention-shaped, but is not reducible to attention.
14. Capability acquisition likely requires prior attention to a
    capability-relevant object, but attention alone is not an acquisition origin,
    authorization, or engine.
15. A frontier likely preserves an exploratory edge that has received sustained
    attention, but a frontier can be dormant and non-priority.
16. Implementation would be premature because trigger, rationale, authority,
    selection, inquiry, priority, and working state boundaries remain unsettled.

---

## Required Tensions Preserved

| Tension | Why it remains unresolved |
| --- | --- |
| Goal vs trigger | A goal can activate attention, but may also be an interpreted object after a request. |
| Need vs trigger | A need can trigger attention, but evidence-derived needs may require attention before they are recognized. |
| Gap vs trigger | A gap can draw attention, but many gaps remain passive until coupled to consequence or current work. |
| Tension vs trigger | A tension is often a strong trigger, but it can also be the object inquiry explores. |
| Trigger vs cause | Trigger language may overstate causality; most attention movement has multiple conditions. |
| Trigger vs rationale | What grabs attention may differ from what justifies continued pursuit. |
| Trigger vs authority | Activation never equals permission, adoption, execution, or truth settlement. |
| Attention vs inquiry | Attention activates; inquiry explores. The boundary blurs when a question both triggers and constitutes inquiry. |
| Attention vs selection | Selection can create attention, and attention can force selection, but neither fully contains the other. |
| Attention vs priority | Actual focus can diverge from normative ordering. |
| Attention vs relevance | Relevant things may remain unattended; attended things may turn out irrelevant. |
| Attention vs salience | Salience can move attention without indicating importance or truth. |
| Attention vs working state | Working state preserves active continuation position, but includes more than focus. |
| Frontier vs trigger | A frontier may result from sustained attention or later trigger renewed attention. |
| Acquisition origin vs attention trigger | Goal, need, gap, burden, and failure may activate acquisition consideration without being formal lifecycle origins. |
| External vs internal triggers | The boundary depends on current attention state, provenance, authority, and repository location. |
| Historical trigger vs evidence | Repeated failure and burden may trigger attention, provide evidence, or both. |

---

## Why Implementation Would Be Premature

Implementation would be premature for several reasons:

- attention triggers are not reconciled ontology objects;
- attention movement is not the same as priority, authority, selection, or
  inquiry;
- many triggers are participant-relative or context-relative, such as surprise,
  salience, and burden;
- trigger identification could easily become a planner, scheduler,
  prioritization system, or recommendation engine;
- acquisition-origin boundaries remain unresolved;
- repeated failure and operator burden require evidence and authority bridges
  before they can become durable needs;
- contradiction, ambiguity, and risk require existing integrity, evidence,
  confidence, caveat, and authority boundaries rather than a new trigger engine;
- working state and active context already provide bounded continuation
  vocabulary that should not be replaced by an attention system;
- frontiers are explicitly not implementation-ready by default.

The safe result of this document is preserved ontology pressure, not machinery.

---

## Candidate Future Questions

Future documentation-only reconciliation could ask:

1. Is `attention trigger` a needed term, or can existing `selection rationale`,
   `inquiry`, `working state`, and `operator intent` vocabulary cover the same
   ground?
2. Are triggers only explanations in prose, or do any need durable
   representation?
3. Can repeated failure and operator burden become evidence-backed capability
   need signals without creating acquisition logic?
4. Does a frontier always imply prior attention, or only preservation of an
   unresolved area?
5. Should handoff templates preserve why attention is currently here, distinct
   from what the next safe move is?
6. Can attention be documented without implying priority?
7. When a question triggers attention, is the question the trigger, the inquiry
   object, or both?
8. Is salience an architectural hazard because it moves attention without
   evidence of importance?
9. What is the minimal vocabulary needed to explain acquisition starting
   conditions without designing acquisition engines?

These questions should remain documentation-only unless a concrete operator or
implementation need appears and existing authority cannot answer it.

---

## Final Characterization

Attention appears important because Seed repeatedly distinguishes between what
exists and what is active. Repository knowledge, gaps, questions, tensions,
frontiers, and capability possibilities can exist without governing current
work. Working state, active context, and handoff activation show that only a
small subset becomes active enough to guide continuation.

Attention triggers appear to be meaningful as an exploratory concept:

```text
An attention trigger is a candidate explanation for why something moved from
available, latent, or merely represented into active focus.
```

The concept is useful because it prevents premature collapse of acquisition
origins. Goal, need, gap, tension, question, repeated failure, and operator
burden may not be rival universal starting objects. They may be different ways
attention moves, different objects attention lands on, or different rationales
for continuing after attention has moved.

The concept remains unresolved because `trigger` may conflate cause, rationale,
authority, salience, evidence, and selection. Attention itself is also not enough
to define inquiry, acquisition, priority, or working state.

The strongest current distinctions are:

```text
trigger
    why focus moved

attention
    what is active

inquiry
    active or preserved pursuit of unresolved understanding

selection
    inclusion, exclusion, ordering, or choice among candidates

priority
    what should receive focus under goals, constraints, risk, authority, and
    capacity

working state
    bounded continuation position preserving what must remain active for safe
    resumption

capability acquisition
    possible downstream lifecycle requiring need/gap evidence, authority,
    adoption boundaries, and execution constraints
```

Implementation would be premature. The correct current outcome is to preserve
attention triggers as a frontier pressure and continue avoiding collapse among
attention, inquiry, selection, priority, authority, working state, and capability
acquisition.
