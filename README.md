# Seed System 

Seed receives observations, records evidence, projects explainable state, and answers questions about what it knows and why; capability resolution operates downstream of projected knowledge rather than defining the system itself.

## One-sentence product definition

Seed receives observations from users, files, providers, local read-only sources, and system inputs; records evidence; projects evidence-backed facts into explainable current state; answers questions about what it knows and why; and only then may resolve capability gaps into registered-operation candidates or provider recommendations without implying execution, verification, or availability.

## Core thesis

Permissions, flow control, and capability catalogs are necessary infrastructure, but they are not the center of gravity. Seed's architecture is knowledge-first:

```text
Observation Sources
  -> Observations
  -> Evidence
  -> Facts
  -> Relationships
  -> Entity Types
  -> Contradictions
  -> Current-State Projection
  -> Explanation
  -> Query / Response
```

Capability handling is a consumer of projected knowledge, not the primary architecture:

```text
Projected State
  -> ToolNeed
  -> Capability Resolution
  -> Registered Operation Candidates
  -> Provider Recommendations
  -> Response
```

A `ToolNeed` records a capability gap. Capability resolution is read-only inventory and recommendation over projected state and catalogs. It does not execute operations, verify capabilities, prove provider availability, or mutate hosts.

## Architectural Principles

- **Observation first.** Seed begins by observing narrow facts about the world, not by choosing operations.
- **Evidence before conclusions.** Claims should be supported by evidence and `FactSupport` links before they are projected into state.
- **Inventory before inference.** Seed should first inventory what is observed, known, registered, configured, or recommended before deriving broader conclusions.
- **Inference before execution.** Deterministic inference can reason over projected facts, but it remains separate from observation and execution.
- **Execution last.** Registered-operation execution is a later, policy-governed runtime path; it is not implied by knowledge, capability gaps, recommendations, or explanations.
- **Observe narrowly. Infer broadly.** Observation vocabulary should stay within the selected source boundary so later reasoning can preserve uncertainty, staleness, and contradiction.
- **Capability resolution does not imply execution.** `request_tool` records and resolves a gap; `call_tool` is the runtime path to `ToolExecutor`.
- **Capability resolution does not imply verification.** Requested, known, candidate, and provider-recommended capabilities are unverified unless a future scoped verification model proves otherwise.
- **Provider recommendations do not imply availability.** A recommendation is metadata for a possible provider or handoff, not evidence that the provider is reachable or ready.
- **Local configuration does not imply reachability.** Local observations may prove configuration, but they do not prove remote access, service health, or network success.

## What is new

Most automation systems begin with execution: a workflow engine, provider adapter, shell command, or catalog of hand-written operations. Seed begins with knowledge:

```text
Observation -> Evidence -> Fact -> State -> Explanation
```

Only after projected state exists does Seed reason about downstream capability surfaces:

```text
Capability -> Operation -> Provider
```

This means Seed first asks what was observed, what evidence supports it, what facts are currently projected, whether facts conflict or have gone stale, and how the answer can be explained. Capability gaps, registered operations, and provider recommendations remain useful, but they are downstream of the knowledge model rather than the organizing principle.

The growth order is deliberate:

1. Inventory before inference.
2. Inference before execution.
3. Execution last.

The model does not get unrestricted power to rewrite its runtime. It can answer from state, ask for missing information, or request a `ToolNeed` that records a capability gap. A separate builder and validation pipeline may produce toolkit metadata, operation contracts, schemas, and policies. A `CapabilityCatalog`, `ToolRegistry`, and policy gate decide what becomes visible as registered-operation candidates or provider/handoff recommendations, and those recommendations still do not imply execution, verification, or availability.

## Design principles

1. **Observation before execution**  
   Seed should prefer observation and projected knowledge before introducing operations, provider calls, shell access, or host mutation.

2. **Evidence-backed claims**  
   Facts, explanations, contradictions, and current-state views should be traceable to evidence and `FactSupport`; unsupported claims should remain visible as unsupported rather than silently promoted.

3. **State before cleverness**  
   The model should reason over explicit projected state, not hidden conversational vibes, implicit provider assumptions, or prompt-only memory.

4. **Explainability by default**  
   Operator-facing answers should be able to explain what Seed believes, why it believes it, which evidence supports it, and whether projected facts conflict, are stale, or are unsupported.

5. **Small-model pressure is good**  
   Design so a small model can succeed: compact context, explicit choices, typed actions, deterministic validation, and knowledge surfaces that do not require hidden orchestration.

6. **Capability resolution is not execution**  
   `ToolNeed` creation, capability catalog lookup, registered-operation candidate discovery, and provider recommendation are read-only reasoning artifacts until an explicit, policy-governed execution path is invoked.

7. **Least privilege first**  
   Capability growth should prefer existing projected facts, existing observations, local read-only data, and narrow external read-only sources before considering inference, elevated privilege, or execution.

8. **Every result returns to state**  
   Answers, questions, observations, evidence, facts, ToolNeeds / capability gaps, capability resolution results, external provider evidence, approvals, and generated toolkit artifacts all become durable events or projected state. Legacy compatibility artifacts may still be projected for historical compatibility, but they are not Core MVP runtime orchestration.

## Current MVP slice

### Seed currently knows how to

- observe user, file, provider, local host, Ansible inventory, and Prometheus read-api inputs through safe intake paths
- normalize provider predicates into canonical vocabulary
- classify entities through `EntityTypeCatalog`
- relate topology and dependency facts through `RelationshipCatalog`
- resolve aliases and identity links
- project append-only events into current state through `StateProjector` and `ProjectionStore`
- explain why it believes a projected fact through evidence, provenance, support links, recursive inference, alias resolution, ambiguity, and conflicts
- inventory current facts, observations, requirements, capabilities, issues, evidence, entity types, relationships, graph issues, unsupported facts, and capability verification status vocabulary
- surface conservative read-only contradictions between projected facts without resolving them by mutation
- track temporal state through current projection, latest measurement semantics, timestamps, expiry, stale filtering, and refresh recommendations
- infer deterministic facts through `InferenceCatalog` while keeping inference separate from observation
- resolve capabilities into `ToolNeeds`, registered-operation candidates, and provider/handoff recommendations downstream of projected knowledge

### Seed currently does not own

- execution as a general automation engine
- host mutation
- workflow orchestration
- scheduling
- authorization workflows or action-plan orchestration
- provider implementations
- shell access or arbitrary shell commands
- secrets
- retries
- RuntimeLoop or any second runtime orchestration path
- Prometheus history
- Ansible, Temporal, AWX, MCP, or manual-provider execution

## Document map

Read in this order for the current knowledge-first architecture:

1. [`docs/architecture.md`](docs/architecture.md) — generated system architecture, ownership, and component boundaries.
2. [`docs/invariants.md`](docs/invariants.md) — runtime, execution, projection, capability, verification, and quarantine invariants.
3. [`docs/reasoning_roadmap.md`](docs/reasoning_roadmap.md) — accepted Core MVP reasoning boundaries and next foundation areas.
4. [`docs/capability_extension_methodology.md`](docs/capability_extension_methodology.md) — how to grow capabilities from narrow observations and evidence.
5. [`docs/capability_verification_vocabulary.md`](docs/capability_verification_vocabulary.md) — vocabulary for requested, known, candidate, provider-recommended, and verified capabilities.
6. [`docs/availability_vocabulary_audit.md`](docs/availability_vocabulary_audit.md) — availability, reachability, and local-configuration boundaries.
7. [`docs/roadmap_reconciliation.md`](docs/roadmap_reconciliation.md) — reconciliation of implemented, partial, and missing reasoning capabilities.
8. [`docs/contradiction_handling_audit.md`](docs/contradiction_handling_audit.md) and [`docs/temporal_reasoning_audit.md`](docs/temporal_reasoning_audit.md) — current contradiction and temporal semantics.

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

Seed is not primarily an agent framework. Its knowledge architecture is:

```text
Observation -> Evidence -> Fact -> State -> Explanation
```

Its runtime architecture consumes projected knowledge:

```text
Input -> EventLedger -> State Projection -> Context Composer -> DecisionProvider -> Decision Validation -> PolicyGate / ToolExecutionPolicyService -> ToolExecutor registered operation or Answer -> New Events
```

The provider proposes; the runtime validates; `PolicyGate` / `ToolExecutionPolicyService` govern whether execution may proceed; `ToolRegistry` exposes registered operation contracts; and `ToolExecutor` executes registered operations. `CapabilityCatalog` provides non-executable provider/handoff recommendations. Runtime decisions are made from projected state and compact context, not from a separate planner or RuntimeLoop. Raw provider output is never executed, LLMs are optional, generated toolkit operations are not active by default, and Seed does not run shell commands or arbitrary host mutation. `DecisionJournal` records decision reason, context hash, selected operation/tool, policy status, final outcome, and errors as append-only events so future `--why`, audit, explain, impact, relationship, graph issue, and verification commands can explain both what happened and why.

## Mental model

Seed should feel less like this:

```text
User -> API route -> hardcoded workflow -> provider call
```

And more like this:

```text
User -> Observation -> Evidence -> Fact -> State -> Explanation -> Response
```

The API is not the center. The context loop depends on a more fundamental knowledge loop:

```text
Observations -> Evidence Graph -> Facts -> projected State -> Fact explanations
Observations -> Evidence Graph -> Facts -> projected State -> Contradiction Detection
Projected State -> Decisions -> Answers / ToolNeeds / Registered Operation Candidates / Provider Recommendations
```

Registered operations and provider handoffs are downstream capability surfaces. Evidence, facts, state, the read-only Evidence Graph, and read-only Contradiction Detection are how Seed knows what is true enough to answer, why a fact is believed, whether a fact is unsupported, and whether projected facts conflict. Contradictions are not resolutions: Seed reports that facts cannot both be true and shows evidence for each side, but it does not choose a winner or mutate state.

## Capability Growth

New capabilities should follow the [Capability Extension Methodology](docs/capability_extension_methodology.md): start from a knowledge gap, reduce it to the narrowest answerable question, and prefer the least-privileged observation source that can support the narrowest fact.

```text
Capability Gap
  -> Required Question
  -> Narrowest Fact
  -> Least-Privileged Source
  -> Read-Only Observation
  -> Observation
  -> Evidence
  -> Fact
  -> Projection
  -> Explanation
```

Capability growth should prefer local observations, read-only sources, narrow facts, and explicit evidence before introducing inference or execution behavior. A new capability should not require write access, provider mutation, shell execution, network probing, runtime changes, or `ToolExecutor` changes unless the extension is explicitly reviewed as execution work rather than observation work.

## Local model development CLI

Seed includes a maintained local runtime CLI for testing the current runtime path with local models through Ollama's `/api/generate` endpoint. The CLI builds the same intent-first decision path used by the runtime (`IntentDecisionModel` + `TextIntentClassifier` + `IntentPromptModelClient`) and loads the core echo toolkit, so local testing tracks repository code changes instead of relying on a separate local-only script.

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

For canonical local intake, use repeatable `--observe SUBJECT PREDICATE VALUE` flags. `--source-type` and numeric `--confidence VALUE` preserve observation provenance, while `--fact-expires-at` or `--fact-ttl-seconds` can make the derived Fact expire for stale-fact checks:

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

Ask for read-only confidence aggregation over projected facts. Confidence estimates support strength; it is not truth resolution and does not rewrite facts, delete unsupported facts, resolve contradictions, invoke runtime behavior, call providers/policy/operations, or append events:

```bash
python scripts/seed_local.py --db seed.sqlite --confidence
python scripts/seed_local.py --db seed.sqlite --confidence-fact jellyfin runtime docker
```

Confidence Aggregation v1 is deterministic: one evidence node gives at least weak support, two or more evidence nodes give strong support, explicit projected fact confidence is preserved when higher, contradicted facts receive a small penalty, and unsupported facts without explicit confidence score `0.0`.

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

Normal CLI and HTTP responses are JSON objects with `response` and `events`. `--raw` prints the raw model completion so you can debug the local model's intent JSON before Seed parses it. The CLI and HTTP paths use `Runtime`, the single canonical runtime path. Runtime trace support is intentionally read-only: `RuntimeTrace` reconstructs a single recorded run from ledger events. The maintained CLI exposes two plain-text views over that reader for completed runs stored in the event ledger:

```bash
python scripts/seed_local.py --db seed.sqlite --trace-run evt_000001
python scripts/seed_local.py --db seed.sqlite --why-run evt_000001
```

`--trace-run RUN_ID` prints the workspace, run id, user input, decision kind/reason/context hash, policy status, selected operation/tool, final outcome/response/error, and ordered event list. `--why-run RUN_ID` prints a shorter human explanation of what the user asked, what Seed decided, why, whether policy allowed it, and what happened. Both commands are read-only: they do not replay the runtime, call providers, evaluate policy, execute operation implementations, ingest observations, or append events. If no `--db` is supplied, they follow the CLI's in-memory convention and will only see an empty process-local ledger, so unknown or missing runs print a clear not-found message.

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

The maintained CLI exposes read-only operator queries over projected state. State Views are projections over the current world model rather than a separate persistence layer. These queries do not ingest new observations, append events, execute operation implementations, mutate hosts, call providers/policy, or ask an LLM to reason over projection state:

- `--state-summary` prints a read-only State View summary with counts for facts, observations, requirements, capabilities, issues, projection version, and last projected event.
- `--impact ENTITY` resolves aliases and summarizes an entity's current types, aliases, availability, local network configuration, endpoints, groups, dependencies, dependents, conflicts, and related graph issues. Local network impact output prioritizes the primary/default-route interface with its observed local IP and default gateway, collapses virtual/container/VPN interfaces into a count, and explicitly does not infer reachability or availability from interface facts.
- `--why ENTITY PREDICATE` explains the current belief by traversing FactSupport, provenance, conflicts, aliases, and deterministic inference links.
- `--unhealthy` and `--down` list currently unhealthy or unavailable entities/endpoints from projected facts.
- `--graph-issues` reports topology/type validation findings.
- `--relationships` prints projected relationship edges, optionally filtered by relationship.
- `--entity-types` prints projected entity classifications.
- `--current-facts` prints all read-only projected Fact Views; `--current-facts ENTITY PREDICATE` keeps the focused current-fact query for a subject/predicate. This remains the complete view for local network facts, including Docker, bridge, veth, virtual, and VPN interfaces that default `--impact` output may collapse.
- `--current-observations`, `--current-requirements`, `--current-capabilities`, and `--current-issues` print read-only State Views for the rest of the projected world model.
- `--decision-context` prints the exact read-only Context View that a `DecisionProvider` receives: confidence-bearing facts, contradiction flags, issues, requirements, capabilities, and summary counts.
- `--evidence` prints the read-only Evidence Graph summary and concise evidence-to-fact links.
- `--why-fact SUBJECT PREDICATE [OBJECT]` explains a matched projected fact with confidence, evidence, and supporting event IDs.
- `--unsupported-facts` lists projected facts that currently have no linked supporting evidence.


Local host network observation is read-only and local-only: it reads Python standard-library interface data plus safe local files such as `/proc/net/route`, `/proc/net/dev`, `/proc/net/if_inet6`, `/sys/class/net/*`, `/etc/resolv.conf`, and, when present, systemd-networkd lease files under `/run/systemd/netif/leases`. Interface role classification is derived from local names and default-route evidence: the default-route interface is `primary`, `lo` is `loopback`, Docker/bridge/veth interfaces are `container`, `virbr*` is `virtual`, Tailscale/WireGuard-style interfaces are `vpn`, and unknown non-default interfaces remain `secondary`. Address assignment is only emitted when explicit evidence exists; for example, a matching systemd-networkd lease marks an IPv4 address as `dhcp`. Static assignment is not guessed from absence of DHCP evidence because it normally requires manager-specific configuration interpretation, so it remains unknown unless a future explicit read-only evidence source supports it.

### Inference catalog

Seed's built-in `InferenceCatalog` defines deterministic reasoning rules that project new facts from unambiguous current observed facts. It is not LLM reasoning and it never executes commands, mutates hosts, or performs network calls. `PredicateCatalog` defines the vocabulary for what can be known, `RelationshipCatalog` defines topology semantics, `EntityTypeCatalog` defines entity classes, `InferenceCatalog` defines deterministic reasoning rules, and `CapabilityCatalog` defines what can be done.

Inferred facts are projection artifacts rather than observations. They are marked with `source_type=inferred` and `inferred=true`, link back to the activating fact and catalog rule through `source_fact_id` and `inference_rule_id`, never exceed the source fact's confidence, and never overwrite observed facts. Single-cardinality predicate ambiguity suppresses inference. Use `--show-inference-catalog` to inspect the built-in rules.

### Performance and projection cache

Seed uses an event-sourced performance model. `EventLedger` owns append-only events and audit history; deterministic projectors derive current state; `ProjectionStore` owns cached projected state for fast operator queries and context composition. The Evidence Graph is another read-only projection over State, not a separate persistence layer or evidence database. The current implementation is SQLite-backed for local portability, with schema boundaries kept narrow enough to move to Postgres later. Use `--rebuild-state-cache` to rebuild cached projections from the ledger and `--state-cache-status` to inspect cache freshness and coverage.

## Next comparison task

After this documentation refresh, create a branch at the earlier prototype point and compare the original proto/control-loop approach with the current knowledge/handoff runtime. The comparison should identify what improved, what became overbuilt, and what should be simplified before the next implementation push.
