# Seed System Blueprint

This directory is a portable architecture packet for a new repository. It is written to be copied out of this codebase without depending on legacy module names.

## Working name

**Seed**: a context-native runtime that grows operational tools from recorded capability gaps.

The name is intentionally different from the old repo. The core idea is not a gateway, not an automation wrapper, and not a permission engine. It is a system that accumulates context, understands missing capabilities, and safely grows a typed tool vocabulary.

## One-sentence product definition

Seed receives unique user or system inputs, turns them into durable state, presents a compact context packet to an LLM, lets the LLM answer, ask, call registered tools, or request missing tools, and records every result back into state.

## Core thesis

Permissions and flow control are necessary infrastructure, but they are not the architecture. The architecture is the **context engine** plus a **tool-growing loop**:

```text
input
  -> event record
  -> state update
  -> context packet
  -> model decision
  -> tool call or tool need
  -> validation/policy/execution/build
  -> state update
  -> response
```

## What is new

Most automation systems begin with a catalog of hand-written tools and then bolt on an LLM. Seed starts from the opposite direction:

1. Start with a small, constrained model.
2. Give it durable state and compact context.
3. Let it discover missing capabilities.
4. Convert missing capabilities into explicit **Tool Needs**.
5. Use a separate builder to generate toolkits.
6. Validate and register toolkits.
7. Expose registered tools back to the model.

The model does not get unrestricted power to rewrite its runtime. It can request and help specify tools. A separate builder and validation pipeline produce tools. A registry and policy gate decide what becomes available.

## Design principles

1. **State before cleverness**  
   The model should reason over explicit state, not hidden conversational vibes.

2. **Small-model pressure is good**  
   Design so a small model can succeed: short context, explicit choices, typed actions, deterministic validation.

3. **Tools are generated products, not prompt tricks**  
   A tool is a manifest, schemas, policy metadata, implementation, tests, documentation, and lifecycle state.

4. **Desire is not permission**  
   A model or user can desire an action. Policy decides whether it can happen.

5. **Generated does not mean trusted**  
   Generated toolkits must be sandboxed, tested, classified, reviewed when needed, and registered before use.

6. **The runtime does not build itself while running production actions**  
   Tool building is separate from tool execution.

7. **Every action returns to state**  
   Answers, questions, tool calls, tool results, failed attempts, approvals, and generated artifacts all become durable events.

## Document map

Read in this order:

1. [`01-architecture.md`](01-architecture.md) — system overview and component boundaries.
2. [`02-domain-model.md`](02-domain-model.md) — names and core objects.
3. [`03-runtime-loop.md`](03-runtime-loop.md) — event-to-context-to-decision execution loop.
4. [`04-toolkit-system.md`](04-toolkit-system.md) — generated toolkit format and lifecycle.
5. [`05-policy-and-safety.md`](05-policy-and-safety.md) — trust boundaries, risk classes, approval model.
6. [`06-context-engine.md`](06-context-engine.md) — how to build model context packets.
7. [`07-builder-service.md`](07-builder-service.md) — separate tool builder design.
8. [`08-small-model-strategy.md`](08-small-model-strategy.md) — designing for small local models and model tiers.
9. [`09-pseudocode.md`](09-pseudocode.md) — implementation sketches.
10. [`10-build-plan.md`](10-build-plan.md) — multi-day Codex session plan.
11. [`11-naming.md`](11-naming.md) — better names and terms to avoid.
12. [`12-open-questions.md`](12-open-questions.md) — decisions to make while building.

## Suggested repo shape

```text
seed/
  README.md
  docs/
    architecture.md
    toolkits.md
    context-engine.md
  seed_runtime/
    api/
    context/
    decisions/
    events/
    execution/
    ledger/
    policy/
    registry/
    state/
  seed_builder/
    generator/
    validators/
    templates/
    sandbox/
  toolkits/
    core/
    generated/
  tests/
```

## Mental model

Seed should feel less like this:

```text
User -> API route -> hardcoded workflow -> provider call
```

And more like this:

```text
User -> event -> state -> context -> model decision -> validated action -> state
```

The API is not the center. The context loop is the center.
