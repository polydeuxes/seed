# 01 Architecture

## System summary

Seed is a context-native planning and handoff runtime. It composes context, records evidence-backed state, ranks capabilities, and produces auditable recommendations and non-executable plans. Seed does **not** own an internal execution lifecycle.

Seed has two large halves:

1. **Runtime** — handles events, builds context, lets models decide, records state, manages Tool Needs, ranks recommendations, and emits non-executable Action Plans and HandoffPlans.
2. **Builder** — turns explicit Tool Needs into generated toolkit candidates, validates metadata/contracts, and prepares capabilities for registration.

The runtime is always conservative. The builder can be creative, but its outputs are untrusted until validated and registered. Actual execution is delegated to external providers.

## High-level flow

```text
External input
  -> Ingestor
  -> Event Ledger
  -> State Projector
  -> Context Composer
  -> Model Orchestrator
  -> Decision Validator
       -> Answer
       -> Clarifying Question
       -> Tool Need Request
       -> State Patch Proposal
       -> Non-executable Action Plan
       -> HandoffPlan
  -> Policy Gate / CapabilityCatalog / Builder / Handoff Composer
  -> Event Ledger
  -> Response Composer
  -> External Provider (outside Seed, if user/operator proceeds)
```


## Ownership boundary

Seed owns:

- Context composition
- Event ledger
- State projection
- Fact/evidence model
- ToolNeeds
- CapabilityCatalog
- RecommendationRanker
- ActionPlans as non-executable plans
- HandoffPlans as non-executable provider handoffs
- Policy metadata
- Audit trail

Seed delegates:

- actual execution
- secrets
- retries
- scheduling
- long-running jobs
- credential prompts

Preferred execution backends live outside Seed:

- Ansible/AWX for host automation
- Temporal/Prefect for workflows
- MCP servers for tool integration
- Vault, ssh-agent, sudo, and become-aware automation for secrets and privilege boundaries

Seed may record a HandoffPlan and later ingest external provider observations as Evidence, but it must not become the executor of record.

## Main components

### 1. Ingestor

Accepts input from users, APIs, schedules, monitors, or webhooks.

Responsibilities:

- assign event IDs
- normalize source metadata
- preserve original text/payload
- attach session or workspace identity
- never discard raw input

Non-responsibilities:

- deciding whether actions are allowed
- executing tools
- generating tools

### 2. Event Ledger

Append-only durable record of what happened.

Stores:

- user messages
- system observations
- model decisions
- handoff plans
- external observations/results when reported back
- policy blocks
- approvals
- generated toolkit artifacts
- validation results
- state transitions

The ledger is the source of auditability. State can be rebuilt from it.

### 3. State Projector

Builds current state from ledger events.

Maintains projections such as:

- active sessions
- active goals
- known entities
- known capabilities
- open ToolNeeds
- CapabilityCatalog entries
- unresolved approvals
- recent evidence
- stale facts
- FactSupport aggregates and fact conflicts

State should be deterministic and inspectable.


#### Fact Support Aggregation

Verification is not a separate subsystem in Seed's core architecture. A provider check, user correction, discovery result, imported record, or deterministic inference enters the system as Evidence and Facts. The projector then groups Facts by `subject + predicate + value` into FactSupport objects.

Seed preserves provenance instead of stamping a claim with `verified: true`. The current belief for a `subject + predicate` is derived from:

- supporting Facts for each value
- conflicting Facts for other values
- aggregate confidence
- source type strength (`discovery`/`provider`/observed sources generally outrank inferred-only support)
- recency via latest observation time

This keeps disagreement auditable: multiple values can remain in state while `get_best_fact(subject, predicate)` returns the representative Fact for the best-supported current belief.

### 4. Context Composer

Builds a compact model-facing packet from state.

This is the heart of the product.

It decides what the model sees:

- current user input
- relevant history
- active goals
- known facts
- missing facts
- available capabilities
- blocked or policy-limited capabilities
- open ToolNeeds
- candidate HandoffPlans
- policy summaries
- expected decision schema

The composer should not dump the database into the prompt. It should present a task-relevant view.

### 5. Model Orchestrator

Calls one or more models to produce a decision.

The model may output:

- answer user
- ask a question
- request a ToolNeed
- propose a non-executable Action Plan
- propose a HandoffPlan
- propose state update
- refuse/block

The model should not directly execute tools or mutate durable state. Its output is a proposal until validated.

### 6. Decision Validator

Checks the model output against schemas and state.

Validates:

- decision type is allowed
- referenced capability or backend exists in the CapabilityCatalog
- HandoffPlan fields match schema
- referenced entities exist or can be created
- confidence/ambiguity rules
- approval requirement
- policy class

Invalid decisions become model-correction events or user-facing clarification.

### 7. CapabilityCatalog

Catalog of capabilities and external provider handoff targets.

A catalog entry includes:

- capability name
- natural-language summary
- supported backend types
- provider/backend references
- operation names
- input/target metadata
- policy action
- toolkit ID or catalog source
- lifecycle status
- visibility rules
- examples

The catalog may load capabilities from hand-written metadata, generated toolkit metadata, MCP server descriptions, and external automation inventory. It describes what Seed can recommend or hand off; it does not imply that Seed can execute the operation itself.

### 8. Policy Gate

Determines whether a proposed action can proceed.

Policy sees:

- action name
- risk class
- subject/user/session
- scope/entity
- current state
- approval status
- environment

Policy returns:

- allow
- block
- require confirmation
- require human approval
- require different credential/provider
- produce handoff-only recommendation

Policy is deterministic and auditable.

### 9. Handoff Composer

Builds non-executable HandoffPlans for external providers.

Handoff Composer responsibilities:

- select an appropriate provider/backend from the CapabilityCatalog
- summarize policy constraints
- state the target and operation
- describe the secret boundary
- record whether external/provider approval is still required
- mark the plan `executable: false`
- avoid implying user approval, execution authorization, credential availability, provider trust, or tool registration
- emit auditable handoff events

The Handoff Composer does not run tools, ask for credentials, retry operations, schedule jobs, monitor long-running work, or manage execution state. Those responsibilities belong to external providers such as Ansible/AWX, Temporal/Prefect, MCP servers, Vault, ssh-agent, sudo, or become-aware automation.

### 10. Tool Need Store

Tracks desired missing capabilities.

A Tool Need is a durable object saying: “The system needs a tool/capability that does not currently exist.”

Example:

```json
{
  "id": "need_123",
  "name": "install_ssh_server",
  "capability": "ssh_access",
  "reason": "User wants host node-1 to accept SSH logins.",
  "risk_hint": "mutating",
  "status": "proposed"
}
```

### 11. Builder Queue

Moves approved Tool Needs to the builder service.

The queue decouples runtime from generation. Production runtime can say “tool needed” without immediately creating executable code.

### 12. Builder Service

Generates toolkit candidates from Tool Needs.

Produces:

- manifest
- schemas
- implementation
- tests
- docs
- policy proposals
- validation report

The builder can use stronger models or deterministic templates. It is not the same as the runtime model.

### 13. Toolkit Validator

Validates generated toolkit candidates.

Checks:

- manifest schema
- operation schema
- policy metadata
- import safety
- static code rules
- test suite
- sandbox validation
- forbidden APIs
- dependency declarations
- documentation completeness

Only validated toolkits can be registered.

## Runtime versus builder boundary

```text
Runtime:
  - receives user input
  - builds context
  - records events and projected state
  - maintains facts, evidence, ToolNeeds, CapabilityCatalog, recommendations, policy metadata, and audit trail
  - proposes non-executable Action Plans and HandoffPlans
  - delegates actual execution to external providers

Builder:
  - generates candidate toolkits
  - validates candidate toolkits
  - proposes registration
  - never silently grants production execution rights
```

## Trust levels

```text
Level 0: User/model desire
Level 1: Tool Need recorded
Level 2: Toolkit candidate generated
Level 3: Toolkit candidate validated in sandbox
Level 4: Capability registered but policy-gated
Level 5: HandoffPlan emitted with `executable: false`
Level 6: External provider reports result back as Evidence
```

Each level is explicit. No implicit promotion.

## Architectural anti-patterns

Avoid:

- model writes code and immediately runs it
- route handlers import provider internals
- registry imports executable provider modules during metadata listing
- generated tool bypasses manifest/validation
- policy lives inside prompt text only
- context window becomes the database
- every user phrase becomes a hardcoded branch
- Seed runs tools, manages retries/schedules, or handles credentials instead of delegating to external providers

## Minimal viable architecture

The first build does not need everything. Minimum useful system:

1. Event ledger.
2. State projector.
3. Context composer.
4. Decision schema.
5. Static CapabilityCatalog.
6. Policy gate.
7. Tool Need object.
8. Builder stub that emits toolkit templates.

Even if tools are not fully generated on day one, Tool Needs should be first-class from the beginning.
