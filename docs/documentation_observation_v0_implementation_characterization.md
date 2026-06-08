# Documentation Observation v0 Implementation Characterization

## Purpose

This document characterizes the smallest useful implementation slice for Documentation Observation v0.

It intentionally moves from architectural description toward implementation constraints without changing runtime behavior.

The goal is to define a tiny, deterministic claim extraction slice.

## Implementation Slice

Documentation Observation v0 should extract explicit documentation-backed claims from only:

```text
README.md
docs/architectural_knowledge_map.md
```

No recursive docs scan.

No model interpretation.

No repository observation.

No repository reconciliation.

## Why This Slice

These two files are enough to prove the path:

```text
Documentation
        ↓
Claim
        ↓
Evidence metadata
```

They contain front-door claims about:

* Seed identity;
* process-layer concerns;
* representation-layer concerns;
* architectural status;
* current frontier;
* rejected concepts;
* reading order.

## Non-Goals

This slice must not implement:

* repository observation;
* repository reconciliation;
* claim support projection;
* self-model projection;
* runtime behavior;
* ToolExecutor integration;
* EventLedger ownership changes;
* ProjectionStore ownership changes;
* LLM claim extraction;
* broad markdown summarization.

## Input Boundary

Inputs are plain markdown files.

Allowed file paths:

```text
README.md
docs/architectural_knowledge_map.md
```

The extractor should fail closed if given other paths unless the allowlist is explicitly expanded.

## Extraction Boundary

Allowed extraction structures:

```text
headings
bullet lists
numbered lists
tables
fenced text diagrams
explicit rejection phrases
explicit boundary phrases
```

Disallowed extraction structures:

```text
narrative paragraphs unless they match explicit claim patterns
examples
CLI commands
code samples
historical commentary
speculation
```

## Claim Families In Scope

V0 claim families:

```text
repository_identity
process_layer
representation_layer
status
frontier
rejected_concept
reading_order
ownership
boundary
```

V0 should prefer fewer correct claims over many fuzzy claims.

## Expected Claims From README.md

Minimum expected extraction:

```text
Seed is a knowledge-oriented runtime.
Seed transforms observations into evidence-backed projected knowledge.
Knowledge Acquisition precedes Knowledge Integrity.
Knowledge Integrity precedes Knowledge Selection.
Knowledge Selection precedes Response.
Knowledge Acquisition is the active capability frontier.
Knowledge Integrity is stable.
Knowledge Selection is stable.
Response is stable.
Architectural Findings are partially reconciled.
Users Observation is a current capability-growth priority.
Groups Observation is a current capability-growth priority.
Package Observation is a current capability-growth priority.
Systemd Observation is a current capability-growth priority.
```

If the README includes the Knowledge Representation section, expected representation claims include:

```text
Observation leads to Evidence.
Evidence leads to Fact.
Fact leads to Support Relationship.
Support Relationship leads to Claim.
Evidence supports facts.
Facts support claims.
Claim Support is not a reasoning engine.
Claim Support is not an inference engine.
Claim Support is not a truth system.
Claim Support is not an architecture engine.
```

## Expected Claims From docs/architectural_knowledge_map.md

Minimum expected extraction:

```text
The architectural knowledge map is not a source of truth.
The architectural knowledge map is not a registry.
The architectural knowledge map is not an inventory.
The architectural knowledge map is not a runtime model.
The architectural knowledge map is not a governance process.
The architectural knowledge map is not a replacement for canonical documents.
Knowledge Acquisition is an active frontier.
Knowledge Integrity is stable.
Knowledge Selection is stable.
Response is complete enough.
Response Caveats are complete enough and paused.
Knowledge Representation is emerging and reconciled.
Architectural Findings are partially reconciled.
Evidence supports facts.
Facts support claims.
Acquisition creates knowledge.
Integrity characterizes knowledge.
Selection chooses knowledge.
Response communicates knowledge.
```

Expected rejected concept claims:

```text
ReasoningEngine is rejected.
IntegrityEngine is rejected.
SelectionEngine is rejected.
ResponseEngine is rejected.
CaveatEngine is rejected.
ContextEngine is rejected.
Planner is rejected.
WorkflowEngine is rejected.
ClaimStore is rejected.
SupportStore is rejected.
Claim-to-claim reasoning chains are rejected.
```

## Evidence Metadata

Every extracted claim should preserve:

```text
source_path
source_heading
line_range
extraction_kind
raw_text
normalized_claim
claim_family
```

`line_range` is preferred but may be approximate in an initial fixture-only characterization.

## Normalization

Normalization should be conservative.

Examples:

```text
README text: Knowledge Acquisition — active capability frontier
normalized claim: Knowledge Acquisition is the active capability frontier.
```

```text
map bullet: `ResponseEngine`
heading context: Rejected Concepts
normalized claim: ResponseEngine is rejected.
```

Do not normalize broad prose into claims unless the extraction pattern is explicit.

## Output Shape

A future implementation can expose extracted claims as plain records before integrating with state projection.

Conceptual record:

```text
DocumentationClaim
  source_path
  source_heading
  line_range
  claim_family
  normalized_claim
  raw_text
  extraction_kind
```

This record is an implementation convenience, not a new architectural store.

## Tests To Add Later

If implemented, tests should use tiny markdown fixtures.

Test categories:

```text
extracts heading-scoped rejected concepts
extracts status table rows
extracts process diagrams
extracts reading-order items
preserves evidence metadata
does not extract CLI examples
does not extract narrative commentary
does not scan outside allowlist
```

Tests should not touch Runtime, ToolExecutor, EventLedger, or ProjectionStore.

## Success Criteria

Documentation Observation v0 succeeds when:

```text
Given README.md and docs/architectural_knowledge_map.md,
Seed can deterministically extract a bounded set of explicit documentation claims
with source evidence metadata.
```

## Failure Criteria

The slice fails if implementation requires:

```text
LLM extraction
runtime invocation
repository scanning
semantic summarization
truth arbitration
claim support projection
repository reconciliation
```

## Recommended Next Step

Implement only a fixture-level extractor or CLI/dev helper that demonstrates deterministic claim extraction from the two allowlisted files.

Do not connect it to Runtime.

Do not connect it to ToolExecutor.

Do not project Claim Support yet.

## Conclusion

Documentation Observation v0 should be tiny.

It should prove that explicit documentation claims can be acquired as structured, evidence-backed records.

Only after that works should Seed consider repository observation or reconciliation implementation.