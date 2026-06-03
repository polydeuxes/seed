# Seed System Blueprint

This directory is a portable architecture packet for a new repository. It is written to be copied out of this codebase without depending on legacy module names.

## Working name

**Seed**: a context-native runtime that grows operational tools from recorded capability gaps.

The name is intentionally different from the old repo. The core idea is not a gateway, not an automation wrapper, and not a permission engine. It is a system that accumulates context, understands missing capabilities, and safely grows a typed tool vocabulary.

## One-sentence product definition

Seed receives unique user or system inputs, turns them into durable state, presents a compact context packet to an LLM, lets the LLM answer, ask, request ToolNeeds, or propose non-executable ActionPlans/HandoffPlans, and records every result back into state.

## Core thesis

Permissions and flow control are necessary infrastructure, but they are not the architecture. The architecture is the **context engine** plus a **tool-growing loop**:

```text
input
  -> event record
  -> state update
  -> context packet
  -> model decision
  -> ToolNeed, ActionPlan, or HandoffPlan
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

The API is not the center. The context loop is the center, and the context loop depends on a more fundamental knowledge loop:

```text
Evidence -> Facts -> State -> Decisions -> Tools
```

Tools are how Seed observes and acts. Evidence, facts, and state are how Seed knows what is true enough to decide.

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

Live read-only observation sources can collect practical host and monitoring metadata without execution, credentials, mutation, shell commands, or arbitrary PromQL. `--observe-ansible-inventory PATH` inspects raw file content before parser dispatch, treats `.ini`, `.yml`, and `.yaml` extensions only as fallback hints, and emits authoritative hostname, `ansible_host`, IP-address, alias, and group observations without invoking Ansible or connecting to hosts. `--observe-local-host` uses Python standard-library platform and disk APIs to emit the local hostname's OS, architecture, and `/` disk totals. `--observe-prometheus BASE_URL` performs HTTP `GET` requests to Prometheus's read API with a fixed allowlist of safe metric names: `up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`. Use `--db` when you want the resulting observations to persist across CLI runs:

```bash
python scripts/seed_local.py --observe-local-host

python scripts/seed_local.py \
  --db .seed-local.sqlite \
  --observe-ansible-inventory inventory.ini \
  --observe-prometheus http://10.0.0.201:9090 \
  --observe-timeout 5
```

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

Normal CLI and HTTP responses are JSON objects with `response` and `events`. `--raw` prints the raw model completion so you can debug the local model's intent JSON before Seed parses it.
