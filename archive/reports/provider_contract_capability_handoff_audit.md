# Provider Contract / Capability Handoff Audit

## Scope

This is a bounded architectural audit. It does not implement a provider registry,
provider negotiation, provider optimization, adaptive prompting, contract scoring,
learning system, runtime provider abstraction, framework, schema change, or CLI
change.

The question is whether current repository evidence already supports separating:

```text
Answer
-> Capability Handoff Artifact
-> Provider Contract
-> Presentation
```

from treating provider-specific prompts or packets as the architectural object.
Repository authority wins. The currently observed provider outputs are treated as
observed implementations, not normative specifications.

## Executive answer

Yes. The repository already supports the distinction:

```text
Capability Handoff Artifact != Provider Contract
```

but only as an implementation-backed architectural characterization, not as a
runtime contract system.

The shared handoff material belongs to an already-supported artifact-kind layer:
bounded inquiry, implementation evidence, repository authority, boundaries,
limitations, expected deliverable, and non-execution/non-truth-promotion
constraints. Provider contracts are downstream observed variants that organize
that material for a particular consumer such as a fresh ChatGPT session, an
active ChatGPT continuation, or Codex implementation work.

The repository evidence also supports characterizing the three currently
observed provider-facing outputs as **Observed Provider Contract Variants** rather
than fixed architectural definitions. Their wording, ordering, verbosity,
context strategy, acceptance phrasing, and continuity strategy optimize for a
consumer. Those differences do not change repository meaning unless they add a
new mutation, execution, authority, or truth boundary.

## Implementation evidence reviewed

Primary evidence:

- `artifact_kind_answer_composition_audit.md` already characterizes capability
  handoffs as artifact kinds produced after bounded answer composition.
- `answer_composition_family_completion_audit.md` documents the implementation
  path from implementation-local answer payloads to compatibility objects and
  rendering.
- `compatibility_handoff_classification_audit.md` classifies Compatibility
  Handoff as a recurring architectural pattern that transports owner decisions
  without owning independent repository truth.
- `seed_runtime/handoff_plans.py` implements non-executable provider handoff
  planning outside the Core MVP runtime path.
- `tests/test_handoff_plans.py` proves handoff plans are non-executable, reject
  secret or authority claims, and do not create approvals, execution
  authorizations, pending actions, or tool calls.
- `seed_runtime/inquiry_orientation.py` shows answer material, limitations, and
  authority boundary being composed before rendering for a human-facing
  orientation surface.
- `seed_runtime/operational_story.py` shows answer, reasoning, supporting
  evidence, boundary, and limitations separated before a public view and text
  formatter.
- `docs/seed.md` preserves repository-level boundaries around observation,
  claims, projection, questions, capabilities, execution, and authority.
- `docs/reasoning_roadmap.md` states the canonical runtime path and explicitly
  keeps provider/handoff recommendations downstream of knowledge and capability
  resolution without adding execution behavior.

## Shared capability handoff semantics

The shared capability handoff artifact is not a prompt, packet, or provider
format. It is the provider-independent material needed to carry an already
bounded answer across a consumer boundary without changing repository truth.

Shared semantics supported by current evidence:

| Shared semantic | What it means | Evidence basis |
| --- | --- | --- |
| Bounded inquiry | The handoff begins from a question already scoped by repository evidence, not from provider preference. | Answer-composition audits and implemented `build_operational_story(...)` / `build_inquiry_orientation(...)` paths. |
| Repository authority | Claims are constrained by repository evidence and explicit boundaries. | `docs/seed.md` and authority boundaries in inquiry orientation and operational story. |
| Implementation evidence | The artifact carries file/code/test/diagnostic evidence or references to the already-composed answer support. | Answer-composition and artifact-kind audits. |
| Boundary preservation | The handoff communicates what is outside scope: no execution, mutation, provider trust, approval, credential availability, or truth promotion unless separately implemented. | `HandoffPlanService` and handoff-plan tests. |
| Limitations / unsupported conclusions | The artifact includes uncertainty, unknowns, or unsupported conclusions rather than silently converting absence into truth. | Operational story limitations and inquiry orientation uncertainty. |
| Expected deliverable | The consumer is told what output is expected: audit, continuation, implementation work packet, report, or patch. | Existing repository audit/report pattern and prompt-like provider outputs observed in practice. |
| Non-normativity of presentation vocabulary | Wording used to orient a human or provider does not itself become knowledge. | Inquiry orientation boundary and repository AGENTS guidance. |

These semantics belong to the **Capability Handoff Artifact** because they are
provider-independent and derive from answer composition plus artifact
composition.

## Observed provider contract variants

### 1. ChatGPT Fresh Session

| Field | Characterization |
| --- | --- |
| Underlying inquiry | A bounded inquiry or implementation-backed answer must be restarted in a new conversation with reduced prior context. |
| Shared handoff semantics | Repository authority, implementation evidence, boundaries, limitations, and expected deliverable must be preserved. |
| Consumer | A ChatGPT session with no active conversational memory of the work. |
| Provider-specific organization | Usually front-loads context, repository authority, scope, central question, forbidden moves, investigation targets, and deliverable so the new session can reconstruct the work position. |
| Provider-specific wording | Emphasizes fresh-session orientation, explicit context reconstruction, and reminders that repository authority wins. |
| Presentation | Prompt-like prose. Its organization is a consumer strategy, not repository truth. |
| Implementation evidence | Supported indirectly by artifact-kind and answer-composition evidence: a consumer-specific artifact can be produced after bounded answer composition without becoming an architectural owner. |

### 2. ChatGPT Continuation

| Field | Characterization |
| --- | --- |
| Underlying inquiry | Continue a bounded answer or audit in a session that already has some active context. |
| Shared handoff semantics | Same invariant handoff material: repository authority, evidence, boundaries, limitations, deliverable. |
| Consumer | A ChatGPT conversation that can rely on active-session continuity. |
| Provider-specific organization | Can use shorter context, more references to current work position, and fewer reconstruction details than a fresh-session prompt. |
| Provider-specific wording | Emphasizes continuation, current active edge, what remains unresolved, and how not to drift from repository evidence. |
| Presentation | Prompt-like continuation prose. It optimizes context strategy and continuity, not meaning. |
| Implementation evidence | The repository already warns that terms such as continuation and current work position may be presentation labels unless implementation evidence promotes them; therefore this contract should remain an observed provider variant. |

### 3. Codex Implementation

| Field | Characterization |
| --- | --- |
| Underlying inquiry | Convert a bounded answer or audit conclusion into repository work: inspect evidence, make the smallest implementation-backed change, test it, commit it, and report it. |
| Shared handoff semantics | Repository authority, implementation evidence, boundaries, limitations, and expected deliverable still apply. |
| Consumer | Codex-like implementation agent operating in the repository. |
| Provider-specific organization | Adds operational instructions: inspect files, obey `AGENTS.md`, edit repo artifacts, run tests, commit changes, and produce PR/report metadata when required. |
| Provider-specific wording | More imperative than ChatGPT variants because the consumer can modify the repository and run commands. |
| Presentation | Work packet / task packet prose plus acceptance criteria. The packet is a provider contract around the same handoff material. |
| Implementation evidence | Repository instructions and current task flow demonstrate that implementation work packets may include repo mutation and tests, while runtime handoff artifacts such as `HandoffPlan` remain non-executable unless the task explicitly asks for repository edits. |

## Invariant versus provider-specific fields

### Invariant fields across provider contracts

These belong to the shared **Capability Handoff Artifact**:

1. **Underlying bounded inquiry**: what question or answer is being carried.
2. **Repository authority**: repository evidence wins over preference,
   provider style, or conversation history.
3. **Implementation evidence requirements**: conclusions must cite or derive
   from files, code, tests, diagnostics, or existing repository documents.
4. **Artifact boundary**: the handoff does not itself create truth, execution,
   approval, credential availability, provider trust, mutation, or architecture
   authority.
5. **Limitations and unsupported conclusions**: what cannot be claimed from the
   evidence.
6. **Expected deliverable**: the output class requested from the consumer.
7. **Acceptance constraints**: the conditions under which the handoff succeeds.

### Provider-specific fields

These belong only to the **Provider Contract**:

1. **Ordering**: where context, authority, forbidden moves, acceptance, and
   deliverable appear.
2. **Verbosity**: how much context is restated for the consumer.
3. **Context strategy**: fresh reconstruction versus active continuation versus
   repository-local implementation.
4. **Instruction phrasing**: reminders, imperatives, bullets, or narrative.
5. **Acceptance wording**: provider-appropriate success criteria.
6. **Provider expectations**: whether the consumer can edit files, run tests,
   commit, or only produce analysis.
7. **Conversation continuity strategy**: how much previous work is assumed to be
   live.
8. **Presentation format**: Markdown prompt, work packet, audit report, final
   response, or PR body.

These differences are real provider-contract concerns. They do not change
repository meaning unless they cross into mutation, execution, policy,
projection, event recording, or knowledge promotion.

## Artifact boundaries

The repository already supports a boundary stack:

```text
Implementation Evidence
-> Question
-> Answer Composition
-> Capability Handoff Artifact
-> Provider Contract
-> Presentation
```

The evidence does not support making provider-specific prompt text the
architectural object. Provider-specific prompt text is a presentation and
consumer-contract variant over shared handoff semantics.

This boundary aligns with existing repository patterns:

- Answer composition owns bounded answer, reason, support, boundary, and
  limitations.
- Artifact composition owns consumer-specific organization.
- Compatibility handoff transports owner decisions without owning independent
  repository truth.
- Presentation renders labels and prose without promoting those labels to
  knowledge.
- Runtime mutation, event recording, execution, projection, and state evolution
  remain outside artifact composition.

## Counterexamples and provider-contract-only behavior

The following differences genuinely belong to the provider contract rather than
the shared handoff artifact:

1. **Fresh-session context reconstruction.** A fresh ChatGPT contract should
   repeat more context. That is a consumer context strategy, not a new repository
   meaning.
2. **Active-session compression.** A continuation contract can assume more live
   context and focus on unresolved edges. That optimizes continuity but does not
   alter evidence or boundaries.
3. **Codex commandability.** A Codex work packet can instruct repository edits,
   tests, commits, and PR creation. That is a provider capability expectation.
   It must still obey repository instructions and does not imply Seed runtime
   handoff artifacts are executable.
4. **Acceptance wording.** Different providers may need different success
   phrasing. Acceptance wording is contract presentation unless it changes what
   evidence, mutation, or deliverable is required.
5. **Instruction phrasing and ordering.** Provider prompts may front-load
   warnings, put deliverables last, or use stronger imperatives. These are
   optimization choices over the same handoff artifact.

No reviewed counterexample requires changing repository truth. The strongest
warning is Codex implementation: the provider contract may authorize repository
file changes in the development environment, while Seed runtime capability
handoffs remain non-executable and non-authorizing. That difference belongs to
execution environment and task contract, not to a runtime provider abstraction.

## Supported conclusions

1. The repository already supports `Capability Handoff Artifact != Provider
   Contract` as an architectural characterization.
2. The current provider-specific outputs are best treated as **Observed Provider
   Contract Variants**, not normative architectural definitions.
3. Shared semantics belong to the handoff artifact: bounded inquiry, repository
   authority, implementation evidence, boundaries, limitations, deliverable, and
   non-truth-promotion constraints.
4. Provider-specific organization belongs to the provider contract: ordering,
   verbosity, context strategy, instruction phrasing, acceptance wording,
   provider expectations, and conversation continuity strategy.
5. Provider contracts can evolve independently while consuming the same
   underlying handoff artifact, as long as they preserve repository authority and
   do not change implemented truth, mutation, execution, projection, or event
   boundaries.
6. This creates an implementation-backed foundation for future provider-specific
   improvement through observation rather than intuition.

## Unsupported conclusions

1. Unsupported: the repository has a runtime provider contract system.
2. Unsupported: the repository has provider selection, negotiation, scoring,
   optimization, adaptive prompting, or learning behavior.
3. Unsupported: ChatGPT Fresh Session, ChatGPT Continuation, or Codex
   Implementation is an optimal or normative provider contract.
4. Unsupported: provider-specific wording is repository knowledge.
5. Unsupported: compatibility handoff is a first-class responsibility family.
6. Unsupported: runtime `HandoffPlan` objects are executable or authorize
   provider work.
7. Unsupported: future providers should be normalized into a registry or schema
   now.

## Explicit answers

### Does the repository already support `Capability Handoff Artifact != Provider Contract`?

Yes. Existing evidence supports the distinction as an architectural
characterization. The shared handoff artifact carries bounded answer material and
boundaries. The provider contract organizes that material for a specific
consumer.

### Are ChatGPT Fresh Session, ChatGPT Continuation, and Codex Implementation observed provider contract variants rather than normative definitions?

Yes. They are best characterized as observed provider contract variants. Their
differences are consumer-specific organization and presentation strategies over
shared handoff semantics, not fixed architecture.

### Which semantics belong to the shared handoff artifact?

Bounded inquiry, repository authority, implementation evidence, boundary
preservation, limitations, unsupported conclusions, expected deliverable,
acceptance constraints, and non-promotion of presentation vocabulary.

### Which semantics belong only to the provider contract?

Ordering, verbosity, context strategy, instruction phrasing, acceptance wording,
provider expectations, conversation continuity strategy, and presentation format.

### Does this create an implementation-backed foundation for future provider-specific improvement without changing repository truth?

Yes. Provider contracts can be improved by observing which organization and
wording better serve each consumer, while preserving the same underlying handoff
artifact and repository authority. That supports future improvement without a
runtime provider registry, negotiation system, optimization layer, schema change,
or truth change.

## Recommended next implementation step

Do not implement a provider registry, provider abstraction, or prompt framework.

The smallest next implementation-backed step, if future work needs it, is to
update one existing provider-facing handoff artifact generator or template by
separating implementation-local **handoff semantics** from **provider wording**
while preserving public behavior. That step should be done only when there is a
concrete existing generator or template under test. It should not introduce
selection, negotiation, scoring, adaptive prompting, schema changes, or CLI
changes.
