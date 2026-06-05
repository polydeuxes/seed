# 01 Architecture

## System summary

Seed is best understood as a state engine / distributed state machine that can use LLMs as one possible `DecisionProvider`; it is not primarily an agent framework. It safely turns raw inputs into append-only events, projects evidence-backed state, composes context, validates proposed decisions, applies policy, and records auditable outcomes. Seed does **not** own shell execution, arbitrary provider-output execution, secrets, host mutation, retries, scheduling, or long-running workflow lifecycle.

Seed has two large halves:

1. **Runtime** — handles events, builds context, lets models decide, records state, manages Tool Needs, ranks recommendations, and emits non-executable Action Plans and HandoffPlans.
2. **Builder** — turns explicit Tool Needs into generated toolkit candidates, validates metadata/contracts, and prepares capabilities for registration.

The runtime is always conservative. The builder can be creative, but its outputs are untrusted until validated and registered. Actual execution is delegated to external providers.

## High-level flow

The core loop is the product:

```text
Input
  -> Events
  -> State
  -> Context
  -> Decision
  -> Policy
  -> Execution
  -> Events
```

Runtime sovereignty is explicit: the model/provider proposes decisions, the runtime validates decisions, policy allows or denies valid tool decisions, and `ToolRegistry` execution is limited to registered handlers. Raw provider output is never executed, and generated tools are not active merely because they exist.


## File-backed raw IN inspection

File-backed raw IN is inspected before source/parser dispatch:

```text
raw IN
  -> InputInspector
  -> source/parser dispatch
  -> ObservationSource
  -> ObservationNormalizer
  -> ObservationIngestor
  -> Evidence / Facts / State
```

`InputInspector` treats a filename extension as a hint, never as authority. It reads files without executing them, importing them, or following includes; detects obvious JSON, YAML, INI, empty, unknown, and null-byte inputs; and records classification plus size/hash audit metadata in an `InputArtifact`. It is not a security scanner, but it prevents obvious parser misrouting and makes the dispatch decision auditable. Unsupported formats remain the responsibility of the source/parser layer, and source adapters remain read-only and non-executing.


## Semantic catalogs

Seed separates knowledge vocabulary from action/handoff vocabulary through small semantic catalogs:

- `PredicateCatalog` defines what can be known: canonical predicate names, value types, cardinality, units, and provider-specific mappings. Cardinality matters because single-valued predicates create current-belief winner/conflict behavior, while multi-valued predicates such as aliases, groups, and IP addresses can hold several current values.
- `RelationshipCatalog` defines how entities connect: identity, topology, dependency, hosting, grouping, and other graph semantics used for traversal and validation.
- `EntityTypeCatalog` defines what kind of thing an entity is and which predicates or relationships are valid for that type.
- `CapabilityCatalog` defines what can be recommended or handed off, including external provider metadata, policy actions, operation names, target schemas, and visibility. It does not grant execution capability to Seed.
- `InferenceCatalog` defines deterministic reasoning rules. These rules project inferred facts from already-projected observations; they are not LLM reasoning, shell invocation, host mutation, or network calls.

## Knowledge projection

The knowledge layer projects current belief from immutable observations rather than treating the latest model answer as state. Core projection responsibilities include:

- Facts derived from Evidence with confidence and provenance.
- FactSupport aggregates grouped by `subject + predicate + value`.
- Predicate cardinality for single-valued conflict handling and multi-valued current sets.
- Measurements distinguished from durable facts. Measurements are retained as current projected samples with bounded recent history while Prometheus or another upstream system remains the historian.
- Identity and alias resolution so inventory names, IPs, endpoint subjects, and hostnames can converge without hiding provenance.
- Relationships and topology projection from facts using the RelationshipCatalog.
- Entity type projection and validation using EntityTypeCatalog rules.
- Graph validation for impossible edges, unknown types, ambiguous identity, and type/predicate mismatches.
- Explanation/why queries that traverse fact support, conflicts, inference links, and provenance without adding a new reasoning mechanism.

## Boundary clarity

- `EventLedger` = historical event source.
- `ProjectionStore` = cached current world-model snapshots; it never becomes the source of truth.
- `State` = current projected world model derived from the EventLedger.
- `State Views` = read-only representations of projected State for facts, observations, requirements, capabilities, issues, and summary counts. They are projection views, not a second state store.
- `RuntimeLoop` = coordinator for one request execution.
- `DecisionProvider` = proposes structured decisions; it may be deterministic code, a model adapter, or another provider. LLMs are optional, not required.
- `PolicyEngine` = authorization/safety boundary for valid tool decisions.
- `ToolRegistry` = executable capability registry; only registered handlers may run, and Seed does not execute shell commands or arbitrary provider text.
- `DecisionJournal` = append-only audit/explanation trail that records why a decision was made and what happened afterward.

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
- DecisionJournal events for why/outcome explanations
- State Views that answer what Seed currently knows without reading raw events or invoking runtime behavior

Seed delegates:

- unregistered or arbitrary execution
- shell commands and host mutation
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

Seed may record a HandoffPlan and later ingest external provider observations as Evidence, but it must not become the executor of record for host automation. RuntimeLoop v1 may invoke only registered in-process `ToolRegistry` handlers and records their results, unknown-tool rejections, policy denials, malformed decisions, and failures as events.

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

### State Views

State Views expose the current world model without requiring callers to read raw events. `seed_runtime/state_views.py` builds read-only `FactView`, `ObservationView`, `RequirementView`, `CapabilityView`, `IssueView`, and `StateSummary` objects from an already projected `State`.

State Views answer:

- What does Seed currently know?
- What facts exist?
- What requirements exist?
- What capabilities exist?
- What issues exist?

They are projections and not separate persistence systems. They do not append events, replay runtime decisions, invoke `RuntimeLoop`, call providers, evaluate policy, execute tools, run shell commands, or perform network calls. CLI flags such as `--current-facts`, `--current-observations`, `--current-requirements`, `--current-capabilities`, `--current-issues`, and `--state-summary` load projected State, reuse `ProjectionStore` snapshots when available, and render plain text.

### Context Views

Context Views are the supported boundary between Seed's knowledge system and decision-making. `seed_runtime/context_views.py` builds a deterministic `DecisionContextView` from already-projected State plus the Evidence Graph, Contradiction Detection, and Confidence Aggregation layers. Future `DecisionProvider` implementations should consume Context Views instead of directly traversing raw `State` structures.

The knowledge-to-decision path is:

```text
Events
→ State
→ Evidence
→ Contradictions
→ Confidence
→ Context Views
→ DecisionProvider
```

Context Views answer:

- What is currently true?
- What evidence supports it?
- What conflicts exist?
- How confident are we?
- What should the provider see?

Context Views are projections. They are read-only and do not append events, mutate State, replay runtime behavior, invoke `RuntimeLoop`, call providers, evaluate policy, execute tools, call LLMs, run shell commands, perform network calls, or create a new persistence layer. The v1 selection rules are intentionally simple and deterministic: supported facts are selected first, higher confidence sorts first, contradicted facts remain visible but marked, and unsupported facts are excluded by default. Operators can inspect the exact provider-facing projection with `--decision-context`.


#### Fact Support Aggregation

Verification is not a separate subsystem in Seed's core architecture. A provider check, user correction, discovery result, imported record, or deterministic inference enters the system as Evidence and Facts. The projector then groups Facts by `subject + predicate + value` into FactSupport objects.

Seed preserves provenance instead of stamping a claim with `verified: true`. The current belief for a `subject + predicate` is derived from:

- supporting Facts for each value
- conflicting Facts for other values
- aggregate confidence
- source type strength (`discovery`/`provider`/observed sources generally outrank inferred-only support)
- recency via latest observation time

This keeps disagreement auditable: multiple values can remain in state while `get_best_fact(subject, predicate)` returns the representative Fact for the best-supported current belief.


### ProjectionStore

`EventLedger` owns append-only facts about what happened. `ProjectionStore` owns cached projected state derived from those events: current facts, FactSupport aggregates, aliases, entity types, relationship edges, graph issues, recommendations, and cache metadata. The current SQLite implementation is intentionally portable: it favors deterministic rebuilds and simple tables so the same projection boundary can move to Postgres later. Operator flags such as `--rebuild-state-cache` and `--state-cache-status` expose this cache lifecycle without changing the ledger.

### 4. Context Composer

Builds compact model-facing packets from projected knowledge. The supported knowledge input for future decision providers is the Decision Context View, not direct traversal of raw State dictionaries.

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

The catalog may load capabilities from hand-written metadata, generated toolkit metadata, MCP server descriptions, and external automation inventory. It describes what Seed can recommend or hand off; it does not imply that Seed can execute the operation itself. For the canonical distinction between requirements, capabilities, operations, implementations, providers, toolkits, and ToolNeeds, see `02-domain-model.md`.

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

Produces non-mutating integration artifacts first:

- `InputInspector` when a new raw input class needs safe pre-dispatch inspection
- `ObservationSource` adapters
- `ObservationNormalizer` logic
- `PredicateCatalog` entries
- `RelationshipCatalog` entries
- `CapabilityCatalog` entries
- `HandoffProvider` metadata
- tests
- docs and validation reports

Generated artifacts describe observation and handoff integration before they describe mutation. They must not add Seed-owned secret handling, shell execution, host mutation, retries, or scheduling.

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
  - receives and inspects raw input
  - normalizes observations into Evidence and Facts
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

## Canonical predicate vocabulary

`PredicateCatalog` is Seed's vocabulary for **what can be known**. It defines each canonical predicate's semantics, value type, and cardinality. Semantics distinguish volatile measurements from durable facts. Cardinality controls whether multiple values are valid simultaneously: `single` predicates select one current belief and may project conflicts, while `multi` predicates maintain support independently for every current value and do not conflict solely because multiple values exist. `CapabilityCatalog` remains Seed's vocabulary for **what can be done**.

For example, `runtime` has `cardinality: single`, so `runtime=docker` and
`runtime=systemd` disagree. Identity and grouping predicates such as `alias` and
`group` have `cardinality: multi`, so all supported values remain current.

Providers emit raw, provider-specific observations. The default observation normalization pipeline preserves those raw observations and their provenance, then runs `EndpointAliasNormalizer`, `EndpointIdentityNormalizer`, and `PredicateNormalizer`, in that order. Predicate normalization derives canonical observations from catalog mappings after identity aliases have been discovered; it never overwrites the provider observation.

Seed reasons over canonical predicates when they are available while preserving raw observations for auditability and backward compatibility. Canonical predicate metadata supplies measurement semantics where possible; legacy raw measurement predicates continue to work during migration.

### Measurement retention policy

Seed is a current-belief and audit system, not a time-series database. Durable facts retain projected history and aggregate independent support. Measurement predicates use current-sample semantics: projection keeps only the latest sample for each canonical subject/alias component, predicate, and dimensions tuple. The default projected measurement history limit is `N=1`; callers may explicitly request a larger recent `N` for debugging, but only the latest retained sample is current. Projection retention never deletes append-only events; physical deletion is reserved for a future explicit compaction operation. Prometheus remains the historian for measurement time series, while Seed stores current belief and audit events. Filesystem measurement dimensions are `mountpoint`, `device`, and `fstype`.

## Relationship projection

Facts are claims about entities. Relationships are derived topology edges between
entities, projected from facts while preserving the source fact's provenance.
`RelationshipCatalog` is Seed's vocabulary for entity connections. It complements
`PredicateCatalog` (what can be known) and `CapabilityCatalog` (what can be done).
Relationships are inspect-only projected state; they are never directly injected
or executed.

### InferenceCatalog and deterministic projection

Seed's catalogs have separate responsibilities:

- `PredicateCatalog` defines vocabulary: what can be known.
- `RelationshipCatalog` defines topology semantics: how entities connect.
- `EntityTypeCatalog` defines entity classes: what kind of thing an entity is.
- `InferenceCatalog` defines deterministic reasoning rules: which current facts imply projection artifacts.
- `CapabilityCatalog` defines capabilities: what can be done.

`InferenceCatalog` is not LLM reasoning. The `StateProjector` applies its local, declarative rules only after observed and canonical facts have been projected. Inferred facts are reproducible projection artifacts from unambiguous observed/current facts; they carry their source fact and rule IDs, respect predicate cardinality, cap confidence at the source fact's confidence, and cannot overwrite observed facts. Inference projection performs no command execution, shell invocation, host mutation, network access, or model call.
