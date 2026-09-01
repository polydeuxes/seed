# Purpose

Seed prompts are intentionally structured because Seed is a small, ownership-driven
knowledge runtime. Codex works best on Seed when a prompt first teaches the shape
of the system instead of immediately asking for implementation.

A good Seed prompt explains:

- what Seed is: a knowledge, evidence, fact, relationship, explanation, and
  capability-discovery runtime;
- what Seed is not: not a workflow engine, scheduler, orchestration system,
  automatic execution system, or prompt-generation engine;
- why the requested task matters;
- what architecture already exists;
- which component owns the behavior in question;
- what must not change while solving the task.

This protocol exists to prevent architecture drift. It is documentation only. It
must not be read as a request to add prompt generation, runtime behavior,
`ToolExecutor` behavior, LLM orchestration, automatic prompt construction, or a
new execution path.

# Protocol Structure

Use this canonical flow for Seed work requests:

1. Context
2. Current Accepted Architecture
3. Recent History
4. Problem Statement
5. Goal
6. Non-Goals
7. Ownership Boundaries
8. Tasks
9. Tests
10. Hard Constraints
11. Final Response Requirements

Each section should make Codex more architecture-aware before it starts changing
files.

## 1. Context

### Purpose

Establish what Seed is, where the task fits, and why the request exists.

### Expected content

- A short description of the relevant Seed subsystem.
- The reasoning or product motivation for the work.
- Any relevant user-visible or developer-visible problem.
- The expected level of change, such as documentation-only, tests-only,
  read-only helper, or implementation.

### Common mistakes

- Starting with file edits before explaining why the task matters.
- Assuming Codex remembers prior Seed decisions without restating them.
- Describing Seed as a general automation platform instead of a bounded knowledge
  and capability-discovery runtime.

## 2. Current Accepted Architecture

### Purpose

Anchor the task in the architecture Seed currently accepts.

### Expected content

- The canonical runtime boundary.
- The owner services involved in the task.
- Existing data flows and names that must be preserved.
- Any accepted docs, audits, or tests that define current behavior.

### Common mistakes

- Reintroducing RuntimeLoop-era assumptions.
- Treating historical audits as current architecture when they are quarantined or
  superseded.
- Omitting the existing component that already owns the behavior.

## 3. Recent History

### Purpose

Explain why the task is being requested now and what recent work or audit finding
it follows.

### Expected content

- Recently completed audits, reconciliations, or cleanups.
- Decisions that narrowed the acceptable solution space.
- Prior failures or drift patterns the prompt should avoid.

### Common mistakes

- Treating old plans as still open when reconciliation docs have already narrowed
  them.
- Repeating a previous rejected implementation path.
- Skipping the reason a conservative solution is preferred.

## 4. Problem Statement

### Purpose

State the specific problem without prescribing the wrong implementation.

### Expected content

- The observed gap, ambiguity, or missing artifact.
- The risk of leaving it unresolved.
- The distinction between the problem and any tempting non-solution.

### Common mistakes

- Turning the problem statement into an implementation checklist too early.
- Framing a documentation or vocabulary problem as an execution problem.
- Describing a capability gap as permission to execute tools automatically.

## 5. Goal

### Purpose

Define successful completion in positive terms.

### Expected content

- The artifact or behavior that should exist after the work.
- The expected scope of the change.
- Concrete success criteria.

### Common mistakes

- Using vague goals such as "make it better" or "add support".
- Mixing goals with non-goals.
- Defining success as broad architecture expansion when the task only needs a
  narrow documentation, test, or read-only change.

## 6. Non-Goals

### Purpose

Prevent Codex from filling gaps with extra architecture.

### Expected content

- Behaviors that must not be added.
- Subsystems that must not be changed.
- Explicit exclusions such as no runtime behavior, no execution behavior, no
  scheduler, no workflow engine, no LLM orchestration, or no prompt generation.

### Common mistakes

- Omitting non-goals because they feel obvious.
- Listing only what to build and not what to avoid.
- Forgetting that Seed prompts often need to forbid attractive but wrong
  architecture.

## 7. Ownership Boundaries

### Purpose

Tell Codex where behavior belongs and where it does not belong.

### Expected content

- The component that owns each relevant behavior.
- The boundary between recommendation, request, resolution, and execution.
- The boundary between append-only events and cached projections.
- Any component that must remain read-only for this task.

### Common mistakes

- Creating duplicate owners for execution, projection, or capability reasoning.
- Letting a catalog become executable.
- Letting `request_tool` become an execution path.
- Moving event ownership into projection caches.

## 8. Tasks

### Purpose

List the concrete work only after context, architecture, history, goals,
non-goals, and ownership have been established.

### Expected content

- Ordered, specific tasks.
- Exact files to create or update when known.
- Review expectations, such as checking recent audits for alignment.
- Documentation, tests, and code changes separated when possible.

### Common mistakes

- Leading with tasks before architecture understanding.
- Combining unrelated implementation and documentation work.
- Hiding architecture decisions inside task wording.

## 9. Tests

### Purpose

Define how correctness should be checked.

### Expected content

- Required test commands.
- Whether tests should be added.
- Whether documentation-only work requires no new tests.
- Any accepted environment limitation.

### Common mistakes

- Omitting tests for implementation work.
- Adding runtime tests for documentation-only tasks that do not need behavior.
- Treating tests as a substitute for architecture constraints.

## 10. Hard Constraints

### Purpose

Make absolute boundaries explicit.

### Expected content

- Architecture constraints that must not be violated.
- Forbidden files, subsystems, or behaviors.
- Required compatibility with accepted docs and invariants.

### Common mistakes

- Stating preferences as constraints without clarity.
- Forgetting to forbid the exact drift that has happened before.
- Leaving room for new execution, scheduling, orchestration, or runtime loops.

## 11. Final Response Requirements

### Purpose

Ensure Codex confirms what changed and what did not change.

### Expected content

- Files created and files modified.
- Tests added, if any.
- Tests run.
- Confirmations for documentation-only or behavior-free work.
- Explicit confirmations that forbidden systems were not changed.

### Common mistakes

- Asking only for a summary and tests when architecture confirmations matter.
- Omitting negative confirmations such as "no Runtime changes".
- Forgetting to ask for file-level evidence.

# Why Narrative First Works

Seed prompts should establish why before how.

```text
Context
-> understanding

Ownership
-> correct placement

Constraints
-> avoids architecture drift

Tasks
-> implementation
```

Narrative-first prompts work because they give Codex the information needed to
choose the smallest architecture-aligned change. Context creates understanding.
Ownership points work to the component that already owns the behavior. Constraints
block duplicate runtimes, hidden execution paths, workflow systems, schedulers,
and orchestration. Tasks then become bounded implementation or documentation
steps instead of invitations to invent new architecture.

The recommended order is deliberate: explain why the work matters before asking
how to do it.

# Architecture Awareness

Seed prompts should restate the current accepted architecture whenever a task is
near runtime, execution, capability resolution, projection, temporal reasoning,
contradiction handling, or provider recommendations.

Required reminders:

- `Runtime` is canonical.
- `ToolExecutor` owns execution.
- `EventLedger` owns append-only events.
- `ProjectionStore` owns projection caching.
- `CapabilityCatalog` recommends.
- `ToolRegistry` exposes operations.
- `ToolExecutor` executes operations.
- `ToolNeed` is a capability gap.
- `request_tool` never executes.
- `call_tool` is the execution boundary.

Architecture-aware prompts should also preserve the current Core MVP shape:
knowledge, evidence, facts, relationships, explanations, `ToolNeed`, read-only
capability resolution, registered operation candidates, and provider/handoff
recommendations. They should not restate RuntimeLoop-era assumptions as current
architecture.

# Anti-Patterns

Avoid these prompt patterns:

- Starting with implementation instructions.
- Skipping ownership.
- Skipping non-goals.
- Creating new runtimes.
- Creating workflow engines.
- Creating schedulers.
- Creating orchestration systems.
- Adding execution behavior when solving knowledge problems.
- Treating provider or handoff recommendations as verified capability status.
- Treating a registered operation candidate as permission to execute.
- Asking `CapabilityCatalog` to execute or verify anything.
- Asking `request_tool` to call `ToolExecutor`.
- Making `ProjectionStore` own events or historical truth.

# Prompt Quality Checklist

Before sending a Seed prompt, check:

- [ ] Does the prompt explain why the work matters?
- [ ] Does it describe what Seed is and what Seed is not?
- [ ] Does it identify the current accepted architecture?
- [ ] Does it name the owner of each behavior involved?
- [ ] Does it define non-goals?
- [ ] Does it define success criteria?
- [ ] Does it separate documentation, tests, and implementation tasks?
- [ ] Does it require tests or explicitly explain why no new tests are needed?
- [ ] Does it forbid architecture drift relevant to the task?
- [ ] Does it avoid RuntimeLoop-era assumptions?
- [ ] Does it require final confirmations for what changed and what did not
  change?

# Canonical Prompt Template

Copy and paste this template for Seed work requests:

```text
You are working in Seed.

Context

[Explain the relevant Seed subsystem, why this task matters, and whether the
change is documentation-only, tests-only, read-only, or implementation.]

Current Accepted Architecture

[State the architecture that must be preserved. Include relevant reminders such
as: Runtime is canonical; ToolExecutor owns execution; EventLedger owns
append-only events; ProjectionStore owns projection caching; CapabilityCatalog
recommends; ToolRegistry exposes operations; ToolExecutor executes operations;
ToolNeed is a capability gap; request_tool never executes; call_tool is the
execution boundary.]

Recent History

[Summarize recent audits, reconciliations, cleanups, or failures that explain why
this task is shaped this way. Note any superseded RuntimeLoop-era assumptions.]

Problem Statement

[State the precise gap or ambiguity. Explain the risk of leaving it unresolved.]

Goal

[Define the desired outcome and concrete success criteria.]

Non-Goals

[Explicitly list what must not be added or changed. Include no runtime behavior,
no ToolExecutor behavior, no scheduler, no workflow engine, no orchestration, no
prompt generation, or other exclusions as appropriate.]

Ownership Boundaries

[Name the owner of each relevant behavior. Explain where behavior does not
belong. Distinguish recommendation, request, resolution, and execution.]

Tasks

1. [Specific task.]
2. [Specific task.]
3. [Specific task.]

Tests

[State required tests or say that no new tests are required for documentation-only
work unless repository docs conventions require them. Include commands to run.]

Hard Constraints

- [Constraint.]
- [Constraint.]
- [Constraint.]

Final Response Requirements

The final response must include:

- files created;
- files modified;
- tests added, if any;
- tests run;
- confirmation that the work stayed within scope;
- confirmation that forbidden systems or behaviors were not changed.
```
