# Continuation Constraints And Consumer Capabilities Reconciliation

## Purpose

This document performs a documentation-only reconciliation of continuation
constraints, consumer capabilities, participant limitations, known defects,
environmental restrictions, continuation safety, and continuation-aware
operation.

It is an architectural boundary audit.

It does not implement code, modify schemas, change runtime behavior, alter
authority systems, change handoff execution behavior, modify continuation
protocols, alter observations, claims, projections, recommendations, decisions,
commands, actions, ontology definitions, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent continuation work exposed a practical failure mode:

```text
A continuation participant consumed and activated a handoff,
but the participant had a known tooling limitation:

repository-wide search unavailable
```

The specific limitation is not the architectural point. The deeper question is:

```text
Should continuation preserve knowledge about participant capabilities,
constraints, and known limitations when those limitations affect safe
continuation?
```

## Central Finding

Yes, with strict boundaries.

Continuation participants may possess capabilities, constraints, limitations,
and known defects that materially affect continuation behavior. If those facts
are relevant to whether a future participant can safely continue the requested
work, they may be preservation-worthy continuation metadata.

However:

```text
Capabilities are not authority.
Constraints are not architecture.
Limitations are not activity context.
Defects are not ontology.
Consumer knowledge is not repository knowledge.
```

The safe architectural boundary is:

```text
Repository truth / architecture / authority
        remain independent from
Consumer capability / constraint / defect awareness
        which may affect
Continuation safety and next safe operation
```

A participant can be fully aligned and still constrained. A participant can be
compliant with authority and still unable to perform the task. Safe continuation
therefore depends not only on knowing what should be done, but also on knowing
whether the current or expected participant can actually perform the required
continuation moves.

## Scope And Non-Goals

In scope:

- defining continuation constraints, consumer capabilities, limitations, known
  defects, continuation safety, and yellow-tag operational metadata;
- distinguishing those concepts from authority, architecture, activity context,
  summary, permission, ontology, and repository knowledge;
- identifying when participant limitations become continuation-relevant;
- identifying what information may be preserved across handoffs when it affects
  safe continuation;
- identifying what should not be preserved;
- preserving conceptual invariants for future continuation work.

Out of scope:

- implementing a continuation-constraint object;
- adding or changing schemas;
- changing handoff files, handoff execution, or continuation protocols;
- changing authority systems or permission models;
- changing repository truth, ontology definitions, claims, projections,
  recommendations, decisions, commands, actions, or tests;
- creating new runtime semantics for detecting, storing, or enforcing
  constraints;
- recommending implementation work beyond the conceptual implications directly
  supported by this reconciliation.

## Definitions

### Participant

A participant is the agent, human, service, or session attempting to continue
work across a boundary.

A participant may consume a handoff, activate a bootstrap, validate references,
inspect repository state, execute tools, or perform follow-up work. The
participant is the actor at the continuation boundary, not the authority for the
architecture merely by participating.

### Consumer

A consumer is a participant in the role of receiving and using continuation
material.

Consumer emphasizes the use of a handoff, bootstrap, summary, repository state,
or other continuation input. The same entity may later become a producer when it
creates a new handoff. Consumer state is the consumer's local or environmental
state; it is not automatically repository state.

### Consumer Capability

A consumer capability is an ability available to a continuation consumer that may
be used to perform continuation work.

Examples include:

```text
read repository files
search the repository
run tests
inspect branch state
access runtime logs
use a connector
open a deployment environment
write files
commit changes
```

A capability answers:

```text
What can this consumer do?
```

It does not answer:

```text
What is true?
What is permitted?
What is architecturally correct?
What should be done?
```

Capability differs from authority because authority determines accepted truth,
valid decision surfaces, or allowed governance boundaries. Capability only
indicates operational ability. A consumer may be capable of editing a file
without having authority to redefine architecture. A consumer may have authority
to follow an instruction but lack the capability to execute a required check.

### Continuation Constraint

A continuation constraint is a continuation-relevant condition on a participant,
consumer, environment, tool, connector, context window, or access surface that
may materially affect whether the continuation can proceed safely.

A continuation constraint answers:

```text
What condition limits or shapes safe continuation for this participant or
handoff transition?
```

Examples include:

```text
repository-wide search unavailable
read-only repository access
runtime unavailable
missing deployment access
limited context window
partial repository visibility
missing branch visibility
connector failure
known stale metadata
required workaround for a broken tool
```

A continuation constraint differs from authority because it does not define what
is true or allowed. It differs from architecture because it does not describe the
system's intended design. It differs from activity context because it describes
what the participant can currently do, not what the participant was doing. It
differs from summary because it is not historical narrative; it is operational
metadata needed to continue safely.

### Limitation

A limitation is an absence, reduction, or restriction in a participant's
capability or environment.

Examples include:

```text
search unavailable
runtime unavailable
repository unavailable
context constrained
network unavailable
write access unavailable
credentials unavailable
```

A limitation becomes continuation-relevant when losing awareness of it could
cause a future participant to make an unsafe, misleading, incomplete, or
materially inefficient continuation move.

Continuation relevance depends on the task. For example:

- search unavailable is continuation-relevant for repository-wide audits,
  refactors, or duplicate-authority checks;
- runtime unavailable is continuation-relevant when the next safe move requires
  running the system or tests;
- repository unavailable is continuation-relevant for implementation work;
- context constrained is continuation-relevant when the consumer must preserve a
  narrow active bootstrap or avoid broad historical replay.

A limitation is not continuation-relevant merely because it exists. A missing
capability should be preserved only when it materially affects the next safe
moves, required verification, interpretation of incomplete work, or workarounds.

### Known Defect

A known defect is a recognized malfunction, incorrect behavior, stale condition,
or unreliable surface in a participant's tool, connector, metadata source, or
environment.

Examples include:

```text
broken search
incomplete indexing
connector failure
stale metadata
incorrect branch listing
flaky runtime access
misreported file visibility
```

A defect differs from an ordinary limitation because it is not merely the absence
of a capability. It is a capability or information source that appears present
but is known to be unreliable, broken, incomplete, stale, or misleading.

The safety risk is therefore different:

```text
Limitation: the consumer cannot do something.
Defect: the consumer may believe it can do something, but the result is unsafe
        to trust without qualification.
```

Defects are especially continuation-relevant when a future participant might
otherwise treat a failed search, stale index, missing connector result, or
partial metadata view as evidence about repository truth.

### Authority

Authority is the accepted source or boundary for determining architectural
truth, repository truth, policy validity, permitted execution, or decision
legitimacy within a given scope.

Continuation constraints do not create, remove, or modify authority. They may
say that a participant cannot inspect an authoritative source, cannot execute an
authorized action, or must use a workaround to validate authority. They must not
turn that inability into a new architectural fact.

### Continuation Context

Continuation context is the active alignment information needed to resume work
safely across a boundary.

It may include operator intent, current frontier, authoritative references,
known risks, active constraints, next safe moves, and unsafe moves. Continuation
context is selected by whether losing it would likely cause a future participant
to continue the wrong task, violate a boundary, rely on the wrong authority, or
misinterpret the state of work.

### Working State

Working state is the information currently active in the participant's reasoning
and operation.

A handoff can be available and consumed without all relevant content entering
working state. Continuation constraints matter only when they are active enough
to influence behavior. A preserved warning that is not activated may fail to
protect safe continuation.

### Activity Context

Activity context describes what the participant was doing, why it was doing it,
what had been tried, what was in progress, and what remained unfinished.

Activity context answers:

```text
What was I doing?
```

Continuation constraints answer:

```text
What can I currently do, not do, or not safely trust while continuing?
```

The two can interact, but they should not be collapsed. A note that the prior
participant was auditing repository-wide references is activity context. A note
that repository-wide search was unavailable is a continuation constraint.

### Continuation Safety

Continuation safety is the condition in which a participant can continue work
without losing the operator's intent, violating active boundaries, inventing
authority, treating incomplete evidence as complete, or taking actions that are
unsafe given the validated context and the participant's actual capabilities.

Continuation safety depends partly on awareness of participant constraints.

A participant may know the correct architecture and still be unsafe to proceed
if it cannot inspect required files, cannot run required checks, cannot access
runtime state, or is using a defective connector whose results may be incomplete.
The risk is not architectural disagreement; it is unsafe continuation under
incorrect capability assumptions.

## Reconciliation By Question

### 1. What Is A Continuation Constraint?

A continuation constraint is operationally relevant metadata about a participant
or environment that shapes safe continuation across a handoff or session
boundary.

It differs from authority because it does not decide truth or permission. It
differs from architecture because it is not a design statement about the system.
It differs from activity context because it is not a record of what work was
being performed. It differs from summary because it is not historical
explanation.

The defining test is:

```text
Would a future participant make a materially less safe continuation decision if
this condition were omitted?
```

If yes, the condition may be a continuation constraint.

### 2. What Is A Consumer Capability?

A consumer capability is an operational ability available to the consumer at the
time of continuation.

Capabilities are not authority. They do not establish truth, justify action, or
create permission. They only affect what operations the consumer can perform and
which verification paths are available.

Capability can be narrower than permission and broader than authority:

```text
A consumer may be technically able to edit a file but not authorized to redefine
architecture.

A consumer may be permitted to continue a task but unable to run the required
runtime.
```

### 3. What Is A Limitation?

A limitation is a missing or restricted capability or environmental condition.

A limitation becomes continuation-relevant when it affects:

- the next safe move;
- required validation;
- the interpretation of incomplete evidence;
- the trustworthiness of an attempted operation;
- the feasibility of the requested work;
- required workarounds;
- whether a handoff should warn the next participant.

Non-impacting limitations should not be preserved merely for completeness.

### 4. What Is A Known Defect?

A known defect is a recognized unreliable or malfunctioning capability,
connector, tool, metadata source, or environment surface.

Defects differ from limitations because they may produce false confidence. A
missing search capability is a limitation. A search capability that silently
omits files is a defect. The latter is often more dangerous because a consumer
may treat its output as complete.

Known defects should be preserved when they affect evidence quality, required
verification, safe tool use, or interpretation of prior results.

### 5. What Is Continuation Safety?

Continuation safety is safe continuation under both conceptual and operational
conditions.

Conceptual safety requires correct intent, authority, boundaries, and frontier.
Operational safety requires awareness of whether the participant can inspect,
verify, execute, or trust the surfaces needed for the next move.

Therefore continuation safety may depend on awareness of participant
constraints. The architecture need not make constraints authoritative to
recognize that unsafe capability assumptions can cause continuation failure.

### 6. What Information Should Be Preserved?

Continuation should preserve capability and constraint information when it is
material to safe continuation.

Preservation-worthy information may include:

- capabilities required for the next safe move;
- capabilities known to be unavailable;
- constraints that affected prior work or will affect follow-up work;
- known defects in tools, connectors, indexes, metadata, runtime access, or
  repository visibility;
- temporary outages when the outage affects pending validation or execution;
- environmental assumptions that a future participant might otherwise treat as
  stable fact;
- required workarounds;
- evidence caveats caused by constrained or defective tools;
- explicit warnings that prior observations were partial because of a
  limitation.

The preservation rule is impact-based:

```text
Preserve the condition if omission could cause unsafe continuation, false
confidence, duplicated failed effort, or misinterpretation of evidence.
```

### 7. What Should Not Be Preserved?

Continuation should not preserve limitation details that do not affect the work.

Examples of information that should usually not be preserved:

- irrelevant implementation details of a tool failure;
- transient noise that has no bearing on next safe moves;
- non-impacting limitations unrelated to the current task;
- generic complaints about environment quality;
- historical debugging details once the actionable constraint has been stated;
- broad inventories of every unavailable capability;
- speculation about defects that were not observed or material;
- details that would encourage treating consumer state as repository truth.

The exclusion rule is also impact-based:

```text
Do not preserve a condition solely because it happened. Preserve it only when it
changes safe continuation behavior.
```

### 8. Relationship To Activity Context

Activity context and continuation constraints answer different questions.

```text
Activity context:
What was I doing?

Continuation constraints:
What can I currently do, not do, or not safely trust?
```

The distinction matters because a future participant may need to continue the
same activity under different constraints, or may inherit the same constraints
while doing a different activity.

For example:

```text
Activity context: auditing all references to handoff activation.
Continuation constraint: repository-wide search unavailable; file discovery was
manual and may be incomplete.
```

The activity explains the goal. The constraint qualifies evidence and next safe
operation.

### 9. Relationship To Authority

Continuation constraints do not modify architectural truth.

A consumer limitation may prevent access to an authoritative source, but it does
not replace that source. A defective connector may make an observation
unreliable, but it does not change repository state. Missing runtime access may
block verification, but it does not prove runtime behavior.

The boundary is:

```text
Authority determines what counts as accepted truth or permitted action.
Constraint awareness determines how safely a participant can attempt to consult,
validate, or act under that authority.
```

A continuation constraint may require caution, deferral, workaround, or explicit
qualification. It must not become an alternative authority system.

### 10. What Should Not Be Collapsed Together?

The following distinctions should remain explicit.

| Distinction | Why it matters |
| --- | --- |
| Capability != Authority | Ability to perform an operation does not determine truth, permission, or architectural correctness. |
| Constraint != Architecture | A local limitation is not the system's intended design. |
| Defect != Ontology | A broken connector or stale index does not redefine the domain model. |
| Limitation != Activity Context | Inability to perform an operation is different from the work being attempted. |
| Constraint != Summary | Operational caution metadata is different from historical narrative. |
| Capability != Permission | Technical ability and authorization can diverge. |
| Consumer Knowledge != Repository Knowledge | What a participant knows, lacks, or mis-sees is not automatically true of the repository. |
| Known Defect != Negative Evidence | A failed or incomplete operation through a defective surface should not be treated as proof of absence. |
| Constraint Awareness != Enforcement | Preserving a warning is not the same as implementing runtime enforcement. |
| Workaround != Architecture | A local path around a limitation should not become the architectural definition of the system. |

These distinctions prevent continuation metadata from becoming accidental
authority, accidental ontology, or accidental repository truth.

## Yellow Tags Versus Red Tags

The red-tag / yellow-tag analogy is useful if kept operational rather than
authoritative.

```text
Red Tag:
Do not operate.

Yellow Tag:
Operation allowed,
but known limitation requires awareness.
```

Continuation constraints usually behave more like yellow tags than red tags.
They do not necessarily prohibit continuation. They warn that continuation is
safe only if the participant accounts for a known limitation, defect, outage, or
restricted capability.

Examples:

```text
Yellow tag: repository-wide search unavailable.
Meaning: continue, but do not claim exhaustive repository coverage unless an
alternative discovery path was used and qualified.

Yellow tag: runtime unavailable.
Meaning: continue documentation or static analysis if appropriate, but do not
claim runtime validation.

Yellow tag: connector metadata stale.
Meaning: continue only with caveats or refresh through an authoritative path
before relying on the metadata.
```

Some constraints may rise to red-tag behavior for a specific task:

```text
Task requires deployment access + deployment access missing = do not perform the
deployment step.

Task requires modifying files + repository is read-only = do not claim the
implementation is complete.
```

The tag color is therefore task-relative. The same limitation may be yellow for
one continuation and red for another. This reinforces that constraints are
operational caution metadata, not global authority boundaries.

## Preservation Boundary

Continuation preservation should be minimal, material, and qualified.

A useful preservation shape is:

```text
Constraint / capability / defect:
  - What is the condition?
  - What work does it affect?
  - What must not be inferred because of it?
  - What workaround, if any, was used or is required?
  - Is it temporary, known-defective, or an inherent access limitation?
```

Preservation should avoid broad self-reporting. The goal is not to create a
complete profile of the participant. The goal is to prevent unsafe continuation
caused by incorrect assumptions about what the participant could do or safely
trust.

## Authority Boundary

The authority boundary is strict:

- continuation constraints may qualify how evidence was collected;
- continuation constraints may explain why verification was deferred;
- continuation constraints may identify required workarounds;
- continuation constraints may warn a future participant not to over-read prior
  observations;
- continuation constraints must not redefine architecture;
- continuation constraints must not mutate repository truth;
- continuation constraints must not authorize otherwise unauthorized work;
- continuation constraints must not become ontology definitions;
- continuation constraints must not convert absence of evidence into evidence of
  absence.

The repository remains the repository. Architecture remains architecture.
Authority remains authority. Consumer constraints only affect the safety and
interpretation of continuation behavior.

## Implementation Implications

This reconciliation does not recommend implementation work.

The architectural implication is conceptual:

```text
Continuation-aware operation should treat material participant constraints as
safety-relevant metadata while preserving their non-authoritative status.
```

If future implementation work is considered, it should preserve the boundaries
identified here. In particular, it should not make capability metadata an
authority source, should not treat constraint records as repository facts, and
should not conflate warnings with enforcement.

## Architectural Invariants

The findings support the following invariants:

1. Continuation participants possess capabilities and constraints.
2. Capabilities are not authority.
3. Constraints are not architecture.
4. Limitations may be continuation-relevant when they affect safe continuation.
5. Known defects may be more safety-relevant than ordinary limitations because
   they can create false confidence.
6. Continuation safety may depend on awareness of participant limitations.
7. A participant may be aligned but constrained.
8. A participant may be compliant but incapable of performing a required task.
9. Consumer state should remain distinct from repository state.
10. Consumer limitations should not modify repository truth.
11. Constraint metadata should behave like yellow-tag operational caution unless
    a task-specific condition makes operation unsafe.
12. Preservation should be material and minimal, not exhaustive self-description.
13. A workaround may be necessary for safe continuation, but it is not
    architecture.
14. A defective or unavailable capability should qualify evidence rather than
    create negative proof.
15. Continuation constraints should guide safe operation without becoming
    authority, ontology, projection truth, or runtime semantics.

## Final Reconciliation

Continuation should preserve awareness of participant capabilities,
constraints, limitations, and known defects when those conditions materially
affect safe continuation.

That preservation is not an authority change. It is not architecture. It is not
repository knowledge. It is not a historical summary. It is yellow-tag style
operational caution metadata: a way to prevent future consumers from continuing
under false assumptions about what a participant could do or safely trust.

The clean boundary is:

```text
What was I doing?        -> activity context
What is true?            -> authority / repository / architecture
What can I do?           -> consumer capability
What limits safe action? -> continuation constraint
What is broken?          -> known defect
What must be preserved?  -> only material safety-relevant constraint awareness
```

Maintaining these distinctions allows continuation to be safer without allowing
consumer limitations to rewrite architectural truth.
