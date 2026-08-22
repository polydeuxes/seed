# Continuation Context And Working State Reconciliation

## 1. Purpose and scope

This document reconciles Seed's architectural boundary for continuation context,
working state, activity preservation, momentum preservation, session continuity,
and continuation-oriented information boundaries.

It answers the narrow architectural question:

```text
Does continuation require preserving more than alignment and references?
```

The answer is yes, but only within a bounded continuation role. A future
participant may know the architecture, ontology, frontier, and references while
still lacking the immediate work-position needed to continue efficiently after
interruption. That immediate work-position is not authority, not architecture,
not a transcript, and not a full historical summary. It is activity context
inside continuation context.

This is a documentation-only reconciliation. It does not implement code, modify
schemas, change runtime behavior, alter handoff execution behavior, authority
systems, observations, claims, projections, recommendations, decisions, ontology
definitions, or tests. It introduces no new runtime semantics.

## 2. Central finding

Continuation requires preserving more than alignment and references when work is
interrupted in the middle of an investigation, implementation, audit, or
decision path.

The missing category is not more authority. It is not a larger transcript. It is
not a duplicate architecture document. The missing category is a compact account
of the current working state:

- what was just completed;
- what was actively being investigated;
- which question or tension remained open;
- which reasoning branch was currently live;
- what the next safe move appeared to be;
- which risks or constraints were immediately relevant.

This category preserves momentum. Activation is what makes the future participant
treat the handoff and its activity context as live continuation guidance rather
than review material. Activity context can preserve the work-position, but it does
not guarantee that the consumer will use that work-position unless the bootstrap
is activated.

This category helps a future participant answer:

```text
What was I doing, and where should continuation resume?
```

That question differs from:

```text
What is true?
How is the architecture defined?
How did we get here?
What happened in the transcript?
What is the roadmap?
What is the current status?
```

The resulting boundary is:

```text
Authority preserves correctness.
Bootstrap preserves alignment.
Activation makes bootstrap content live in working state.
Activity context preserves momentum.
Summary preserves history.
Transcript preserves interaction provenance.
Roadmap preserves intended direction.
Status preserves declared condition.
Working state preserves current work-position.
```

## 3. Definitions

### 3.1 Continuation context

Continuation context is the bounded set of information a future participant
needs in order to resume a work episode safely, coherently, and efficiently after
an interruption.

It is a continuation-oriented selection over already-existing architecture,
state, references, activity, risks, and unresolved questions. It does not own the
truth of those items. It keeps the next participant aligned with what matters for
resumption.

Continuation context differs from authority because authority determines what is
allowed to count as correct, accepted, or binding. Continuation context may point
to authority, but it does not replace it.

Continuation context differs from architecture because architecture defines
system concepts, boundaries, ownership, and design commitments. Continuation
context only selects the subset of those things that matters to a current or
recent work episode.

Continuation context differs from summary because summary compresses what has
been covered. Continuation context preserves what must remain active next.

Continuation context differs from transcript because transcript preserves the
chronological interaction record. Continuation context discards most chronology
and keeps the continuation-relevant working set.

### 3.2 Working state

Working state is the current work-position of a participant, session, or work
stream.

It represents active work rather than preserved knowledge. It includes the
immediate objective, the current object of attention, the live reasoning branch,
recently completed step, next intended step, known blockers, active tensions,
relevant constraints, and short-lived assumptions that must be checked before
continuing.

Working state is not the same as repository state. Repository state describes
what files, commits, artifacts, projections, or stored records exist. Working
state describes where the work process currently stands relative to them.

Working state is also not architecture. Architecture may explain why a boundary
exists. Working state explains which boundary is currently being exercised and
what the next participant was about to do with it.

### 3.3 Activity context

Activity context is the continuation-facing slice of working state.

It answers questions such as:

- What was the last completed audit?
- What was the last completed implementation?
- What was the current investigation?
- What question was still unresolved?
- What was about to be attempted?
- What should not be retried without revalidation?

Activity context differs from summary because it is oriented around active
position, not historical coverage. A summary can say that several documents were
reviewed. Activity context says which review result is currently operative,
which thread remains open, and what action was next.

### 3.4 Momentum preservation

Momentum preservation is the preservation of enough immediate context to avoid
forcing a future participant to rediscover the local work-position before taking
the next safe step.

Momentum is not speed alone. It is continuity of attention, constraint, and
intent. Preserving momentum prevents loss patterns such as:

```text
Architecture known
+ references known
+ current work-position unknown
= safe but inefficient restart
```

Momentum preservation should be compact. It should not require preserving or
replaying the full transcript. It should identify the current edge of work, the
open questions at that edge, and the next safe move.

## 4. Conceptual boundary map

| Concept | Preserves | Answers | Does not own |
| --- | --- | --- | --- |
| Authority | Correctness, acceptance, binding constraints, source of truth. | What may be relied on as correct or accepted? | Momentum, narrative history, transcript chronology. |
| Continuation bootstrap | Initial alignment and safe orientation. | What must be loaded first to avoid immediate misalignment? | Full working state, full history, architecture itself. |
| Bootstrap activation | Live continuation use of consumed bootstrap content. | Has the bootstrap entered active working state? | Authority, proof, compliance by itself. |
| Continuation context | Resumption-relevant context. | What must remain available to continue safely and efficiently? | Independent truth, proof, ontology ownership. |
| Working state | Current work-position. | Where does the active work stand right now? | Durable architecture, durable status, complete history. |
| Activity context | Continuation-facing active work slice. | What was being done, just done, and about to be done? | Authority, comprehensive summary, transcript. |
| Momentum | Local continuity of attention and next-step readiness. | What prevents rediscovery before continuing? | Correctness, history, roadmap priority. |
| Historical summary | Compressed account of past reasoning or events. | How did we get here? | Current activity, authority, complete transcript. |
| Status | Declared condition of a thing at a point in time. | What is the known or reported condition? | Process position, next action, rationale history. |
| Roadmap | Intended or possible future direction. | Where might work go? | Current activity, current commitment, authority. |
| Transcript | Chronological interaction provenance. | What was said or done in sequence? | Curated continuation priority, architecture, authority. |

These categories overlap in content but not in role. A sentence such as
"the next safe move is to audit X" may appear in activity context, a handoff,
and a roadmap note. Its role changes by location: in activity context it
preserves momentum; in a roadmap it indicates future direction; in a handoff it
supports transition; in no case does it become architectural authority by mere
repetition.

## 5. What belongs in continuation context

Continuation context should contain only information that materially improves
safe resumption. The following categories belong when applicable.

| Candidate | Belongs? | Rationale |
| --- | --- | --- |
| Current frontier | Yes. | Identifies the active boundary of work and prevents broad restart. |
| Active tensions | Yes. | Preserves unresolved conflict, ambiguity, or category pressure that should not be erased by omission. |
| Last completed work | Yes, compactly. | Establishes the immediate predecessor step and prevents accidental repetition. |
| Pending questions | Yes. | Keeps open inquiry open and prevents premature closure. |
| Current reasoning branch | Yes, when live. | Preserves the path being tested without elevating it to accepted architecture. |
| Next safe move | Yes. | Converts context into resumption readiness while remaining non-authoritative guidance. |
| Known risks | Yes. | Warns the next participant about likely failure modes, unsafe collapses, stale assumptions, or validation needs. |
| Implementation targets | Yes, when work is implementation-oriented. | Identifies likely files, modules, or surfaces, but does not authorize modification by itself. |
| Relevant references | Yes. | Keeps continuation subordinate to authoritative documents, repository state, evidence, and tests. |
| Recently invalidated paths | Yes, if likely to be retried. | Avoids wasting momentum on paths already found unsafe or out of scope. |
| Consumption expectations | Yes. | Tells the next participant what must be read, what may be optional, and what must be revalidated. |

The information should be selected for immediate continuation value. It should
not attempt to restate every prior reconciliation, reproduce ontology
definitions, or preserve all historical detail.

## 6. What does not belong in continuation context

Continuation context should exclude content whose preservation would collapse it
into another artifact type.

| Candidate | Does not belong as continuation context | Reason |
| --- | --- | --- |
| Full transcript | Exclude. | Transcript preservation is chronology/provenance, not curated resumption context. |
| Complete history | Exclude. | Complete history belongs in archives, summaries, or source documents. Continuation needs selected current relevance. |
| Architecture duplication | Exclude. | Architecture should be referenced, not rewritten into continuation artifacts. |
| Ontology duplication | Exclude. | Ontology definitions remain in ontology or vocabulary documents. Duplication risks drift. |
| Reconciliation duplication | Exclude. | Reconciliation findings should be cited or named rather than copied wholesale. |
| Full roadmap | Exclude. | Roadmap direction is broader than current activity. |
| Full status inventory | Exclude. | Status may inform continuation, but a status document is not working state. |
| Speculative branches not currently live | Usually exclude. | Dormant speculation increases load unless it prevents a known continuation error. |
| Unaccepted recommendations | Usually exclude. | Recommendations can be referenced as pending or rejected, but should not be smuggled into active guidance. |

The exclusion rule is not that this material is useless. The rule is that it is
owned elsewhere. Continuation context may point to it when needed.

## 7. Activity context and summary

Activity context and summary answer different continuation questions.

```text
Activity context: What was I doing?
Summary: How did we get here?
```

A participant may understand history without knowing current activity. For
example, a summary may explain the sequence of handoff reconciliations, the
finding that handoffs are not authority, and the reason summaries are optional.
That still may not reveal which audit was actively in progress, which question
was being tested, or what action was intended next.

A participant may also continue safely without consuming a broad summary if the
bootstrap, authority references, and activity context provide enough orientation
for the next bounded task. This does not make summary unimportant. It means
historical context remains optional unless the current task depends on the path
by which a finding was reached.

The distinction matters because a summary optimized for history may omit the
current work-position, while an activity context optimized for momentum may omit
large amounts of history. Both omissions are correct when the artifact preserves
its role.

## 8. Activity context and authority

Activity context may guide work without becoming authoritative.

It can say:

```text
The current investigation was testing whether continuation needs active working
state in addition to bootstrap references. The next safe move was a
documentation-only boundary reconciliation.
```

That guidance helps preserve momentum. It does not prove the resulting finding,
modify architecture by itself, authorize code changes, or override canonical
source documents.

Activity context should therefore use language that preserves its status:

- "current investigation" rather than "settled architecture";
- "next safe move" rather than "required implementation";
- "active tension" rather than "contradiction resolved";
- "known risk" rather than "binding prohibition" unless a binding prohibition is
  separately sourced;
- "reference" rather than "replacement source of truth."

This boundary allows working state to be useful without turning it into a
parallel authority system.

## 9. Consumption expectations

Continuation does not require every artifact to be consumed in every session.
Consumption expectations should match artifact role and task risk.

| Artifact | Consumption expectation | Reason |
| --- | --- | --- |
| Activation section | Required when a handoff is used for continuation. | Prevents treating the artifact as review material and directs use as live working state. |
| Bootstrap | Usually required for continuation. | Preserves initial alignment, non-goals, and immediate guardrails. |
| Authoritative references | Required when acting on claims, boundaries, code, tests, or architecture. | Continuation context points to authority; it does not replace it. |
| Activity context | Required when resuming interrupted active work. | Preserves momentum and current work-position. |
| Summary | Optional unless historical path affects the current decision. | Summary preserves history; safe continuation may not require full history. |
| Transcript | Optional and exceptional. | Needed for provenance disputes, ambiguity, or audit of interaction sequence, not normal continuation. |
| Roadmap | Optional unless choosing or reprioritizing future work. | Roadmap direction is broader than the current work-position. |
| Status | Required when the current task depends on declared condition. | Status can constrain work but does not itself describe active process. |

The minimum safe continuation pattern is:

```text
activation to make the handoff live continuation guidance
+ bootstrap for alignment
+ activity context for momentum
+ authoritative references for correctness
+ repository or evidence validation before acting
```

Summary and transcript remain available but should not be mandatory by default.
Making them mandatory would convert continuation into historical replay and
undermine the compactness that continuation artifacts are meant to preserve.

## 10. Distinctions that should not be collapsed

### 10.1 Availability is not activation

A handoff can be accessible without being read, read without affecting working
state, and activated without full compliance. Safe continuation therefore requires
more than possession of the artifact.

If these are collapsed, an available handoff may be mistaken for successful
continuation while references remain unvalidated and optional prose drives the
next move.

### 10.2 Bootstrap is not activity context

Bootstrap preserves initial alignment: scope, non-goals, guardrails, and where to
look. Activity context preserves the active work-position: what was being done,
what was just completed, and what was next.

If these are collapsed, bootstrap grows too large and loses its ability to orient
quickly.

### 10.3 Activity context is not summary

Activity context preserves momentum. Summary preserves history.

If these are collapsed, a historical summary may be mistaken for current
guidance, or a compact activity note may be expected to carry all historical
rationale.

### 10.4 Summary is not authority

Summary may compress findings, but it does not own correctness. Authority
remains with canonical architecture, accepted decisions, evidence, repository
state, tests, and other designated sources.

If these are collapsed, convenient restatements can outrank the sources they
summarize.

### 10.5 Status is not working state

Status describes condition. Working state describes process position.

A document can say that a reconciliation is complete without saying what was
being investigated next. Conversely, activity context can say that a participant
was investigating a status gap without changing the status itself.

### 10.6 Roadmap is not current activity

Roadmap describes possible or intended direction. Current activity describes the
work presently active.

If these are collapsed, every future possibility can look like current work, and
every current task can look like a durable plan.

### 10.7 Transcript is not continuation context

Transcript preserves sequence. Continuation context preserves selected
resumption relevance.

If these are collapsed, continuation requires replaying conversation order and
may revive superseded speculation instead of carrying forward the current edge.

### 10.8 Momentum is not history

Momentum depends on current relevance and next-step readiness. History depends
on provenance and narrative path.

If these are collapsed, preserving momentum becomes unnecessarily expensive and
historical completeness is mistaken for continuation quality.

### 10.9 Working state is not architecture

Working state may reference architecture, but it remains situated and temporary.
Architecture defines durable concepts and boundaries.

If these are collapsed, transient work-position can accidentally become design
commitment.

## 11. Non-goals

This reconciliation does not require or recommend:

- new schemas;
- new runtime behavior;
- new handoff execution behavior;
- new authority systems;
- new observation types;
- new claim semantics;
- new projection semantics;
- new recommendation or decision behavior;
- ontology changes;
- tests;
- transcript preservation requirements;
- mandatory summary consumption;
- a complete activity log;
- conversion of working state into durable architecture;
- conversion of momentum guidance into authority.

It only clarifies documentation boundaries for continuation-oriented
information.

## 12. Implementation implications

No implementation work is directly required by these findings.

If future documentation or handoff templates are revised, they should preserve
these boundaries:

- make activation explicit before bootstrap content;
- keep bootstrap small and alignment-oriented;
- keep activity context compact and momentum-oriented;
- cite authoritative references rather than duplicating architecture;
- treat summaries as optional historical compression;
- avoid requiring transcript replay for ordinary continuation;
- identify next safe moves as guidance, not authority;
- distinguish current activity from roadmap direction and status declarations.

These are documentation implications, not runtime requirements.

## 13. Architectural invariants supported

The reconciliation supports the following architectural invariants:

```text
Authority preserves correctness.
Bootstrap preserves alignment.
Activation makes bootstrap content live in working state.
Activity context preserves momentum.
Summary preserves history.
Transcript preserves interaction provenance.
Status preserves declared condition.
Roadmap preserves intended direction.
Working state preserves current work-position.
```

Additional supported invariants:

- Availability, consumption, activation, and compliance should remain
  distinguishable.
- Activity context preserves momentum, but activation is what makes the consumer
  treat the handoff as live continuation rather than review material.
- Working state should remain distinguishable from architecture.
- Continuation should not require transcript preservation.
- Momentum should not become authority.
- Historical context should remain optional unless the current task depends on
  historical path.
- A participant may continue safely without consuming summary content when
  bootstrap, activity context, authority references, and validation are adequate.
- A participant may understand history without knowing current activity.
- Working state may be useful without becoming authoritative.
- Continuation context should select for resumption relevance, not completeness.

## 14. Final conclusion

Continuation requires activation and a small amount of activity-aware working
state in addition to alignment and references when work is interrupted before a
natural boundary.

That addition should be understood as momentum preservation, not as authority,
architecture, summary, status, roadmap, ontology, transcript, or execution
semantics.

The safe model is:

```text
Correctness comes from authority.
Alignment comes from bootstrap.
Activation makes alignment live in working state.
Momentum comes from activity context.
History comes from summary.
Provenance comes from transcript.
Direction comes from roadmap.
Condition comes from status.
Current work-position comes from working state.
```

Preserving these distinctions allows continuation to be efficient without making
continuation artifacts larger, more authoritative, or more historically complete
than their role requires.
