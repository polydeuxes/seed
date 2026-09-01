# Handoff Template And Continuation Protocol Reconciliation

## 1. Purpose and scope

This document reconciles Seed's documentation boundary for handoff structure,
continuation protocols, continuation safety, alignment preservation, and
cross-session architectural continuity.

It answers the narrow architectural question:

```text
What normalized shape should a handoff have, and how should a future session
safely continue from it without treating it as authority?
```

This is a documentation-only reconciliation. It does not implement code, modify
schemas, change runtime behavior, alter projections, observations, evidence
handling, claims, recommendations, decisions, capabilities, execution paths, or
tests.

The reconciliation assumes the prior boundary finding that a handoff is a
continuation-alignment artifact. It is not a transcript, not architecture, not a
status document, not a roadmap, not a knowledge store, and not a proof surface.

## 2. Central finding

A handoff preserves enough alignment for a future operator, assistant,
implementation agent, or session to resume safely.

A handoff should therefore be structured as a compact continuation artifact that
records:

- the operator's active intent;
- the current frontier of work;
- the questions still open;
- the established claims and accepted decisions that must not be silently
  re-litigated;
- the boundaries that prevent category collapse;
- the authoritative references the consumer must inspect;
- the repository state or state-validation step needed before acting;
- the next safe moves and the unsafe moves to avoid.

A handoff does not become the source of architectural truth. It points to the
sources that carry authority. Its usefulness depends on being smaller, more
situated, and more disposable than the documents it references.

The current handoff model must also make activation explicit. Safe continuation
is not established by possession of a handoff artifact alone:

```text
Handoff availability
        -> handoff consumption
        -> bootstrap activation
        -> continuation compliance
```

A handoff can be available without being consumed, consumed without being
activated, and activated without full compliance. Successful continuation
therefore requires reading the required bootstrap, making it active working
state, validating references and repository state, and behaving within the
validated continuation constraints.

## 3. Definitions

### 3.1 Handoff

A handoff is a bounded continuation-alignment artifact created at a session,
operator, or work-boundary transition.

Its job is to preserve continuity across discontinuity. It tells the next
consumer what must be remembered to avoid losing alignment, repeating settled
boundary reasoning, or accidentally collapsing distinct document roles.

A handoff may summarize claims, decisions, risks, and frontiers, but those
summaries are navigational. They do not replace architecture, ontology,
reconciliation papers, status documents, roadmaps, repository state, code, tests,
or evidence records.

### 3.2 Handoff template

A handoff template is the normalized structure used to create handoff documents.

It defines expected sections, required fields, optional fields, and excluded
content. It is a shape constraint, not a specific session artifact. A template
answers:

```text
What categories of continuation information should a handoff contain?
```

A template differs from a handoff document because the template is reusable
structure while a handoff document is a concrete instance populated for a
specific transition.

A template differs from a protocol because the template defines what is written,
while the protocol defines what a consumer does with what was written.

### 3.3 Handoff document

A handoff document is a concrete artifact produced from a template for a
particular transition.

It contains situated content: this operator intent, these active questions, this
frontier, these accepted decisions, these references, this repository state, and
these next safe moves.

It may be superseded, archived, corrected, or declared stale. It is not a
canonical store of durable architecture.

### 3.4 Continuation protocol

A continuation protocol is the safe-consumption and activation procedure a future
session follows when receiving a handoff.

It answers:

```text
What should a consumer validate, read, preserve, and avoid before continuing?
```

A protocol is procedural rather than structural. It does not define the handoff's
section order; it defines the minimum review, activation, and validation behavior
necessary to avoid unsafe continuation.

### 3.5 Handoff availability

Handoff availability means the continuation artifact exists and can be accessed.
Availability does not imply that the artifact was read, understood, activated, or
used compliantly.

### 3.6 Handoff consumption

Handoff consumption means the required bootstrap is read and the references
required by the continuation protocol are identified. Consumption does not imply
that the consumed content becomes active working state.

### 3.7 Bootstrap activation

Bootstrap activation means the consumed bootstrap content enters the consumer's
active working state and affects continuation behavior. Activation is not
authority; it activates the need to consult authority.

### 3.8 Continuation compliance

Continuation compliance means behavior follows validated references, validated
repository state, operator intent, current frontier, preserved boundaries, and
known risks. Compliance is not blind obedience to handoff prose.

## 4. Required continuation information

The following information should survive continuation when applicable.

| Information | Required? | Reason |
| --- | --- | --- |
| Operator intent | Required | Preserves why work is being continued and prevents the next session from optimizing for an unrelated goal. |
| Active questions | Required | Preserves unresolved inquiry and prevents premature closure. |
| Current frontier | Required | Identifies the exact boundary of ongoing work and prevents broad, unbounded continuation. |
| Established claims | Required when claims constrain continuation | Preserves settled findings that would be costly or unsafe to silently reinterpret. |
| Accepted decisions | Required when decisions constrain continuation | Preserves operator- or architecture-accepted choices without turning them into proof. |
| Unresolved contradictions | Required when known | Preserves known tension so future work does not erase it by omission. |
| Open risks | Required when known | Preserves safety, architecture, documentation, or implementation hazards relevant to next action. |
| Preserved boundaries | Required | Protects category separation, authority boundaries, and non-goals. |
| Authoritative references | Required | Keeps the handoff subordinate to source documents, repository state, and evidence surfaces. |
| Repository state | Required as a reference or validation instruction | Continuation must know what state was assumed or that state must be rechecked. |
| Continuation activation | Required | Tells the consumer to use the handoff as live continuation guidance rather than as a review, summary, or critique task. |
| Next safe moves | Required for operational handoffs | Constrains continuation to actions consistent with intent and boundaries. |
| Explicit non-goals / do-not-collapse notes | Required when category confusion is likely | Prevents handoff content from absorbing architecture, status, roadmap, transcript, or evidence roles. |

The requirement is conditional in one sense: a handoff should not invent a risk,
contradiction, claim, or decision merely to fill a section. If none is known, the
handoff should say so briefly or mark the section as not applicable. Silence is
less safe than an explicit absence marker because silence may be mistaken for
forgetfulness.

## 5. Information that may be omitted or should not survive

A handoff should omit information that does not materially preserve safe
continuation.

The following content should usually not survive inside the handoff:

- full conversation history;
- long transcripts;
- repeated architectural arguments already preserved in reconciliation documents;
- implementation details not needed for the next continuation boundary;
- duplicated reconciliation text;
- duplicated status reporting;
- duplicated roadmaps;
- exhaustive evidence records;
- complete code walkthroughs;
- speculation not tied to active questions or safe next moves.

The reason is not that this information is always valueless. The reason is that
embedding it in the handoff changes the handoff's role. A transcript should
preserve conversation, an architecture document should preserve structural truth,
a roadmap should preserve future possibilities, and a reconciliation should
preserve boundary reasoning. A handoff should preserve continuation alignment.

A handoff may include a short pointer to omitted material when omission could
otherwise appear as loss:

```text
Detailed argument omitted; see the referenced reconciliation.
```

This keeps the handoff useful without turning it into a duplicate authority.

## 6. Relationship to authoritative documents

A handoff references authority; it does not replace authority. Activation also
is not authority: activating a bootstrap makes its constraints live in working
state, but the handoff still loses when it diverges from authoritative
references. Compliance means validating and following the appropriate authority
process, not obeying handoff prose blindly. If authoritative references diverge,
the consumer should use the appropriate reconciliation or authority process.

### 6.1 Architecture

Architecture documents preserve structural truths and durable system boundaries.
A handoff may summarize the architectural constraint relevant to continuation,
but the summary is subordinate to the architecture document. If the two conflict,
the consumer must inspect the architecture document and repository state rather
than treating the handoff as the winner.

### 6.2 Ontology

Ontology documents preserve vocabulary, entity distinctions, and semantic
relationships. A handoff may use ontology terms, but it must not redefine them.
If a term is ambiguous, the handoff should point to the ontology or vocabulary
source that owns the term.

### 6.3 Reconciliations

Reconciliation documents preserve boundary reasoning and architectural case law.
A handoff may record the result of a reconciliation as an established claim or
accepted decision, but it should link or cite the reconciliation instead of
copying its argument wholesale.

### 6.4 Status

Status documents preserve current state. A handoff may record the state assumed
at the transition or instruct the consumer to revalidate state. It should not
become a parallel status report.

### 6.5 Roadmap

Roadmap documents preserve future possibilities and sequencing candidates. A
handoff may identify next safe moves, but those moves are local continuation
guidance. They should not become a roadmap unless promoted through the roadmap's
own authority process.

### 6.6 Repository state

Repository state is validated by inspecting the repository, branch, commit,
working tree, tests, and relevant files. A handoff may record a commit hash,
branch name, dirty/clean state, or validation command, but those values can go
stale. A continuation protocol must require revalidation before implementation or
architecture-sensitive decisions.

## 7. Continuation protocol

When a future session receives a handoff, it should proceed in this order:

1. **Recognize the consumption stages.** Treat safe continuation as
   availability -> consumption -> activation -> compliance, not as artifact
   possession alone.
2. **Read and activate the continuation activation section.** Establish that the
   handoff is live continuation guidance for working state, not the task to
   review, summarize, or critique unless explicitly asked.
3. **Identify the handoff type and scope.** Determine whether the handoff is an
   architectural, implementation, review, operator, incident, or exploratory
   handoff. Do not assume that one type grants authority belonging to another.
4. **Validate authoritative references.** Open the referenced architecture,
   ontology, reconciliation, status, roadmap, and repository files needed for the
   task. Confirm that the files still exist and appear relevant.
5. **Confirm repository state.** Check branch, working tree, relevant files, and
   task-specific tests or generated artifacts before relying on recorded state.
6. **Review operator intent.** Preserve the active goal before selecting next
   actions.
7. **Review active questions and current frontier.** Continue from the frontier;
   do not widen the task merely because adjacent work is visible.
8. **Review established claims and accepted decisions.** Treat them as preserved
   alignment cues, then verify against authority when they materially constrain
   action.
9. **Review important boundaries and non-goals.** Identify what must not be
   collapsed, implemented, modified, or reinterpreted.
10. **Review open risks and contradictions.** Carry them forward explicitly or
    resolve them through the appropriate authoritative process.
11. **Select next safe moves.** Choose actions that are consistent with the
    validated references, repository state, operator intent, and preserved
    boundaries.
12. **Record deviations.** If continuation diverges from the handoff, explain
    why and point to the newer authority, newer repository state, or operator
    instruction that justifies the divergence.

This protocol makes the handoff a starting point, not an endpoint.

## 8. What a handoff consumer must not do

A handoff consumer should not:

- treat the handoff as architecture;
- treat the handoff as ontology;
- treat the handoff as authority;
- treat the handoff as proof;
- treat the handoff itself as the task to review, summarize, or critique unless
  explicitly asked;
- treat a summarized claim as evidence;
- ignore referenced documents;
- ignore repository state;
- silently reinterpret established claims;
- silently drop active questions;
- convert next safe moves into roadmap commitments;
- convert open risks into accepted decisions;
- collapse implementation details into architectural truth;
- use stale handoff state as current state without validation;
- expand scope beyond the current frontier without operator or architectural
  justification.

The safe continuation boundary is:

```text
Use the handoff to know where to look, what to preserve, and what to avoid.
Use authoritative documents, repository state, evidence, and operator decisions
to determine what is true or permitted now.
```

## 9. Minimum safe handoff

The smallest handoff capable of preserving alignment is:

```text
Continuation Activation
Continuation Bootstrap
Authoritative References
Activity Context / Working State
Optional Historical Summary
```

This minimum is safe only when established claims, accepted decisions,
contradictions, and risks are either absent or already fully captured by the
referenced authority. If any of those items materially constrain continuation,
they must be added explicitly.

The minimum safe handoff should remain short. Its purpose is to prevent immediate
misalignment, not to preserve all context. The optional historical summary should
remain physically last and removable without invalidating continuation safety.

## 10. Ideal handoff for long-running architectural work

For long-running architectural work, the preferred template is:

```text
# Handoff: <short name>

## Continuation Activation

You are the continuation participant.

Do not review this handoff as the task unless explicitly asked.

Do not summarize this handoff as the task unless explicitly asked.

Do not critique this handoff as the task unless explicitly asked.

Use this handoff to establish working state.

Validate authoritative references.

Validate repository state.

Continue from the Next Safe Move.

## Continuation Bootstrap

### Handoff Type

### Operator Intent

### Current Frontier

### Active Questions

### Established Claims

### Accepted Decisions

### Important Boundaries

### Open Risks / Unresolved Contradictions

### Next Safe Moves

### Do Not Collapse

## Authoritative References

### Repository State / Revalidation Instruction

## Activity Context / Working State

## Optional Historical Summary
```

### 10.1 Evaluation of the potential template

The proposed template is mostly correct:

```text
Handoff Type
Operator Intent
Active Questions
Current Frontier
Established Claims
Accepted Decisions
Important Boundaries
Authoritative References
Repository State
Open Risks
Next Safe Moves
Do Not Collapse
```

It contains the necessary alignment, frontier, authority, and safety categories.
The reconciliation adds two refinements:

1. **Open risks and unresolved contradictions should be grouped or adjacent.**
   Both preserve hazards that must not disappear, but they should not be confused
   with accepted claims or accepted decisions.
2. **Omitted context should be explicit.** A handoff benefits from naming what it
   intentionally excludes, especially when full transcripts, duplicated
   reconciliations, or roadmap detail are available elsewhere.
3. **Activation should precede bootstrap.** A small required activation section
   tells the consumer to use the handoff to establish working state and continue,
   not to treat the handoff itself as the task.
4. **Optional summary should remain physically last.** Historical context stays
   removable and cannot bury required bootstrap content.

The template should remain a documentation convention unless a future, separate
reconciliation establishes a need for schema or runtime representation. This
document does not establish that need.

## 11. Distinct document roles that must not collapse

The following artifacts remain distinct because each preserves a different kind
of continuity or authority.

| Artifact | Preserves | Why it must remain distinct from handoff |
| --- | --- | --- |
| Transcript | Conversation | A transcript records what was said; a handoff records what must survive for safe continuation. |
| Architecture | Structural truths | Architecture owns durable system structure; a handoff only points to relevant structural authority. |
| Ontology | Vocabulary | Ontology owns terms and semantic distinctions; a handoff uses those terms without redefining them. |
| Status | Current state | Status records current condition; a handoff records assumed state or validation needs at a transition. |
| Roadmap | Future possibilities | Roadmap records candidate future work; a handoff records local next safe moves. |
| Reconciliation | Boundary reasoning | Reconciliation preserves why a boundary exists; a handoff preserves that the boundary matters now. |
| Handoff | Continuation alignment | Handoff bridges sessions; it is intentionally smaller and less authoritative than the referenced materials. |

Collapsing these roles creates predictable failures:

- transcripts become treated as decisions;
- summaries become treated as proof;
- roadmaps become treated as commitments;
- status becomes treated as architecture;
- handoffs become stale knowledge stores;
- future sessions continue from memory rather than authority.

## 12. Handoff lifecycle

### 12.1 Creation

A handoff is created when a transition risks loss of alignment: session end,
operator change, agent change, branch handoff, review handoff, or a pause in
long-running architectural work.

Creation should be concise and reference-heavy. It should preserve only the
continuation-critical subset of context.

### 12.2 Consumption

A handoff is consumed through the continuation protocol. Consumption should read
the required bootstrap and identify references, then activation should make the
bootstrap part of active working state. Compliance should validate references and
repository state before action and continue within operator intent, frontier,
boundaries, and risks.

A concise failure mode to preserve is:

```text
handoff available
bootstrap partially consumed
references not validated
bootstrap not activated
optional summary or prose interpreted
continuation misrouted
```

### 12.3 Supersession

A handoff can be superseded by a newer handoff, newer operator instruction,
newer reconciliation, newer status document, newer roadmap entry, or changed
repository state.

Supersession does not mean the older handoff was wrong. It means the older
handoff no longer represents the best continuation artifact for the current
transition.

### 12.4 Archival

A handoff can be archived when it is no longer needed for active continuation but
remains useful as historical context. Archived handoffs should be treated like
history, not active guidance.

### 12.5 Staleness

A handoff can become stale because references moved, repository state changed,
operator intent changed, architecture evolved, risks were resolved, or active
questions were answered.

Staleness is not failure. It is a normal lifecycle property of transition
artifacts.

### 12.6 Continued usefulness after architecture evolves

A stale handoff may remain useful as a record of prior frontier, prior intent,
and prior boundary concerns. It should not be used to override newer authority.
Its safe use after architecture evolves is diagnostic and historical:

```text
Why was the prior session aligned this way?
What questions were active then?
Which boundaries were considered important at that transition?
```

## 13. Architectural invariants

This reconciliation supports the following architectural invariants:

- A handoff preserves continuation alignment.
- A handoff points to authority.
- A handoff does not replace authority.
- A handoff is smaller than the authority it references.
- A handoff should preserve operator intent.
- A handoff should preserve active questions.
- A handoff should preserve the current frontier.
- A handoff should preserve established claims when they constrain
  continuation.
- A handoff should preserve accepted decisions when they constrain continuation.
- A handoff should preserve important boundaries.
- A handoff should preserve authoritative references.
- A handoff should preserve known open risks and unresolved contradictions.
- A handoff should not preserve unnecessary history.
- A handoff should not duplicate transcripts, architecture, status, roadmaps, or
  reconciliation arguments.
- A handoff should enable safe continuation.
- Handoff availability, consumption, bootstrap activation, and continuation
  compliance are distinct stages.
- Bootstrap activation is necessary for safe continuation but does not create
  authority.
- Continuation compliance is not blind obedience to handoff prose.
- A continuation protocol validates references before relying on handoff
  summaries.
- A continuation protocol validates repository state before acting on recorded
  repository assumptions.
- A handoff may be superseded, archived, or stale without losing historical
  usefulness.

## 14. Non-goals

This reconciliation does not:

- define a runtime handoff object;
- define a persistence schema;
- require projection changes;
- require observation changes;
- require evidence-model changes;
- require claim-model changes;
- require decision-model changes;
- require capability or execution changes;
- require tests;
- require generated documentation;
- promote any specific future implementation;
- make handoffs authoritative.

## 15. Implementation implications

No implementation work is directly required by these findings.

The only immediate implication is documentation practice: future handoff
artifacts should use the normalized template or the minimum safe handoff shape,
and future sessions should consume handoffs through the continuation protocol.

If a later effort proposes schema, runtime, projection, or tooling support for
handoffs, that effort should begin with a separate reconciliation because this
document intentionally stops at the architectural documentation boundary.
