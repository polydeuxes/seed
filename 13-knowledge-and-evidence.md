# 13 Knowledge and Evidence

Seed is not a chatbot memory system.

Seed is an evidence-to-fact system.

The primary job of the runtime is to transform observations into trustworthy state.

Core pipeline:

```text
Observation
  -> Evidence
  -> Fact Extraction
  -> Fact Support Aggregation
  -> State Projection
  -> Context Composition
```

Local development seeding follows the same single intake path. `scripts/seed_local.py --observe` is the canonical CLI surface, and `--fact` is a developer shorthand that creates an Observation before `ObservationIngestor` derives Evidence and a Fact. There should not be a separate CLI path that appends `fact.observed` directly.

### Endpoint identity normalization

Endpoint-scoped operational facts often use an `IP:PORT` or `hostname:PORT` subject while inventory facts use a stable node name. The default observation normalization pipeline bridges those identities only when the same observation batch contains an explicit `ip_address`, `alias`, or `ansible_host` relationship. For example:

```text
Inventory:  node115 -> 192.168.254.115
Metrics:    192.168.254.115:9100 -> up / os / filesystem_*
Normalizer: node115 -> 192.168.254.115:9100
```

`EndpointIdentityNormalizer` derives a `node115 alias 192.168.254.115:9100` observation, allowing alias-aware fact queries for `node115` to find endpoint-scoped facts. The derivation preserves the endpoint and matched identity provenance. It does not infer relationships from naming or node-number conventions, contain source-specific logic, execute commands, make network calls, mutate hosts, or call external services.

The biggest conceptual shift is:

```text
Conductor:
Operations / Handoffs -> Actions

Seed:
Evidence -> Facts -> State -> Decisions -> Operations / Handoffs
```

The fact system is more important than the operation/toolkit system. Registered operations and provider handoffs are how Seed observes and acts; evidence and facts are how Seed knows what is true enough to decide. See `02-domain-model.md` for the canonical capability/operation/implementation/provider/toolkit vocabulary.

## Knowledge Sources

Seed should classify knowledge by source and trust posture before it reaches the context engine.

### Operational Sources

Examples:

- Prometheus
- SSH
- Docker
- Kubernetes
- Home Assistant
- Cloud APIs
- Databases
- Monitoring systems

These sources describe reality and should be preferred for operational decisions.

Operational observations are not automatically permanent truths. They should become Evidence first, then be transformed into fresh Facts with explicit provenance, confidence, and expiry.

### Structured Knowledge Sources

Examples:

- Wikidata
- Internal asset inventories
- CMDB systems
- Metadata catalogs

These sources provide structured facts.

Structured knowledge can often be projected into Facts directly, but Seed should still preserve the Evidence record that explains where the fact came from and when it was observed.

### Document Sources

Examples:

- Documentation
- RFCs
- Wikis
- Git repositories
- Runbooks

Document sources produce evidence, not immediate facts.

A documentation excerpt can support a fact only after extraction and validation. This keeps retrieved text separate from the state Seed relies on for decisions.

## Evidence

Evidence is an immutable raw observation.

Examples:

- Prometheus query result
- SSH command output
- API response
- User statement
- Documentation excerpt
- Wikidata record

Evidence should preserve the original payload as much as practical, plus source metadata and observation time. Multiple Facts may be extracted from one Evidence record, and one Fact may cite multiple Evidence records.

## Parallel Evidence Collection

Seed may use multiple workers, operation implementations, or subagents to investigate the same goal.

These branches should not be treated as independent authorities. Their primary output is Evidence, not final truth. Parallel workers and subagents do not merge opinions; they emit Evidence. Seed merges Evidence into Facts.

A worker may return:

- raw observations
- operation outputs
- cited document excerpts
- failed attempts
- uncertainty notes
- candidate facts

The runtime records these as Events and Evidence.

Fact extraction and deterministic support aggregation then condense the collected evidence into Facts and current-belief projections. Conflicting evidence should remain visible through provenance rather than being silently averaged away.

Projection Integrity Summary is a read-only composition over those projected structures. It aggregates existing Evidence Graph unsupported-fact counts, FactConflict records, Contradiction views, GraphValidationIssue records, stale fact helpers, refresh recommendations, and capability verification inventory states. It does not add a parallel truth system, execute verification or refreshes, resolve contradictions, call providers, mutate facts, or mutate projections. Integrity signals are not truth judgments: unsupported, unverified, stale, contradicted, missing evidence, and missing observations do not mean false.

This allows Seed to accumulate experience from multiple attempts or viewpoints without turning subagent text into unverified state.

Pattern:

```text
Goal
  -> parallel investigation branches
  -> Evidence records
  -> Fact extraction / validation
  -> State projection
  -> Context composition
  -> next decision
```

Core rule:

```text
Subagents collect experience.
Seed decides what becomes state.
```

## Facts

Facts are projected interpretations of Evidence.

Facts should include:

- subject
- predicate
- value
- supporting evidence IDs
- source type (`user`, `discovery`, `provider`, `inferred`, or `imported`)
- observed time
- expiry or freshness policy
- confidence (defaulting by source type to 0.90, 0.95, 0.85, 0.60, or 0.70)
- confidence derived from source type and support

Facts can become stale, conflict with newer facts, or be superseded. Inferred Facts should use `source_type: "inferred"` and cap confidence at or below the source Fact's confidence. Evidence remains immutable; Facts are the state projection layer used for context and decisions. Seed should preserve provenance rather than adding `verified: true`; current belief is derived from supporting/conflicting facts, confidence, source type, and recency.


## Fact Support Aggregation

Verification is modeled as more evidence entering the system. If an operator, provider, monitor, discovery source, or import supports or disputes an existing claim, Seed records another Evidence-backed Fact. It does not create a separate FactVerification object and does not overwrite the claim with a boolean verified stamp.

The projector groups Facts by `subject + predicate + value` and produces FactSupport objects containing:

- subject
- predicate
- value
- supporting Fact IDs
- source types
- aggregate confidence
- first observed time
- latest observed time

Aggregate confidence increases when multiple independent sources support the same value. Conflicting values remain visible as conflicting Facts for the same `subject + predicate`. `get_best_fact(subject, predicate)` returns a representative Fact for the best-supported current belief, based on support, confidence, source type, and recency. Inferred-only support is intentionally weaker than direct observed/provider/discovery support.

Terminology:

- **Observed fact** — a Fact extracted from direct user input, provider output, discovery, or imported data.
- **Inferred fact** — a deterministic Fact derived from other Facts.
- **Supporting fact** — a Fact that has the same subject, predicate, and value as another claim.
- **Conflicting fact** — a Fact that has the same subject and predicate but a different value.
- **Best fact/current belief** — the representative Fact for the value with the strongest aggregate support.


## Raw IN pipeline and live examples

The knowledge layer starts before parsing. File-backed and provider-backed raw inputs flow through:

```text
raw input
  -> InputInspector
  -> ObservationSource
  -> ObservationNormalizer
  -> ObservationIngestor
  -> Evidence / Facts
```

Current live read-only examples are Ansible inventory ingestion, Prometheus observation ingestion, and local host observation. Ansible inventory is inspected as raw file content before parser dispatch and does not invoke Ansible or connect to hosts. Prometheus ingestion uses allowlisted read API queries and keeps Prometheus as the historian. Local host observation uses local read-only platform/disk APIs to emit observations about the current machine.

## ProjectionStore and operator queries

The `EventLedger` owns append-only events. `ProjectionStore` owns cached projected state derived from those events: current facts, FactSupport aggregates, recent measurements, alias/identity indexes, relationship edges, entity types, graph validation findings, and explanation inputs. Measurements are projected as current samples with bounded retention rather than an unbounded time series; durable facts and measurement facts stay distinguishable through predicates, dimensions, timestamps, and provenance.

Operators can inspect this projection with read-only queries such as `--state-summary`, `--impact ENTITY`, `--why ENTITY PREDICATE`, `--unhealthy`, `--down`, `--graph-issues`, `--relationships`, `--entity-types`, `--current-facts`, and `--decision-context`. Cache lifecycle is explicit through `--rebuild-state-cache` and `--state-cache-status`.

## Context Views and the decision boundary

Context Views formalize how projected knowledge becomes runtime context. The target knowledge path is:

```text
Events
→ State
→ Evidence
→ Contradictions
→ Confidence
→ Context Views
→ DecisionProvider
```

A `DecisionContextView` is assembled only from projected State, the Evidence Graph, Contradiction Detection, and Confidence Aggregation. It carries decision-ready facts with confidence, contradiction flags, and evidence counts, plus projected issues, requirements, capabilities, and summary counts. Unsupported facts are excluded by default; contradicted facts are retained and marked so providers can see conflicts without Seed resolving or hiding them.

Context Views are read-only projections. They do not execute runtime behavior, invoke providers, invoke operation implementations, evaluate policy, call LLMs, mutate State, append events, replay the ledger, or create new persistence. Future providers must consume Context Views rather than directly traversing State structures, preserving a clear boundary between the knowledge layer and decision-making.

## Recommended Toolkit Roadmap

### Knowledge Toolkit

Operations:

- `wikipedia_lookup`
- `wikidata_lookup`
- `document_search`
- `document_extract`

Purpose:

Provide retrieved and structured knowledge.

Knowledge toolkit outputs should be recorded as Evidence. Structured source results may also feed fact extraction when validation rules are available.

### Observation Toolkit

Operations:

- `observe_service_status`
- `observe_disk_usage`
- `observe_container_health`
- `observe_ssh_access`

Purpose:

Convert operational observations into evidence-backed observed Facts.

Observation operations should prefer direct observations of the current environment and should emit Evidence records suitable for deterministic fact extraction and Fact Support Aggregation. Existing names such as `verify_ssh_access` should be treated as observation surfaces, not as a reason to add a standalone verification subsystem or internal execution lifecycle.

### Computation Toolkit

Operations:

- `sympy_compute`
- `unit_convert`
- `statistical_summary`

Purpose:

Perform deterministic calculations.

Computation operation outputs should also be recorded as Evidence so any derived answer can cite its inputs and deterministic result.

## Symbolic Computation

Seed does not require Wolfram.

Recommended implementation:

- SymPy

Capabilities:

- algebra
- calculus
- equation solving
- symbolic manipulation
- units
- matrices
- statistics

SymPy should be exposed through a toolkit rather than embedded into the runtime.

Example:

```text
User:
Solve x^2 - 5x + 6 = 0

Decision:
propose_handoff_plan(sympy_compute via MCP/manual provider backend)

Result:
x = 2
x = 3
```

The result should be recorded as evidence and returned to the user. If the answer is stored for future use, it should be projected into a Fact with a provenance link back to the computation Evidence.

## Explanation Engine (`--why`)

Seed's explanation layer answers why a projected belief is current without adding a new reasoning mechanism. It deterministically traverses the already-projected fact support, conflicts, alias resolution, provenance, and inference links. It performs no external command execution, shell invocation, host mutation, network request, or LLM call.

The three related concepts have distinct responsibilities:

- **Provenance** records where knowledge came from: supporting Fact IDs, Evidence IDs, source types, confidence, and observation times.
- **Inference** records how deterministic rules derived new knowledge: `inference_rule_id`, `source_fact_id`, and any applied confidence cap.
- **Explanation** renders a human-readable recursive traversal of provenance and inference for an operator query.

For a directly observed fact, an explanation shows its supporting facts, evidence, source types, observed confidence, and observation time. For an inferred fact, it shows the rule, source fact, inferred confidence, any rule confidence cap, and recursively explains the source fact. Alias-resolved queries include the deterministic identity-resolution path. Multi-valued predicates return every current value; ambiguous or blocked single-valued predicates return the competing supported values and conflict details.

```bash
python scripts/seed_local.py --db seed.sqlite --why node115 health_status
python scripts/seed_local.py --db seed.sqlite --why node115 alias
python scripts/seed_local.py --db seed.sqlite --why jellyfin runtime
```

`ExplanationBuilder` consumes only a projected `State`. Its result model separates current beliefs from competing beliefs so future `--why-not`, `--how`, and `--what-changed` query modes can reuse the traversal; those modes are not implemented yet.
