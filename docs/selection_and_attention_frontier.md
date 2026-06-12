---
doc_type: frontier
status: exploratory
domain: selection and attention ontology
defines:
  - selection and attention frontier
  - candidate attention object
  - selection rationale boundary
  - active attention boundary
  - attention priority distinction
  - inquiry selection boundary
depends_on:
  - inquiry_frontier.md
  - handoff_and_continuation_lineage_frontier.md
  - operations_frontier.md
  - knowledge_navigation_layers_frontier.md
  - future_frontiers.md
  - foundational_ontology_reconciliation.md
  - architectural_status_and_next_frontier.md
related:
  - selection_rationale_vocabulary.md
  - selection_rationale_reconciliation.md
  - context_composition_vocabulary.md
  - context_composition_reconciliation.md
  - continuation_context_and_working_state_reconciliation.md
  - active_context_and_working_set_reconciliation.md
  - architectural_findings_preservation.md
---

# Selection And Attention Frontier

## Purpose

This document characterizes a documentation-only frontier exposed by recurring
selection, prioritization, relevance, attention, active-context, working-state,
inquiry, handoff, and future-frontier language across Seed documentation.

It investigates the question:

```text
Why is one thing selected instead of another?
```

More specifically, it asks whether Seed's ontology needs to distinguish:

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

The document is ontology discovery only. It does not design planners,
prioritization systems, recommendation engines, agent schedulers, workflow
systems, attention algorithms, runtime behavior, schemas, read models, routes,
provider ranking, LLM ranking, projection mutation, or tests.

Repository authority wins over this frontier. In particular, existing Context
Composition and Selection Rationale work already establishes stable vocabulary
for many current selection surfaces. This document does not reopen those settled
surface-level findings. It investigates a broader inquiry-facing and
continuation-facing question: why attention moves to one unresolved possibility
rather than another.

---

## Background Observation

The repository repeatedly encounters this shape:

```text
Many possible directions exist.
Only a few become active.
```

Examples include:

```text
Many unresolved questions exist.
One becomes a frontier.

Many frontiers exist.
One becomes today's investigation.

Many findings exist.
Some become working state.

Many preserved facts exist.
Only a selected subset governs continuation.
```

Existing documentation increasingly explains:

```text
What is known.
```

and:

```text
What is being investigated.
```

The possible missing question is:

```text
Why this investigation?
```

That question should not be treated as an implementation request. It is a
boundary test for whether selection-related concepts have recurring
architectural roles outside already-characterized projection, context, current
state, capability, and explanation surfaces.

---

## Existing Authority That Constrains This Frontier

### Foundational Ontology

Seed is claim-centric. Observations, evidence, claims, facts, relationships,
projections, assessments, recommendations, decisions, operators, questions,
goals, policy, authority, explanation, and handoffs already have settled or
partly settled roles.

That matters because selection must not silently become truth, authority,
policy, decision, recommendation, or execution. A selected item is not thereby
more true. A prioritized item is not thereby authorized. An attended item is not
thereby implemented.

### Selection Rationale And Context Composition

Selection Rationale Vocabulary already defines selection rationale as a
read-only account of why an already-known candidate had a specific selection
outcome for a specific surface. It also rejects a `SelectionEngine`, planner,
workflow engine, provider router, and truth arbiter.

Context Composition already distinguishes context selection, relevance,
priority, budgets, ordering, exclusion, and explanation for context-facing
surfaces.

Therefore this frontier must not duplicate those documents by inventing a new
central selection artifact. Its narrower contribution is to ask whether the
repository also shows inquiry-level or attention-level selection: the movement
from many possible unresolved directions into the active edge of work.

### Inquiry Frontier

The Inquiry Frontier asks whether inquiry has objects, lineage, state,
relationships, and lifecycle distinct from claim-centered knowledge. It already
uses terms such as tension, question, gap, audit, frontier, open question, next
frontier, working state, active context, and selection rationale.

This frontier treats inquiry as the immediate neighbor. If inquiry asks what is
unresolved, selection may ask why one unresolved thing is attended to now.

### Handoff And Continuation Lineage Frontier

The Handoff And Continuation Lineage Frontier found that continuation can fail
despite preserved information when active position, selection rationale,
unresolved tensions, navigation context, or activation does not survive the
handoff.

That finding strongly suggests attention is not merely a reader's mental state.
A handoff may need to preserve what must remain active, why it was selected, and
what would make continuation unsafe.

### Knowledge Navigation Layers Frontier

Knowledge Navigation answers:

```text
I have a question. Where should I look?
```

Selection is adjacent but not identical. Navigation may expose possible paths;
selection explains why a particular path is active, relevant, or safe to pursue
now.

### Future Frontiers

Future Frontiers explicitly says a frontier appearing on the bounty board means:

```text
Interesting enough to revisit.
```

It does not mean priority, sequencing, implementation readiness, or canonical
ontology. This distinction is crucial: an unknown can be preserved as a possible
future frontier without becoming current priority or active attention.

---

## Method

This investigation reviewed the requested authoritative references and adjacent
selection/context documents needed to avoid contradicting existing authority.
It looked for recurring roles rather than word frequency.

The test was whether candidate concepts answer different questions:

```text
What is not known?
What is missing?
What is unstable, surprising, or unresolved?
What is at the active edge of exploration?
What matters for a purpose?
What should be considered first?
What is currently being considered?
Why was this path selected?
What subset governs current work?
```

If two words answer the same question under all tested examples, they may not
need separate ontology roles. If collapsing them creates architectural error,
they should remain distinct at least as frontier vocabulary.

---

## Candidate Selection Concepts Evaluated

| Candidate | Candidate question | Preliminary finding |
| --- | --- | --- |
| Unknown | What is not known by Seed or a participant? | Broadest category; too large to be a frontier by itself. |
| Gap | What understanding, support, representation, or answer is missing for a purpose? | More scoped than unknown; can exist without active exploration. |
| Tension | What appears incomplete, inconsistent, surprising, unresolved, or unexplained? | Strong inquiry signal; may motivate but does not guarantee selection. |
| Frontier | What is the active edge of exploration or reconciliation? | More active than gap or tension; usually selected from many possibilities. |
| Relevance | Why does something matter to the current question, context, or purpose? | Purpose-relative; not the same as importance or truth. |
| Importance | Why does something matter in broader consequence, risk, value, or architectural weight? | May influence priority but is not identical to current attention. |
| Significance | Why might a finding change interpretation, architecture, or future work? | Close to importance; may be retrospective or prospective. |
| Attention | What is currently receiving focus or active cognitive/work bandwidth? | Distinct from priority because attention can drift, lag, or be constrained. |
| Priority | What should receive focus under current goals, constraints, authority, and risk? | Normative ordering; may diverge from actual attention. |
| Selection rationale | Why was one candidate included, ordered, made current, or pursued over alternatives? | Already stable for surface selection; emerging for inquiry and continuation selection. |
| Active context | What matters right now for safe/current work? | A selected subset of total knowledge and inquiry context. |
| Working state | Where does active work stand now? | Work-position, not repository state; selected but not identical to selected state. |

The table supports a cautious conclusion: not all candidates are primitives, but
collapsing them all into `selection` would lose important distinctions.

---

## Knowledge, Inquiry, And Selection

The proposed framing under test is:

```text
Knowledge answers:
    What is known?

Inquiry answers:
    What is unresolved?

Selection answers:
    Why are we looking here?
```

### What Survives Scrutiny

The framing is useful because the three questions fail in different ways.

Knowledge can be preserved without telling a future participant what remains
unresolved. Inquiry can list unresolved things without explaining why one is the
current edge. Selection can explain why a subset is active without proving the
selected candidate is true or settled.

This distinction explains several repository patterns:

- a fact can be known but not active;
- a gap can be known but not investigated;
- a tension can be recognized but not promoted to frontier;
- a frontier can be characterized but not current priority;
- a handoff can preserve information but lose continuation alignment if the
  active selection is not preserved.

### What Does Not Survive Cleanly

The framing is too clean if it implies three independent systems. Knowledge,
inquiry, and selection interlock.

A question may arise from known evidence. A gap may be defined only relative to
a current goal or authority boundary. A frontier may be both an inquiry object
and a selected active context. A projection may select known information without
being an inquiry. A decision may select an option under authority, which is not
the same as attention selection.

A safer frontier formulation is:

```text
Knowledge, inquiry, and selection appear distinct by primary question, but they
share objects, operations, surfaces, and explanation needs.
```

---

## Unknown, Gap, Tension, And Frontier

### Unknown

`Unknown` is too broad to be an active frontier. It includes everything Seed,
an operator, or a participant does not know. Most unknowns are not actionable,
recognized, relevant, or safe to pursue.

Unknowns can become architecturally meaningful only when they are bounded by a
question, source, purpose, authority boundary, evidence limitation, or observed
failure.

### Gap

A `gap` is a missing understanding, support, representation, or answer relative
to a purpose. A gap is narrower than an unknown because it has a recognizable
shape:

```text
Something needed for explanation, continuation, support, reconciliation, or safe
work is missing.
```

Not all gaps are frontiers. Some are irrelevant to current work, too broad,
unsafe to pursue, already delegated to later documentation, or acceptable as
known limitations.

### Tension

A `tension` is not merely absence. It is pressure created by incompleteness,
inconsistency, surprise, unresolved boundary conflict, or unexplained behavior.

Tension is often a stronger frontier signal than gap because it suggests current
architecture may be strained. However, tensions can remain dormant. A document
may preserve a tension without selecting it as the next investigation.

### Frontier

A `frontier` is the active edge of exploration. It usually carries both an
unresolved object and a selection state:

```text
This is not settled, and this is where investigation is now allowed or useful to
continue.
```

A frontier can originate from a gap, tension, unknown, contradiction, repeated
pattern, failed continuation, or operator question. The frontier is not identical
to any of those origins because it adds active exploration and boundary framing.

### Boundary Findings

```text
All gaps are not frontiers.
All tensions are not frontiers.
All frontiers are not merely gaps.
All frontiers probably contain unresolvedness, but unresolvedness may be a gap,
tension, open question, or boundary pressure rather than simple missing
knowledge.
```

A frontier without any tension is possible when an operator chooses to explore a
new bounded domain despite no inconsistency. A frontier without any gap is less
plausible, unless `gap` is defined narrowly as missing facts rather than missing
understanding, characterization, or reconciliation.

---

## Relevance, Importance, Significance, Priority, And Attention

### Relevance

`Relevance` is relation-to-purpose:

```text
This matters for this question, context, continuation, surface, or boundary.
```

Relevance is not truth. Relevance is also not importance. A low-consequence item
can be highly relevant to a narrow investigation, while a high-consequence item
can be irrelevant to the present question.

### Importance And Significance

`Importance` appears broader and more value- or consequence-laden than
relevance. It may involve risk, architectural centrality, operator value,
frequency, blast radius, or future consequences.

`Significance` appears close to importance but often names interpretive effect:

```text
If this is right, it changes how nearby concepts should be understood.
```

Neither importance nor significance automatically creates current attention.
They can justify priority, but authority, timing, safety, existing evidence,
participant capability, and current task boundaries may still prevent selection.

### Priority

`Priority` is a normative ordering:

```text
What should receive focus first under current goals, constraints, risk,
authority, and available capacity?
```

Priority can be recorded without being acted on. Future Frontiers demonstrates
this boundary by preserving candidates while explicitly refusing to imply
priority or sequencing.

### Attention

`Attention` is actual active focus:

```text
What is receiving work, interpretation, continuation bandwidth, or active
context right now?
```

Attention can diverge from priority. It can be pulled by operator request,
handoff constraints, discovered risk, missing authority, local availability,
recent evidence, participant capability, or simple continuation momentum.

### Boundary Findings

```text
Relevance answers why something matters here.
Importance answers why something matters broadly.
Priority answers what should receive focus.
Attention answers what is receiving focus.
Selection rationale explains why a selection outcome occurred.
```

The repository should preserve these distinctions. If attention is treated as
priority, accidental focus may become justified after the fact. If priority is
treated as attention, documented importance may be mistaken for active work. If
relevance is treated as importance, narrow contextual fit may be over-promoted
into architectural weight.

---

## Selection Rationale

Selection rationale is already established as a recurring architectural concept
for explaining surface-level inclusion, exclusion, ordering, and current-state
choice over already-known candidates.

This frontier tests whether a related but broader rationale appears at the
inquiry and continuation layer:

```text
Why was one path selected?
Why was another path not selected?
Why did this tension become active?
Why did this frontier become today's investigation?
Why did these findings enter working state?
```

### Rationale Versus Outcome

The outcome is the selected item or path. The rationale is the explanation of
why that outcome occurred or should be preserved.

They must remain distinct. A document can record that endpoint prominence led to
projection-boundary investigation and host-observation reconciliation without
fully explaining why that path was chosen over other possible audits.

### Rationale Versus Authority

Selection rationale is not authority. It may cite authority, respect authority,
or explain authority constraints, but it does not approve work, settle ontology,
or promote a frontier into architecture.

### Rationale Versus Navigation

Navigation identifies possible paths and where to look. Selection rationale
explains why a path is active, preferred, excluded, deferred, or safe relative to
the current purpose.

### Preliminary Finding

Selection rationale appears to have at least two layers:

| Layer | Question | Status |
| --- | --- | --- |
| Surface selection rationale | Why did a known candidate appear, not appear, order, or become current on a surface? | Already characterized/reconciled enough for current architecture. |
| Inquiry/attention selection rationale | Why did this unresolved path, frontier, or working-state subset become active? | Emerging frontier; not reconciled. |

The second layer should not be implemented until its boundaries with inquiry,
handoff lineage, navigation, active context, working state, authority, and
priority are reconciled.

---

## Critical Examples

### Example 1: Endpoint Prominence

The path:

```text
endpoint prominence
    -> projection boundary
    -> host observation
```

suggests selection occurred. Many audits were possible, but the investigation
followed the path where endpoint identity, host identity, and projection behavior
were producing visible architectural pressure.

Possible selection signals included:

- recurring projection noise;
- boundary risk from over-promoting endpoint evidence into host truth;
- concrete Prometheus cleanup needs;
- relation to already-reconciled observation and evidence boundaries;
- availability of bounded documentation and implementation surfaces.

This path was not merely navigation. Navigation could show where endpoint,
projection, and host documents are. Selection explains why those documents became
the active edge.

### Example 2: Handoff Failure

Handoff work shows that many facts can survive while continuation still fails.
That failure is difficult to explain as knowledge loss alone.

What may be lost is selected attention:

```text
which references matter now
which tensions remain live
which next move is safe
which alternatives are intentionally inactive
why this subset governs continuation
```

Preserved selection rationale appears continuation-relevant because it keeps the
next participant from flattening all known information into equal background.
Preserved attention also matters because active context is smaller than total
knowledge.

### Example 3: Future Frontiers

Future Frontiers contains many unknowns, but only some are included. Inclusion
appears to require more than being unknown.

Candidate transformation may involve:

- repeated emergence across investigations;
- boundary pressure not resolved by existing documents;
- architectural significance;
- enough shape to ask future questions;
- not enough stability to reconcile;
- explicit non-commitment to priority or implementation.

Thus a future frontier is not simply an unknown. It is a selected, preserved,
question-shaped candidate for later attention.

### Example 4: Working State

A repository may contain thousands of findings. Working state contains only a
small subset.

The operation or boundary at work appears to be selection into active
work-position:

```text
What must remain operative for current safe continuation?
```

This differs from a complete knowledge inventory. Working state is selected for
continuation relevance, risk, unresolvedness, next move safety, and current task
scope. It is not necessarily the same as what is most important globally.

---

## Relationship To Handoffs

Successful continuation likely requires preserving selected material rather than
preserving everything.

Candidate selected material includes:

```text
selected knowledge
selected inquiry
selected tensions
selected constraints
selected risks
selected next moves
selected authority reminders
```

The handoff question is not:

```text
Can everything be transferred?
```

It is closer to:

```text
What must remain active so continuation does not drift, restart, or over-promote
working state into authority?
```

This finding supports the Handoff And Continuation Lineage Frontier: continuation
may be a selection-preservation problem as much as an information-preservation
problem.

---

## Relationship To Inquiry

Inquiry appears to require selection at least in practice.

A repository can preserve many unresolved questions, but a participant cannot
explore every unresolved thing simultaneously. Inquiry becomes active when a
question, gap, tension, or frontier is selected into current attention.

However, inquiry should not be collapsed into selection. Inquiry names the
unresolved object, lineage, or investigation state. Selection names why one part
of that unresolved space is active, ordered, included, excluded, deferred, or
made current.

A cautious relationship is:

```text
Inquiry identifies unresolved possibility.
Selection activates, orders, or bounds attention within unresolved possibility.
Attention is the current realized focus of that selection, whether or not it
perfectly matches priority.
```

---

## Working State Versus Selected State

`Working state` is already stronger than a selected list. It records where active
work stands, including current frontier, constraints, validation state, risks,
and next safe moves.

A `selected state` would be too broad or too ambiguous if it only meant any
subset chosen from repository knowledge. Many projections, context packets, and
current-state views are selected states in a loose sense, but they are not
working state.

Boundary finding:

```text
Working state is selected, but not every selected state is working state.
```

Working state is selected for continuation and safe current work. A context
packet is selected for model-visible context. A projection is selected for
communication. A decision selects under authority. These selection types should
not be collapsed.

---

## Candidate Relationship Map

A possible non-authoritative relationship map is:

```text
unknown
    may become recognized as
        gap
        tension
        question

recognized gap or tension
    may become
        candidate inquiry
        future frontier
        active frontier

future frontier
    preserves possible later attention
    without implying priority

active frontier
    is selected into current exploration
    and may enter working state

working state
    preserves the active selected position
    needed for safe continuation

selection rationale
    explains why a candidate, path, surface item, frontier, or subset
    was selected, excluded, ordered, deferred, or made current
```

This map is intentionally tentative. It is useful because it prevents the most
dangerous collapse: treating every unknown as a frontier or every frontier as a
priority.

---

## Major Findings

1. Selection-related concepts recur across inquiry, handoff, continuation,
   working state, navigation, future-frontier preservation, context composition,
   and projection surfaces.
2. Existing Selection Rationale documents already cover many surface-level
   selection questions; this frontier should not create a new central selection
   system.
3. A broader inquiry/attention selection question remains visible: why one
   unresolved path becomes active while others remain inactive, deferred, or
   merely preserved.
4. Knowledge, inquiry, and selection are distinguishable by primary question,
   but they are not independent systems.
5. Gaps, tensions, and frontiers are not equivalent. Gaps and tensions can exist
   without becoming frontiers; frontiers add active exploration framing.
6. Attention and priority are distinct. Attention is actual focus; priority is
   normative ordering under goals, constraints, authority, risk, and capacity.
7. Relevance and importance are distinct. Relevance is purpose-relative;
   importance is broader and consequence- or value-laden.
8. Selection rationale is distinct from outcome, authority, and navigation.
9. Handoffs likely need selected knowledge, selected inquiry, and selected
   tensions rather than complete preservation of everything.
10. Implementation would be premature because the repository has not reconciled
    inquiry-level selection, attention, priority, active context, working state,
    navigation intent, and handoff lineage boundaries.

---

## Required Tensions Preserved

| Tension | Frontier pressure |
| --- | --- |
| Gap vs tension | Gap names missing understanding; tension names pressure from incompleteness, inconsistency, surprise, or unresolved boundary conflict. |
| Tension vs frontier | Tensions can remain dormant; frontiers are active edges of exploration. |
| Frontier vs priority | A frontier can be characterized without being current priority; current priority can be implementation cleanup rather than conceptual frontier work. |
| Attention vs priority | Attention is actual focus; priority is what should receive focus. They can diverge. |
| Relevance vs importance | Relevance is purpose-relative; importance is broader consequence, risk, value, or architectural weight. |
| Selection vs authority | Selection explains focus or inclusion; authority approves, constrains, or settles boundaries. |
| Selection vs navigation | Navigation exposes paths; selection explains why a path is active, preferred, deferred, or excluded. |
| Selection rationale vs outcome | Outcome is what was selected; rationale is why selection occurred or should be preserved. |
| Working state vs selected state | Working state is selected for active continuation; not every selected projection, context, or current-state view is working state. |
| Inquiry vs selection | Inquiry names unresolved work; selection activates or orders attention among unresolved possibilities. |
| Priority vs future frontier | Future-frontier preservation marks revisit-worthiness without priority, sequencing, or implementation readiness. |
| Surface selection vs inquiry selection | Surface selection is already partly reconciled; inquiry-level selection remains exploratory. |

---

## Why Implementation Would Be Premature

Implementation would be premature for several reasons:

- existing authority already rejects new selection engines, context engines,
  planner/workflow systems, provider ranking systems, and parallel truth systems;
- surface-level selection rationale is already distributed across existing
  surfaces and does not require a new runtime owner;
- inquiry-level selection has not been reconciled as an object, operation,
  lineage property, handoff requirement, navigation property, or working-state
  property;
- attention and priority remain distinct, so an implementation could easily
  turn observed focus into normative priority or documented priority into forced
  attention;
- future-frontier inclusion explicitly does not imply priority or sequencing;
- handoff preservation needs bounded active context, not a complete selection
  inventory;
- selection rationale must remain distinct from authority and outcome.

The safe next step is not implementation. The safe result of this document is
preserved vocabulary pressure and unresolved tensions for later reconciliation.

---

## Conclusion

Selection appears important because Seed repeatedly moves from many possible
known, unknown, unresolved, or documented directions into a much smaller active
set.

Selection-related objects may exist, but the current evidence is mixed. Surface
selection rationale is already well characterized. Inquiry-level attention
selection is visible but not reconciled. It may ultimately belong to inquiry
lineage, handoff lineage, working state, navigation intent, operations, or a
small separate selection concept.

The most durable current finding is not that Seed needs a selection system. It
is that Seed must preserve distinctions among:

```text
what is known
what is unresolved
what matters here
what should receive focus
what is receiving focus
why this was selected
what authority permits or settles
what must remain active for continuation
```

Until those distinctions are reconciled, implementation would risk collapsing
attention into priority, priority into authority, relevance into importance,
frontier into gap, or selection rationale into outcome.
