# Handoff Document Boundary Reconciliation

## 1. Purpose and scope

This document performs a documentation-only reconciliation of handoff documents,
continuation artifacts, alignment transfer, authority boundaries, and repository
continuation practices.

The audit question is:

```text
What is a handoff document allowed to preserve,
and what must it avoid becoming?
```

This is an architectural boundary audit. It does not implement code, modify
schemas, change runtime behavior, alter projections, introduce observations,
change evidence handling, revise claims, create recommendations or decisions,
add capabilities, alter execution paths, or modify tests.

In scope:

- defining the architectural role of a handoff document;
- distinguishing handoff from transcript, summary, projection, architecture,
  status, roadmap, authority, and knowledge;
- identifying what continuation context should be preserved;
- identifying what a handoff must avoid preserving or duplicating;
- defining the authority boundary around handoffs;
- identifying invariants for future handoff documents.

Out of scope:

- creating a handoff schema or runtime artifact;
- creating a continuation engine, memory system, state store, or projection;
- changing repository documentation lifecycle rules;
- changing canonical architecture documents;
- deciding a particular workstream's next implementation step;
- treating this reconciliation as approval for future work.

## 2. Central finding

A handoff is a **continuation alignment artifact**.

It is not a transcript, architecture document, status board, roadmap, knowledge
store, projection, provenance substitute, or authority source.

A handoff exists to preserve enough alignment for a later operator, assistant,
or implementation agent to continue bounded work safely without re-reading the
entire interaction history or inventing authority that was never granted.

The clean boundary is:

```text
Transcript preserves conversation.
Status preserves current state.
Roadmap preserves possible or intended future sequencing.
Architecture preserves accepted structural truths.
Reconciliation preserves boundary reasoning and decision provenance.
Knowledge stores preserve supported durable knowledge.
Handoff preserves continuation alignment and points to authority.
```

The most important handoff rule is therefore:

```text
A handoff may carry context forward,
but it must not become the source of truth for that context.
```

## 3. Definition of a handoff

A handoff is a bounded document that transfers the continuation-relevant working
set from one work episode to another.

It should answer:

- What work was being continued?
- Why was that work active?
- What is the current frontier of that work?
- Which claims, decisions, questions, risks, and boundaries must remain active?
- Which documents or artifacts own the authority for those claims and decisions?
- What should the next operator or assistant avoid collapsing, repeating, or
  overextending?

A handoff is best understood as a **navigation and alignment artifact for
continuation**, not as a projection or durable knowledge structure.

It may summarize, but it is not merely a summary. A generic summary compresses
content. A handoff selects continuation-relevant content and records why that
content matters for the next step.

It may reference projections, but it is not a projection. A projection is a
structured view produced from source material under defined semantics. A handoff
is a human-authored or assistant-authored continuation guide whose safety comes
from scoped references and boundary discipline, not from projection authority.

It may reference architecture, but it is not architecture. Architecture defines
accepted structural relationships. A handoff keeps those relationships active in
the working set and points to their owners.

## 4. Purpose of a handoff

A handoff exists to preserve **continuation context**.

Continuation context includes the information needed for a later session to
resume work without losing alignment, duplicating already-settled reasoning, or
mistaking provisional material for authority.

A handoff may support continuation of:

- architectural reconciliation;
- documentation audits;
- implementation work;
- investigation chains;
- repository maintenance;
- operator-directed research;
- follow-on review of unresolved contradictions or questions.

The durable purpose is not to remember everything. It is to preserve the minimum
safe bridge between work episodes.

The bridge should preserve:

```text
intent
+ current frontier
+ active questions
+ accepted decisions
+ established claims
+ unresolved risks
+ relevant boundaries
+ authoritative references
```

It should not preserve every conversational turn, emotional tone, speculative
branch, or discarded path unless that material is necessary to prevent a known
continuation error.

## 5. Handoff and transcript

A transcript and a handoff preserve different things.

| Object | Preserves | Selection rule | Authority |
| --- | --- | --- | --- |
| Transcript | Conversation as it happened. | Chronological completeness. | Evidence of interaction history only. |
| Handoff | Continuation-relevant findings and alignment. | Relevance to safe continuation. | No independent authority; points to owners. |

A transcript belongs to interaction provenance. It can show what was asked, what
was answered, what was corrected, and what assumptions appeared during the
conversation.

A handoff belongs to continuation practice. It should not require the next reader
to replay the full conversation. It should extract the continuation-relevant
working set and cite or name the documents, commits, issues, or transcripts that
own provenance.

The distinction matters because conversation order is not the same thing as
continuation priority. A late correction may be more important than many pages of
earlier exploration. A handoff should foreground the correction; the transcript
should preserve the whole path.

Failure mode:

```text
Transcript excerpt
        ↓
Treated as current guidance
        ↓
Earlier speculation outranks later correction
```

Correct boundary:

```text
Transcript preserves what happened.
Handoff preserves what must remain active next.
```

## 6. Handoff and summary

A handoff may contain summary, but it is not reducible to summary.

A summary compresses material. It may be optimized for brevity, recall, or reader
orientation. A handoff is optimized for safe continuation.

Therefore a handoff should include information that a pure summary might omit:

- active guardrails;
- unresolved questions;
- forbidden shortcuts;
- authority references;
- known failure modes;
- the reason a frontier is active;
- what not to do next.

A handoff should also exclude information that a broad summary might include:

- full narrative history;
- interesting but inactive branches;
- duplicated architecture prose;
- unaccepted recommendations;
- speculative future work not needed for continuation.

The clean boundary is:

```text
Summary says what was covered.
Handoff says what must be carried forward.
```

## 7. Handoff and projection

A handoff is not a projection.

Projection implies a structured view over source material with defined ownership,
refresh expectations, and interpretation boundaries. A handoff is a document that
selects continuation-relevant context for the next work episode.

A handoff may reference projected state or projection outputs when those outputs
are relevant to continuation. It must not mutate projection semantics, replace
projection stores, define projection truth, or become a side-channel projection.

Boundary rule:

```text
Projected state is read through its owning projection semantics.
Handoff context is read as continuation guidance.
```

If a handoff needs a projected fact, it should point to the projection or source
that owns the fact. It should not silently copy projected content in a way that
causes the handoff to become a stale derived store.

## 8. Handoff and architecture

A handoff cannot define architecture.

A handoff cannot modify architecture.

A handoff cannot override architecture.

A handoff may summarize architecture only to the degree necessary for
continuation, and any such summary should point to the authoritative architecture
or reconciliation documents.

Architecture documents preserve accepted structural truths. Reconciliation
documents preserve scoped boundary reasoning and decision provenance. Handoffs
preserve the subset of those truths and decisions that must remain active for the
next continuation step.

The authority relationship is:

```text
Architecture owns accepted structural claims.
Reconciliation owns scoped boundary reasoning.
Handoff carries active alignment and references both.
```

A handoff becomes unsafe when it starts using its own prose as the reason that an
architectural boundary exists. The reason belongs in the architecture or
reconciliation that established the boundary. The handoff should say where to
look and why the boundary matters now.

Acceptable handoff language:

```text
Continue to preserve the Evidence before Capability Selection boundary;
see the owning architecture/reconciliation references before changing flow.
```

Unsafe handoff language:

```text
This handoff establishes a new Evidence-to-Capability architecture.
```

## 9. Handoff and knowledge

A handoff is not a knowledge store.

A handoff may preserve established claims only as continuation-relevant claims
with references to their support. It must not become the place where claims are
made durable, verified, promoted, classified, or maintained.

A handoff may carry:

- established claims that must remain active;
- claim status as understood at the time of handoff;
- pointers to supporting reconciliations, audits, architecture documents, or
  provenance;
- reminders about unsupported or disputed claims.

A handoff must not:

- replace provenance;
- replace supporting reconciliations;
- replace evidence records;
- hide claim support behind handoff prose;
- create a parallel list of durable truths;
- maintain stale copies of knowledge that has an owning document.

The correct pattern is:

```text
Claim preserved for continuation
        +
Reference to supporting authority
        +
Boundary on how the claim may be used
```

The incorrect pattern is:

```text
Claim copied into handoff
        ↓
Handoff becomes the only remembered support
        ↓
Claim loses provenance while appearing authoritative
```

## 10. Handoff and status

A handoff is not a status document.

Status documents answer where the project, concern, or workstream currently
stands. Frontier documents identify the active edge of ongoing work. Roadmaps
identify possible or intended future sequencing.

A handoff may mention status only as needed for continuation.

The clean boundary is:

| Object | Primary question |
| --- | --- |
| Status | Where does the project or concern stand now? |
| Frontier | What edge is active or next under current status? |
| Roadmap | What future paths or sequencing are possible or intended? |
| Handoff | What must be preserved so continuation is safe? |

A handoff should not duplicate status tables, maintain parallel progress
tracking, or become the current-state authority. If current state matters, the
handoff should point to the status or frontier owner and record only the portion
needed for the next operator to resume.

Failure mode:

```text
Handoff includes a status snapshot
        ↓
Snapshot becomes stale
        ↓
Next session treats stale handoff as current state
```

Correct boundary:

```text
Handoff records the continuation-relevant status assumption
and points to the status document for current truth.
```

## 11. Handoff and roadmap

A handoff is not a roadmap.

A roadmap can hold possible future work, sequencing, deferred concerns, and
strategic direction. A handoff should hold only the future-oriented information
required to continue the current bounded work safely.

A handoff may include a next step when the next step is part of continuation. It
should not broaden that into a backlog, strategy, or durable plan.

Acceptable handoff content:

- the immediate next question in a reconciliation chain;
- the next bounded implementation verification step;
- a deferred issue that blocks safe continuation;
- a reference to the roadmap when future sequencing matters.

Unsafe handoff content:

- a replacement backlog;
- broad priority ordering;
- speculative features unrelated to the active work;
- roadmap decisions without operator or architectural authority.

The clean boundary is:

```text
Roadmap sequences future possibilities.
Handoff preserves the next continuation edge.
```

## 12. Handoff and authority

A handoff does not authorize work by itself.

A handoff cannot override operator decisions, accepted architecture, repository
policy, tests, documentation lifecycle boundaries, or scoped reconciliation
findings.

A handoff can preserve that authority was granted elsewhere, but it must point to
where that authority came from.

Authority categories that a handoff may reference but not own:

- operator instruction;
- accepted architectural decision;
- canonical documentation;
- scoped reconciliation finding;
- repository status or roadmap owner;
- implementation plan approved elsewhere;
- policy or invariant document.

A handoff may say:

```text
The operator asked that the next session continue the reconciliation without
implementation changes.
```

It should not say:

```text
This handoff authorizes implementation of the reconciliation outcome.
```

Unless the authorizing source is external to the handoff and explicitly cited,
the handoff should be treated as alignment context, not permission.

## 13. Information a handoff should preserve

A handoff should preserve information when losing it would make continuation
unsafe, wasteful, or likely to cross an architectural boundary.

Recommended preserved elements:

| Element | Belongs in handoff? | Reason |
| --- | --- | --- |
| Operator intent | Yes, when relevant. | Preserves why the work exists and what constraints the operator imposed. |
| Active question | Yes. | Identifies the unresolved edge the next session should continue. |
| Current frontier | Yes, by reference and brief context. | Prevents restarting from the wrong layer or stale concern. |
| Established claim | Yes, with support reference. | Keeps important conclusions active without making the handoff the support. |
| Accepted decision | Yes, with authority reference. | Prevents relitigating settled choices while preserving provenance. |
| Important boundary | Yes. | Guards against collapse of nearby concepts. |
| Open risk | Yes. | Helps continuation avoid known unsafe assumptions. |
| Unresolved contradiction | Yes. | Prevents accidental smoothing-over of live disagreement. |
| Authoritative references | Yes. | Ensures the handoff points to owners rather than becoming owner. |
| Known failure mode | Yes. | Transfers reasoning posture, not only facts. |
| Non-goals | Yes. | Prevents scope creep during continuation. |

A good handoff is therefore not just a list of facts. It is a compact working-set
activation document.

It should preserve:

```text
what matters
+ why it matters now
+ where authority lives
+ what boundary must not be crossed
```

## 14. Information a handoff should avoid preserving

A handoff should avoid preserving material that would cause it to become a
parallel authority surface, stale store, or noisy transcript substitute.

Recommended excluded elements:

| Element | Should be excluded? | Reason |
| --- | --- | --- |
| Full conversation history | Yes. | Belongs in transcript; overwhelms continuation signal. |
| Duplicated architecture | Yes. | Creates stale parallel architecture. |
| Duplicated reconciliations | Yes. | Replaces boundary reasoning with copied conclusions. |
| Duplicated status reporting | Yes. | Creates stale parallel status. |
| Duplicated roadmap | Yes. | Creates a second planning authority. |
| Unsupported conclusions | Yes. | Makes handoff prose appear more authoritative than support allows. |
| Speculative branches | Usually. | Include only if needed to explain active risk or rejected direction. |
| Private rationale without provenance | Yes. | Cannot safely guide continuation. |
| Implementation directives without authority | Yes. | Handoff does not authorize execution. |
| Hidden policy | Yes. | Policy belongs in policy or invariant owners. |

Exclusion does not mean erasure. It means the handoff should point to the owning
artifact instead of copying or replacing it.

## 15. What must not be collapsed together

The most important conceptual risk is collapsing adjacent documentation objects
because they all seem to help the next reader.

They remain distinct:

### Transcript versus handoff

```text
Transcript preserves conversation.
Handoff preserves continuation alignment.
```

The transcript is chronological provenance. The handoff is selected working-set
activation.

### Handoff versus status

```text
Status preserves current state.
Handoff preserves what current-state assumptions matter for continuation.
```

The handoff can be stale. The status owner should be checked for current state.

### Handoff versus roadmap

```text
Roadmap preserves future possibilities and sequencing.
Handoff preserves the next continuation edge.
```

A handoff should not become a backlog.

### Handoff versus architecture

```text
Architecture preserves structural truths.
Handoff preserves active architectural guardrails by reference.
```

A handoff can remind; it cannot define.

### Handoff versus reconciliation

```text
Reconciliation preserves boundary reasoning.
Handoff preserves which boundary reasoning must remain active next.
```

A handoff should not replace the reasoning record.

### Handoff versus knowledge

```text
Knowledge stores preserve supported durable knowledge.
Handoff preserves continuation-relevant claims with references.
```

A handoff should not become the durable store or support layer.

### Handoff versus authority

```text
Authority grants permission or defines accepted truth.
Handoff records where authority already lives.
```

A handoff cannot grant authority to itself.

## 16. Handoff document shape

A safe handoff document should be short enough to remain usable and structured
enough to prevent authority drift.

A recommended shape is:

1. **Scope** — what work this handoff continues and what it does not cover.
2. **Operator intent** — relevant constraints, goals, and explicit non-goals.
3. **Current continuation frontier** — the immediate edge of the work.
4. **Established claims** — only continuation-relevant claims, each with support
   references.
5. **Accepted decisions** — decisions that should not be relitigated without new
   authority.
6. **Active questions** — unresolved questions to continue.
7. **Risks and contradictions** — known hazards and live disagreements.
8. **Boundaries and guardrails** — distinctions that must remain active.
9. **Authority references** — architecture, reconciliation, status, roadmap,
   issue, commit, or transcript references that own the relevant material.
10. **Non-goals** — what the next session should not do merely because it read
    the handoff.
11. **Next continuation step** — the bounded next action, if known.

The structure should make copied authority visible. A claim without a reference
should be treated as weak continuation context, not durable truth.

## 17. Relationship to repository continuation practice

Seed relies on long-running architectural work, audits, implementation efforts,
and continuation across operators and assistants. Handoffs are useful because
continuity can fail even when the repository contains the correct information.

The repository may contain the right architectural documents, but a new session
can still fail if the right guardrails are not active in its working set.

A handoff should therefore preserve both:

- **content alignment**: the relevant claims, decisions, and current frontier;
- **posture alignment**: the boundaries and reasoning stance needed to apply the
  content safely.

This distinction is important. A handoff that preserves only facts may still
allow the next session to combine those facts incorrectly. A handoff that
preserves posture reminds the next session which distinctions are dangerous to
collapse.

## 18. Non-goals

A handoff should not attempt to become:

- canonical architecture;
- a durable knowledge base;
- a source-of-truth registry;
- a planning system;
- a roadmap;
- a status dashboard;
- a transcript archive;
- an evidence store;
- a projection cache;
- an authorization mechanism;
- a policy document;
- an implementation prompt that bypasses review.

A handoff also should not be used to launder unsupported ideas into apparent
repository truth. If a claim is not supported elsewhere, the handoff should label
it as unresolved, speculative, or operator intent rather than presenting it as
established architecture.

## 19. Implementation implications

This reconciliation does not require implementation work.

The documentation implication is that future handoff documents should be written
as continuation alignment artifacts and should explicitly point to authority.

Potential low-risk documentation practices, if future work chooses to adopt
them, include:

- using a consistent handoff heading structure;
- labeling handoff non-goals;
- separating active questions from accepted decisions;
- separating status assumptions from status authority;
- requiring references for established claims;
- identifying which documents own architecture, roadmap, status, or provenance.

These practices do not imply schema changes, runtime changes, projections, tests,
or new repository machinery.

## 20. Architectural invariants

The findings support the following invariants:

- Handoffs preserve continuation context.
- Handoffs preserve continuation alignment, not complete history.
- Handoffs do not replace transcripts.
- Handoffs do not replace authoritative documents.
- Handoffs should reference authority rather than become authority.
- Handoffs do not define, modify, or override architecture.
- Handoffs do not replace reconciliations or their boundary reasoning.
- Handoffs do not replace provenance or evidence.
- Handoffs do not become knowledge stores.
- Handoffs do not become status documents.
- Handoffs do not become roadmaps.
- Handoffs cannot authorize work by themselves.
- Handoffs should preserve active questions.
- Handoffs should preserve established claims only with support references.
- Handoffs should preserve accepted decisions only with authority references.
- Handoffs should preserve important boundaries and guardrails.
- Handoffs should identify non-goals and excluded interpretations.
- Handoffs should enable safe continuation across operators, assistants, and
  implementation agents.

## 21. Conclusion

A handoff is the repository's continuation bridge, not its authority center.

It should keep the next session aligned with the work's intent, frontier,
questions, claims, decisions, risks, and boundaries. It should do this by
pointing to architecture, reconciliations, status documents, roadmaps,
transcripts, and evidence stores rather than replacing them.

The safe handoff posture is:

```text
Preserve what the next session must carry.
Name what owns the authority.
Do not turn continuation context into durable truth.
```
