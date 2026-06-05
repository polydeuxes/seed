# Seed System 

A system that accumulates context, understands missing capabilities, and safely grows a typed tool vocabulary.

## One-sentence product definition

Seed receives raw user, file, provider, and system inputs; safely inspects and normalizes them into Evidence-backed Facts; projects a knowledge graph and current state; presents compact context to an LLM; lets the LLM answer, ask, request ToolNeeds, or propose non-executable ActionPlans/HandoffPlans; and records every result back into state.

## Core thesis

Permissions and flow control are necessary infrastructure, but they are not the architecture. The architecture is the **context engine** plus a **tool-growing loop**:

```text
raw input
  -> InputInspector
  -> ObservationSource
  -> ObservationNormalizer
  -> ObservationIngestor
  -> Evidence / Facts / FactSupport
  -> projected knowledge state
  -> context packet
  -> model decision
  -> ToolNeed, recommendation, ActionPlan, or HandoffPlan
  -> validation/policy metadata/build/external-provider handoff
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
7. Expose registered capabilities and provider handoff options back to the model.

The model does not get unrestricted power to rewrite its runtime. It can request and help specify capabilities. A separate builder and validation pipeline produce capability metadata/contracts. A CapabilityCatalog and policy gate decide what becomes available for handoff planning.

## Design principles

1. **State before cleverness**  
   The model should reason over explicit state, not hidden conversational vibes.

2. **Small-model pressure is good**  
   Design so a small model can succeed: short context, explicit choices, typed actions, deterministic validation.

3. **Tools are generated products, not prompt tricks**  
   A toolkit is a manifest, schemas, policy metadata, integration contracts, tests, documentation, and lifecycle state; execution stays with external providers.

4. **Desire is not permission**  
   A model or user can desire an action. Policy decides whether Seed may recommend a non-executable handoff; external providers decide and perform actual execution.

5. **Generated does not mean trusted**  
   Generated toolkits must be sandboxed, tested, classified, reviewed when needed, and registered before use.

6. **The runtime does not build itself while running production actions**  
   Tool/capability building is separate from external-provider execution, which Seed does not own.

7. **Every action returns to state**  
   Answers, questions, ToolNeeds, ActionPlans, HandoffPlans, external provider evidence, approvals, and generated artifacts all become durable events.


## Current MVP slice

Seed can now:

- inspect and ingest inputs safely
- ingest Ansible inventory and Prometheus observations
- ingest local host observations
- normalize provider predicates into canonical vocabulary
- resolve aliases and identity links
- classify entities through `EntityTypeCatalog`
- project topology relationships through `RelationshipCatalog`
- detect graph issues
- infer deterministic facts through `InferenceCatalog`
- explain why it believes something
- summarize current state
- produce non-executable plans and handoffs

Seed still does **not**:

- execute host commands
- handle secrets
- schedule jobs
- retry work
- replace Prometheus as historian
- replace Ansible, Temporal, AWX, MCP, or manual providers as executor

## Document map

Read in this order:

1. [`01-architecture.md`](01-architecture.md) — system overview and component boundaries.
2. [`02-domain-model.md`](02-domain-model.md) — names and core objects.
3. [`03-runtime-loop.md`](03-runtime-loop.md) — event-to-context-to-decision handoff loop.
4. [`04-toolkit-system.md`](04-toolkit-system.md) — generated toolkit format and lifecycle.
5. [`05-policy-and-safety.md`](05-policy-and-safety.md) — trust boundaries, risk classes, approval model.
6. [`06-context-engine.md`](06-context-engine.md) — how to build model context packets.
7. [`07-builder-service.md`](07-builder-service.md) — separate tool builder design.
8. [`08-small-model-strategy.md`](08-small-model-strategy.md) — designing for small local models and model tiers.
9. [`09-pseudocode.md`](09-pseudocode.md) — implementation sketches.
10. [`10-build-plan.md`](10-build-plan.md) — multi-day Codex session plan.
11. [`11-naming.md`](11-naming.md) — better names and terms to avoid.
12. [`12-open-questions.md`](12-open-questions.md) — decisions to make while building.
13. [`13-knowledge-and-evidence.md`](13-knowledge-and-evidence.md) — evidence-to-fact pipeline and knowledge source trust classes.

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
    catalogs/
    context/
    decisions/
    events/
    handoff/
    knowledge/
    ledger/
    policy/
    projection_store/
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

## Runtime architecture update

Seed is not primarily an agent framework. It is a state engine / distributed state machine whose core loop is:

```text
Input -> EventLedger -> State Projection -> Context Composer -> DecisionProvider -> Decision Validation -> PolicyEngine -> ToolRegistry or Answer -> New Events
```

The provider proposes; the runtime validates; policy allows or denies; and `ToolRegistry` can execute only registered handlers. Raw provider output is never executed, LLMs are optional, generated tools are not active by default, and Seed does not run shell commands or arbitrary host mutation. `DecisionJournal` records decision reason, context hash, selected tool, policy status, final outcome, and errors as append-only events so future `--why`, audit, explain, impact, relationship, graph issue, and verification commands can explain both what happened and why.

## Mental model

Seed should feel less like this:

```text
User -> API route -> hardcoded workflow -> provider call
```

And more like this:

```text
User -> event -> state -> context -> model decision -> validated action -> state
```

The API is not the center. The context loop is the center, and the context loop depends on a more fundamental knowledge loop:

```text
Events -> projected State -> Evidence Graph -> Fact explanations
Evidence -> Facts -> State -> Decisions -> Tools
```

Tools are how Seed observes and acts. Evidence, facts, state, and the read-only Evidence Graph are how Seed knows what is true enough to decide and why a fact is believed.

## Local model development CLI

Seed includes a maintained local runtime CLI for testing the current runtime loop with local models through Ollama's `/api/generate` endpoint. The CLI builds the same intent-first decision path used by the runtime (`IntentDecisionModel` + `TextIntentClassifier` + `IntentPromptModelClient`) and loads the core echo toolkit, so local testing tracks repository code changes instead of relying on a separate local-only script.

Start Ollama and pull a small model if needed:

```bash
ollama pull qwen2.5:3b
```

Run one-shot messages:

```bash
python scripts/seed_local.py "echo hello"
python scripts/seed_local.py "install docker"
python scripts/seed_local.py --raw "what is the weather in Jacksonville?"
```

Seed known local-development facts before a message with repeatable `--fact SUBJECT PREDICATE VALUE` flags. `--fact` is only a dev shorthand: the canonical intake remains an `Observation`, and the CLI routes each shorthand through `ObservationIngestor` so the ledger records `Observation -> Evidence -> Fact -> State` instead of appending Facts directly. This makes it useful for recommendation-ranking checks without hardcoding a specific service into the runtime. For example, this observed runtime fact should rank Docker lifecycle recommendations above systemd service recommendations:

```bash
python scripts/seed_local.py \
  --fact jellyfin runtime docker \
  "restart jellyfin?"
```

Use additional `--fact` flags to seed more than one shorthand observation:

```bash
python scripts/seed_local.py \
  --fact jellyfin runtime docker \
  --fact nas platform linux \
  "restart jellyfin?"
```

For canonical local intake, use repeatable `--observe SUBJECT PREDICATE VALUE` flags. `--source-type` and `--confidence` preserve observation provenance, while `--fact-expires-at` or `--fact-ttl-seconds` can make the derived Fact expire for stale-fact checks:

```bash
python scripts/seed_local.py \
  --observe jellyfin runtime docker \
  --source-type discovery \
  --confidence 0.81 \
  --fact-support jellyfin runtime
```

Ask for a deterministic explanation of a projected belief, including observed provenance, recursive inference rules, alias resolution, ambiguity, and conflicts:

```bash
python scripts/seed_local.py --db seed.sqlite --why node115 health_status
python scripts/seed_local.py --db seed.sqlite --why jellyfin runtime
```

Live read-only observation sources can collect practical host and monitoring metadata without execution, credentials, mutation, shell commands, or arbitrary PromQL. `--observe-ansible-inventory PATH` inspects raw file content before parser dispatch, treats `.ini`, `.yml`, and `.yaml` extensions only as fallback hints, and emits authoritative hostname, `ansible_host`, IP-address, alias, and group observations without invoking Ansible or connecting to hosts. `--observe-local-host` uses Python standard-library platform and disk APIs to emit the local hostname's OS, architecture, and `/` disk totals. `--observe-prometheus BASE_URL` performs HTTP `GET` requests to Prometheus's read API with a fixed allowlist of safe metric names: `up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`. Prometheus `up` samples also emit the metric's `job` label as the endpoint's durable `endpoint_role`. Use `--db` when you want the resulting observations to persist across CLI runs:

```bash
python scripts/seed_local.py --observe-local-host

python scripts/seed_local.py \
  --db .seed-local.sqlite \
  --observe-ansible-inventory inventory.ini \
  --observe-prometheus http://10.0.0.201:9090 \
  --observe-timeout 5
```

Seed projects measurements as current belief rather than an unbounded time series. By default it retains the latest sample per canonical subject/alias component, predicate, and dimensions; filesystem dimensions are `mountpoint`, `device`, and `fstype`. Endpoint availability and derived endpoint health remain scoped to the exact endpoint rather than being flattened into its host alias component. A larger recent projection history can be explicitly requested for debugging, while append-only audit events remain untouched until an explicit future compaction operation. Prometheus remains the historian.

All read-only sources ingest through `ObservationCollectionService`. Prometheus intake prints a concise summary by default: the ingested observation count, discovered hosts/instances, and counts by predicate. Add `--verbose-observations` to print every ingested fact. Use `--prometheus-instance INSTANCE` or `--prometheus-mountpoint MOUNTPOINT` to limit Prometheus ingestion; without those filters, the full allowlisted metric intake is ingested unchanged. If Prometheus is unreachable, the source fails gracefully by ingesting zero observations.

By default, the CLI posts intent prompts to `http://localhost:11434/api/generate` with model `qwen2.5:3b`, `stream: false`, and JSON-formatted output enabled. Use `--model` to select another local model:

```bash
python scripts/seed_local.py --model qwen2.5:3b "echo hello"
```

Run without a message to open shell mode:

```bash
python scripts/seed_local.py
```

Run HTTP mode for lightweight local integration tests:

```bash
python scripts/seed_local.py --http
curl -s http://127.0.0.1:8765/message \
  -H 'Content-Type: application/json' \
  -d '{"message":"echo hello"}'
```

Normal CLI and HTTP responses are JSON objects with `response` and `events`. `--raw` prints the raw model completion so you can debug the local model's intent JSON before Seed parses it. Runtime trace support is intentionally read-only: `RuntimeTrace` reconstructs a single RuntimeLoop run from ledger events. The maintained CLI exposes two plain-text views over that reader for completed RuntimeLoop runs stored in the event ledger:

```bash
python scripts/seed_local.py --db seed.sqlite --trace-run evt_000001
python scripts/seed_local.py --db seed.sqlite --why-run evt_000001
```

`--trace-run RUN_ID` prints the workspace, run id, user input, decision kind/reason/context hash, policy status, selected tool, final outcome/response/error, and ordered event list. `--why-run RUN_ID` prints a shorter human explanation of what the user asked, what Seed decided, why, whether policy allowed it, and what happened. Both commands are read-only: they do not replay the runtime, call providers, evaluate policy, execute tools, ingest observations, or append events. If no `--db` is supplied, they follow the CLI's in-memory convention and will only see an empty process-local ledger, so unknown or missing runs print a clear not-found message.

### Predicate catalog

Seed's built-in `PredicateCatalog` defines the canonical vocabulary for what can be known and maps provider-specific observations into canonical observations without discarding the originals. Each predicate declares its semantics, value type, and cardinality. `single` predicates such as `runtime` retain winner/conflict behavior; `multi` predicates such as `alias`, `group`, and `ip_address` keep independently supported values current without creating a conflict solely because several values exist. The default normalization order is endpoint alias, endpoint identity, then predicate normalization. Use `--predicate-catalog PATH` to load a custom JSON catalog for observation-source ingestion and projection, or `--show-predicate-catalog` to print canonical predicates and mappings. `CapabilityCatalog` separately describes what can be done.

Inspect every current value of a multi-valued predicate with:

```bash
python scripts/seed_local.py --db seed.sqlite --current-facts node115 alias
```

### Inspect projected relationships

Seed derives topology edges from facts using `relationship_catalog/core.json`.
Facts describe claims about entities, relationships describe how entities connect,
and capabilities describe what Seed can do. Each catalog relationship declares a
`relationship_kind`: `identity`, `topology`, `dependency`, `hosting`, or `grouping`.
The kind is preserved on projected edges and controls graph traversal semantics:
`find_dependencies(entity)` and `find_dependents(entity)` traverse dependency and
hosting edges, while excluding identity and grouping edges. This semantic metadata
also gives future reasoning systems a stable way to distinguish what an edge means.

```bash
python scripts/seed_local.py --db seed.sqlite --relationships
python scripts/seed_local.py --db seed.sqlite --relationships --relationship member_of
```

Inspect one entity's projected status and blast radius with `--impact ENTITY`. The
read-only query resolves aliases and reports current types, aliases, host availability,
endpoint availability grouped by role, groups, dependencies, dependents, active
conflicts, and related graph issues without ingesting observations or executing tools.

```bash
python scripts/seed_local.py --db seed.sqlite --impact node115
```

Inspect graph validation findings with `--graph-issues`; add `--severity warning`
or `--severity error` to focus on one severity. Unknown or ambiguous entity types
are warnings, while known type mismatches are errors. `--state-summary` reports
warning and error totals separately so warnings do not present the graph as
unhealthy in the same way as errors.

```bash
python scripts/seed_local.py --db seed.sqlite --graph-issues --severity warning
python scripts/seed_local.py --db seed.sqlite --state-summary
```

### Operator query surfaces

The maintained CLI exposes read-only operator queries over projected state. State Views are projections over the current world model rather than a separate persistence layer. These queries do not ingest new observations, append events, execute tools, mutate hosts, call providers/policy, or ask an LLM to reason over projection state:

- `--state-summary` prints a read-only State View summary with counts for facts, observations, requirements, capabilities, issues, projection version, and last projected event.
- `--impact ENTITY` resolves aliases and summarizes an entity's current types, aliases, availability, endpoints, groups, dependencies, dependents, conflicts, and related graph issues.
- `--why ENTITY PREDICATE` explains the current belief by traversing FactSupport, provenance, conflicts, aliases, and deterministic inference links.
- `--unhealthy` and `--down` list currently unhealthy or unavailable entities/endpoints from projected facts.
- `--graph-issues` reports topology/type validation findings.
- `--relationships` prints projected relationship edges, optionally filtered by relationship.
- `--entity-types` prints projected entity classifications.
- `--current-facts` prints all read-only projected Fact Views; `--current-facts ENTITY PREDICATE` keeps the focused current-fact query for a subject/predicate.
- `--current-observations`, `--current-requirements`, `--current-capabilities`, and `--current-issues` print read-only State Views for the rest of the projected world model.
- `--evidence` prints the read-only Evidence Graph summary and concise evidence-to-fact links.
- `--why-fact SUBJECT PREDICATE [OBJECT]` explains a matched projected fact with confidence, evidence, and supporting event IDs.
- `--unsupported-facts` lists projected facts that currently have no linked supporting evidence.

### Inference catalog

Seed's built-in `InferenceCatalog` defines deterministic reasoning rules that project new facts from unambiguous current observed facts. It is not LLM reasoning and it never executes commands, mutates hosts, or performs network calls. `PredicateCatalog` defines the vocabulary for what can be known, `RelationshipCatalog` defines topology semantics, `EntityTypeCatalog` defines entity classes, `InferenceCatalog` defines deterministic reasoning rules, and `CapabilityCatalog` defines what can be done.

Inferred facts are projection artifacts rather than observations. They are marked with `source_type=inferred` and `inferred=true`, link back to the activating fact and catalog rule through `source_fact_id` and `inference_rule_id`, never exceed the source fact's confidence, and never overwrite observed facts. Single-cardinality predicate ambiguity suppresses inference. Use `--show-inference-catalog` to inspect the built-in rules.

### Performance and projection cache

Seed uses an event-sourced performance model. `EventLedger` owns append-only events and audit history; deterministic projectors derive current state; `ProjectionStore` owns cached projected state for fast operator queries and context composition. The Evidence Graph is another read-only projection over State, not a separate persistence layer or evidence database. The current implementation is SQLite-backed for local portability, with schema boundaries kept narrow enough to move to Postgres later. Use `--rebuild-state-cache` to rebuild cached projections from the ledger and `--state-cache-status` to inspect cache freshness and coverage.

## Next comparison task

After this documentation refresh, create a branch at the earlier prototype point and compare the original proto/control-loop approach with the current knowledge/handoff runtime. The comparison should identify what improved, what became overbuilt, and what should be simplified before the next implementation push.
