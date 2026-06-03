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

The biggest conceptual shift is:

```text
Conductor:
Tools -> Actions

Seed:
Evidence -> Facts -> State -> Decisions -> Tools
```

The fact system is more important than the tool system. Tools are how Seed observes and acts; evidence and facts are how Seed knows what is true enough to decide.

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

Seed may use multiple workers, tools, or subagents to investigate the same goal.

These branches should not be treated as independent authorities. Their primary output is Evidence, not final truth. Parallel workers and subagents do not merge opinions; they emit Evidence. Seed merges Evidence into Facts.

A worker may return:

- raw observations
- tool outputs
- cited document excerpts
- failed attempts
- uncertainty notes
- candidate facts

The runtime records these as Events and Evidence.

Fact extraction and deterministic support aggregation then condense the collected evidence into Facts and current-belief projections. Conflicting evidence should remain visible through provenance rather than being silently averaged away.

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

## Recommended Toolkit Roadmap

### Knowledge Toolkit

Tools:

- `wikipedia_lookup`
- `wikidata_lookup`
- `document_search`
- `document_extract`

Purpose:

Provide retrieved and structured knowledge.

Knowledge toolkit outputs should be recorded as Evidence. Structured source results may also feed fact extraction when validation rules are available.

### Observation Toolkit

Tools:

- `observe_service_status`
- `observe_disk_usage`
- `observe_container_health`
- `observe_ssh_access`

Purpose:

Convert operational observations into evidence-backed observed Facts.

Observation tools should prefer direct observations of the current environment and should emit Evidence records suitable for deterministic fact extraction and Fact Support Aggregation. Existing names such as `verify_ssh_access` should be treated as observation surfaces, not as a reason to add a standalone verification subsystem.

### Computation Toolkit

Tools:

- `sympy_compute`
- `unit_convert`
- `statistical_summary`

Purpose:

Perform deterministic calculations.

Computation tool outputs should also be recorded as Evidence so any derived answer can cite its inputs and deterministic result.

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

SymPy should be exposed as a toolkit rather than embedded into the runtime.

Example:

```text
User:
Solve x^2 - 5x + 6 = 0

Decision:
propose_handoff_plan(sympy_compute via MCP/manual backend)

Result:
x = 2
x = 3
```

The result should be recorded as evidence and returned to the user. If the answer is stored for future use, it should be projected into a Fact with a provenance link back to the computation Evidence.
