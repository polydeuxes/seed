# Documentation Observation Characterization

## Purpose

This document characterizes Documentation Observation v0.

It defines the exact documentation facts Seed should be able to extract from a small canonical documentation allowlist before any implementation begins.

This is documentation-only.

It does not require or justify Runtime, ToolExecutor, EventLedger, ProjectionStore, provider, model-client, or test changes.

## Scope

Documentation Observation v0 asks:

```text
What does the repository say it is meant to be?
```

It does not ask:

```text
What does the repository actually contain?
Does code match documentation?
Which source is ultimately correct?
What should be implemented next?
```

Those questions belong to later Repository Observation and Repository Reconciliation work.

## Source Allowlist

V0 should be limited to three canonical front-door documents:

1. `README.md`
2. `docs/README.md`
3. `docs/architectural_knowledge_map.md`

These files are enough to characterize the primitive because they contain:

* high-level identity statements;
* primary concern ordering;
* recommended reading order;
* canonical document lists;
* current frontier statements;
* rejected concepts;
* boundary and non-goal language.

V0 should not scan all documentation recursively.

## Observation Boundary

Documentation Observation v0 observes documentation structure and explicit claims.

Allowed evidence structures:

* headings
* bullet lists
* numbered lists
* markdown tables
* fenced `text` diagrams
* fenced `mermaid` diagrams
* explicit boundary phrases such as `is not`, `does not own`, `rejected`, `current frontier`, and `canonical documents`

Disallowed extraction behavior:

* broad prose summarization
* model-required interpretation
* inferring implementation from roadmap text
* resolving contradictions between documents
* choosing the most authoritative document automatically
* scanning source code
* executing commands
* calling providers
* appending runtime events outside a future normal observation ingestion path

## V0 Fact Families

Documentation Observation v0 should only produce narrow architectural facts.

Initial fact families:

| Fact family | Meaning |
| --- | --- |
| `repository_identity` | What the repository says Seed is. |
| `architectural_concern` | A primary or supporting architectural concern. |
| `concern_order` | Ordered lifecycle relationships between concerns. |
| `documentation_concern` | A concern that preserves architectural memory rather than runtime behavior. |
| `canonical_document` | A document associated with a concern or reading path. |
| `reading_order` | Recommended document order. |
| `current_frontier` | Current architectural or capability frontier. |
| `rejected_concept` | Explicitly rejected concept or engine. |
| `ownership_boundary` | Explicit ownership or non-ownership claim. |
| `non_goal` | Explicit statement of what Seed is not. |

These are documentation-grounded claims, not proof of implementation.

## Expected V0 Facts From README.md

The top-level README should support at least these documentation observations.

### Repository identity

```text
Seed is a knowledge-oriented runtime.
Seed transforms observations into evidence-backed projected knowledge.
Seed uses projected knowledge to support decisions, recommendations, explanations, capability resolution, and operator understanding.
```

### Primary concern order

```text
Knowledge Acquisition precedes Knowledge Integrity.
Knowledge Integrity precedes Knowledge Selection.
Knowledge Selection precedes Response.
```

### Documentation concern

```text
Architectural Findings is an additional documentation concern.
```

### Emphasis facts

```text
Seed emphasizes evidence-backed knowledge.
Seed emphasizes explicit ownership boundaries.
Seed emphasizes deterministic projection.
Seed emphasizes read-only explanation and integrity surfaces.
Seed emphasizes small-context decision making.
Seed emphasizes audit-before-implementation architecture.
```

### Non-goals

```text
Seed is not a planner.
Seed is not a workflow engine.
Seed is not a reasoning engine.
Seed is not an orchestration framework.
Seed is not an autonomous execution platform.
```

### Navigation facts

```text
README.md points new readers to docs/architectural_knowledge_map.md.
README.md points new readers to docs/README.md.
README.md points new readers to docs/architectural_status_and_next_frontier.md.
```

### Current status facts

```text
Knowledge Acquisition is the active capability frontier.
Knowledge Integrity is stable.
Knowledge Selection is stable.
Response is stable.
Architectural Findings is partially reconciled.
```

### Capability-growth priorities

```text
Users Observation is a current capability-growth priority.
Groups Observation is a current capability-growth priority.
Package Observation is a current capability-growth priority.
Systemd Observation is a current capability-growth priority.
```

## Expected V0 Facts From docs/README.md

The docs README should support documentation-navigation and concern facts.

### Documentation identity

```text
docs/ contains architectural knowledge, audits, vocabularies, reconciliations, status reviews, roadmaps, and observation designs.
```

### Recommended reading order

```text
docs/architectural_knowledge_map.md is recommended first.
docs/architectural_findings_preservation.md is recommended second.
docs/architectural_status_and_next_frontier.md is recommended third.
docs/reasoning_roadmap.md is recommended fourth.
```

### Concern order

```text
Knowledge Acquisition precedes Knowledge Integrity.
Knowledge Integrity precedes Knowledge Selection.
Knowledge Selection precedes Response.
```

### Concern frontier facts

```text
Users Observation is a Knowledge Acquisition frontier.
Groups Observation is a Knowledge Acquisition frontier.
Package Observation is a Knowledge Acquisition frontier.
Systemd Observation is a Knowledge Acquisition frontier.
```

### Important finding facts

```text
Selection Rationale Summary implementation is not currently justified.
Response exists primarily as communication of selected and characterized knowledge.
Architectural memory already exists.
Architectural Findings discoverability remains weaker than preservation.
```

## Expected V0 Facts From docs/architectural_knowledge_map.md

The architectural knowledge map should support concern, status, canonical-document, and rejection facts.

### Map identity

```text
docs/architectural_knowledge_map.md is a lightweight navigation map for Seed architectural knowledge.
docs/architectural_knowledge_map.md exists to reduce rediscovery cost.
docs/architectural_knowledge_map.md is not a source of truth.
docs/architectural_knowledge_map.md is not a registry.
docs/architectural_knowledge_map.md is not an inventory.
docs/architectural_knowledge_map.md is not a runtime model.
docs/architectural_knowledge_map.md is not a governance process.
docs/architectural_knowledge_map.md is not a replacement for canonical documents.
```

### Concern status facts

```text
Knowledge Acquisition is an active frontier.
Knowledge Integrity is stable.
Knowledge Selection is stable.
Response is complete enough.
Response Caveats are complete enough and paused.
Architectural Findings are partially reconciled.
```

### Acquisition facts

```text
Acquisition answers what Seed knows.
Acquisition creates evidence-backed projected knowledge.
Acquisition does not own explanation.
Acquisition does not own integrity characterization.
Acquisition does not own selection.
Acquisition does not own response composition.
Acquisition does not own provider execution.
Acquisition does not own truth arbitration.
```

### Implemented local observation slice facts

```text
Identity Observation is implemented.
Mount Observation is implemented.
Kernel / CPU / Memory Observation is implemented.
Local Network Observation is implemented.
Storage Topology Observation is implemented.
Listening Port Observation is implemented.
Local Host Observation is implemented.
```

### Acquisition frontier facts

```text
Users Observation is a highest-value next slice.
Groups Observation is a highest-value next slice.
Package Observation is a highest-value next slice.
Systemd Observation is a highest-value next slice.
Schedule Observation is a planned slice.
Certificate Observation is a planned slice.
Process Marker Observation is a planned slice.
Container Marker Observation is a planned slice.
```

### Integrity facts

```text
Integrity answers whether projected knowledge can be safely interpreted.
Integrity characterizes knowledge.
Integrity does not determine truth.
Integrity is read-only over projected knowledge.
Projection Integrity Summary v0 is implemented composition.
Projection Integrity Navigation v0 is implemented composition.
```

### Selection facts

```text
Selection answers what projected knowledge matters now and why.
Selection rationale already exists across distributed surfaces.
Selection Rationale Summary implementation is not currently justified.
Existing rationale surfaces are sufficient for current concrete questions.
```

### Response facts

```text
Response answers how selected knowledge is communicated.
Response is communication, not knowledge creation.
Response is broader than Explainability.
Response implementation is not justified by current evidence.
```

### Boundary facts

```text
Acquisition creates knowledge.
Integrity characterizes knowledge.
Selection chooses knowledge.
Response communicates knowledge.
```

### Rejected concept facts

```text
IntegrityEngine is rejected.
SelectionEngine is rejected.
ContextEngine is rejected.
Selection Rationale Summary implementation is rejected.
ResponseEngine is rejected.
Universal formatter is rejected.
Runtime-owned response subsystem is rejected.
ToolExecutor response semantics are rejected.
Parallel response system is rejected.
```

## Evidence Requirements

Every extracted documentation fact should retain evidence metadata.

Required evidence metadata:

* source path
* source heading when available
* source line range when available
* extraction kind
* original text span or normalized snippet

Recommended extraction kinds:

* `heading`
* `bullet`
* `numbered_list`
* `table_row`
* `fenced_text_diagram`
* `mermaid_diagram`
* `explicit_boundary_phrase`

## Projection Requirements

Projected documentation facts should be distinguishable from host, provider, runtime, and code-observation facts.

A future projection should preserve at least:

* claim family
* subject
* predicate
* object or value
* source document
* evidence reference
* extraction kind
* confidence or support strength

Documentation facts should not overwrite implementation facts.

Documentation facts should not prove runtime behavior.

Documentation facts should be available to explanation surfaces so Seed can answer why it believes a repository claims something.

## Example Query Behavior

If asked:

```text
What is Seed?
```

Documentation Observation v0 should be able to answer from projected documentation facts:

```text
Seed is documented as a knowledge-oriented runtime that transforms observations into evidence-backed projected knowledge and uses that knowledge to support decisions, recommendations, explanations, capability resolution, and operator understanding.
```

If asked:

```text
Is Seed a workflow engine?
```

It should answer:

```text
No. The README explicitly documents that Seed is not a workflow engine.
```

If asked:

```text
What is the active frontier?
```

It should answer:

```text
Knowledge Acquisition is documented as the active capability frontier, with Users, Groups, Package, and Systemd observations listed as current capability-growth priorities.
```

If asked:

```text
Does the code actually match that?
```

It should refuse to answer from Documentation Observation alone:

```text
Documentation Observation can answer what the docs claim. Repository Observation is required before comparing those claims to code.
```

## Non-Goals

Documentation Observation v0 is not:

* repository observation
* repository reconciliation
* code analysis
* static analysis
* semantic code search
* documentation linting
* documentation generation
* roadmap execution
* implementation planning
* engine creation
* runtime behavior

## Completion Criteria

Documentation Observation v0 is characterized when the repository has a bounded fact list for:

* source allowlist;
* extraction structures;
* fact families;
* expected facts from each source document;
* evidence requirements;
* projection requirements;
* query behavior;
* non-goals.

This document provides that characterization.

## Recommended Next Step

The next step after this characterization is an implementation design document for the smallest possible read-only documentation observation slice.

That design should specify:

* where the observation source would live;
* which existing observation/event types it can reuse;
* whether new predicates are required;
* how evidence spans are represented;
* how markdown structures are parsed without broad summarization;
* which tests would be documentation-observation characterization tests;
* why Runtime, ToolExecutor, EventLedger ownership, and ProjectionStore ownership remain unchanged.
