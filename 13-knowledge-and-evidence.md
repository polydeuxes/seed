# 13 Knowledge and Evidence

Seed is not a chatbot memory system.

Seed is an evidence-to-fact system.

The primary job of the runtime is to transform observations into trustworthy state.

Core pipeline:

```text
Observation
  -> Evidence
  -> Fact Extraction
  -> Fact Validation
  -> State Projection
  -> Context Composition
```

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

Fact extraction and validation then condense the collected evidence into Facts. Conflicting evidence should remain visible through provenance rather than being silently averaged away.

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
- observed time
- expiry or freshness policy
- confidence
- validation status

Facts can become stale, conflict with newer facts, or be superseded. Evidence remains immutable; Facts are the state projection layer used for context and decisions.

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

### Verification Toolkit

Tools:

- `verify_service_status`
- `verify_disk_usage`
- `verify_container_health`
- `verify_ssh_access`

Purpose:

Convert operational observations into facts.

Verification tools should prefer direct observations of the current environment and should emit evidence records suitable for deterministic fact extraction.

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
