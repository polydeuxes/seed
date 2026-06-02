# 01 Architecture

## System summary

Seed is a context-native tool-growing runtime. It has two large halves:

1. **Runtime** — handles events, builds context, lets models decide, invokes registered tools, and records outcomes.
2. **Builder** — turns explicit tool needs into generated toolkit candidates, validates them, and prepares them for registration.

The runtime is always conservative. The builder can be creative, but its outputs are untrusted until validated and registered.

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
       -> Registered Tool Call
       -> Tool Need Request
       -> State Patch Proposal
  -> Policy Gate / Registry / Builder / Executor
  -> Event Ledger
  -> Response Composer
```

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
- tool calls
- tool results
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
- open tool needs
- registered tools
- tool validation status
- unresolved approvals
- recent evidence
- stale facts

State should be deterministic and inspectable.

### 4. Context Composer

Builds a compact model-facing packet from state.

This is the heart of the product.

It decides what the model sees:

- current user input
- relevant history
- active goals
- known facts
- missing facts
- available tools
- blocked tools
- open tool needs
- policy summaries
- expected decision schema

The composer should not dump the database into the prompt. It should present a task-relevant view.

### 5. Model Orchestrator

Calls one or more models to produce a decision.

The model may output:

- answer user
- ask a question
- call registered tool
- request new tool
- propose state update
- refuse/block

The model should not directly execute tools or mutate durable state. Its output is a proposal until validated.

### 6. Decision Validator

Checks the model output against schemas and state.

Validates:

- decision type is allowed
- referenced tool exists
- arguments match schema
- referenced entities exist or can be created
- confidence/ambiguity rules
- approval requirement
- policy class

Invalid decisions become model-correction events or user-facing clarification.

### 7. Tool Registry

Catalog of registered tools.

A registered tool includes:

- name
- natural-language summary
- input schema
- output schema
- policy action
- implementation reference
- toolkit ID
- lifecycle status
- visibility rules
- examples

The registry may load tools from hand-written core toolkits and generated toolkits.

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

Policy is deterministic and auditable.

### 9. Executor

Runs registered tool implementations.

Executor responsibilities:

- resolve implementation reference
- run in the right sandbox/environment
- enforce timeout and resource limits
- capture stdout/stderr/artifacts
- normalize result
- emit events

Executor does not decide what should exist. It only runs registered tools after validation and policy.

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
- sandbox execution
- forbidden APIs
- dependency declarations
- documentation completeness

Only validated toolkits can be registered.

## Runtime versus builder boundary

```text
Runtime:
  - receives user input
  - builds context
  - invokes registered tools
  - records state
  - requests missing tools

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
Level 4: Toolkit registered but approval-gated
Level 5: Tool allowed for current context
Level 6: Tool executed and result recorded
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
- tool execution returns results without recording them

## Minimal viable architecture

The first build does not need everything. Minimum useful system:

1. Event ledger.
2. State projector.
3. Context composer.
4. Decision schema.
5. Static tool registry.
6. Policy gate.
7. Tool Need object.
8. Builder stub that emits toolkit templates.

Even if tools are not fully generated on day one, Tool Needs should be first-class from the beginning.
