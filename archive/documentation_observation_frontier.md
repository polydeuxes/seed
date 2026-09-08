# Documentation Observation Frontier

## Purpose

This document defines a documentation-only frontier for treating Seed's own documentation as an observation source.

The goal is not to build a documentation parser, repository analyzer, reasoning engine, planner, or codebase-understanding subsystem.

The goal is to preserve the next architectural insight:

```text
Documentation can be observed as evidence.
Evidence can support projected architectural facts.
Projected architectural facts can help Seed understand its own intended shape.
```

This is a frontier document, not an implementation plan.

## Problem

Seed has accumulated substantial architectural documentation.

That documentation now contains more than prose. It contains:

* concern maps
* lifecycle diagrams
* mermaid hints
* reading orders
* canonical document lists
* rejected concepts
* ownership boundaries
* capability frontiers
* negative findings
* implementation non-goals

A human can read those documents and build a mental image of what Seed is meant to be.

Seed cannot yet observe those documents as evidence-backed architectural knowledge.

Without a documentation observation path, Seed can preserve documentation for humans but cannot project durable architectural facts such as:

```text
Knowledge Acquisition precedes Knowledge Integrity.
ProjectionStore owns cached projected state.
EventLedger owns append-only events.
ToolExecutor owns registered-operation execution.
Response communicates selected knowledge.
Integrity characterizes projected knowledge without selecting truth.
```

That gap matters because repository self-understanding is a prerequisite for later codebase understanding.

## Why Documentation Is An Observation Source

Documentation is not truth by itself.

Documentation is evidence.

It can support claims about intended architecture, known boundaries, rejected concepts, and current frontiers. Those claims should remain evidence-backed, inspectable, and overridable by stronger or more current evidence.

A documentation observation source should follow the existing Seed lifecycle:

```text
Document Content
        ↓
Observation
        ↓
Evidence
        ↓
Fact
        ↓
Projection
        ↓
Explanation
```

The observed subject is not the runtime world. The observed subject is the repository's architectural memory.

## Mermaid Hints As Structured Evidence

Mermaid hints and simple text diagrams are useful because they encode architectural topology in a semi-structured form.

They should not be treated as decorative diagrams first.

They should be treated as possible structured evidence for relationships such as:

```text
A precedes B
A depends_on B
A flows_to B
A owns concern C
A is_boundary_for B
A rejects concept C
```

For example, a lifecycle diagram can support ordered concern facts:

```text
Knowledge Acquisition precedes Knowledge Integrity
Knowledge Integrity precedes Knowledge Selection
Knowledge Selection precedes Response
```

A runtime boundary diagram can support ownership and consumption facts:

```text
Runtime consumes projected state
ToolExecutor owns registered-operation execution
ProjectionStore owns cached projection state
EventLedger owns append-only events
```

These facts are useful only if their evidence remains attached to the source document, heading, code block, and line range when available.

## Architectural Facts Worth Extracting

A future documentation observation slice should start with narrow, high-value architectural facts.

Initial fact types:

* `has_architectural_concern`
* `precedes_concern`
* `owns_boundary`
* `does_not_own_boundary`
* `rejected_concept`
* `canonical_document`
* `current_frontier`
* `implemented_slice`
* `planned_slice`
* `status_classification`

Initial subjects:

* `Seed`
* `Knowledge Acquisition`
* `Knowledge Integrity`
* `Knowledge Selection`
* `Response`
* `Architectural Findings`
* `Runtime`
* `ToolExecutor`
* `EventLedger`
* `ProjectionStore`
* `ContextComposer`
* `ObservationCollectionService`

Initial source documents:

* `README.md`
* `docs/README.md`
* `docs/architectural_knowledge_map.md`
* `docs/architectural_findings_preservation.md`
* `docs/architectural_status_and_next_frontier.md`
* `docs/reasoning_roadmap.md`

## What V0 Should Answer

A documentation observation v0 should help answer narrow operator and developer questions such as:

* What is Seed?
* What are Seed's primary architectural concerns?
* What concern is the active frontier?
* Which concepts have been rejected?
* Which document should I read first?
* Which component owns append-only events?
* Which component owns cached projection state?
* Does capability resolution imply execution?
* Is Response an engine or a distributed communication concern?
* Is Knowledge Integrity allowed to mutate projected truth?

These are documentation-grounded architecture questions.

They do not require runtime execution, provider calls, code parsing, model inference, or repository-wide semantic analysis.

## What V0 Must Not Do

A documentation observation v0 must not create:

* `DocumentationEngine`
* `ArchitectureEngine`
* `CodebaseUnderstandingEngine`
* hidden architectural truth store
* parallel source of truth
* automatic documentation authority resolution
* automatic supersession resolution
* implementation planning
* code generation
* runtime behavior
* provider calls
* ToolExecutor integration
* projection mutation outside normal observation projection

It must not treat documentation as automatically correct.

It must not treat diagrams as proof of implementation.

It must not infer runtime behavior from aspirational roadmap text.

It must not collapse current behavior, intended behavior, rejected behavior, and future behavior into one undifferentiated fact.

## Proposed First Primitive

The first primitive should be a read-only documentation observation slice.

Suggested name:

```text
Documentation Architecture Observation
```

Suggested input:

```text
A small allowlist of repository documentation files.
```

Suggested output:

```text
Observation events with source document, heading, extracted claim, claim kind, and evidence span.
```

Suggested projection result:

```text
Architectural facts with provenance back to the documentation evidence.
```

The primitive should prefer explicit structure over interpretation:

1. headings
2. bullet lists
3. fenced text diagrams
4. mermaid diagrams
5. tables
6. explicit phrases such as `is not`, `does not own`, `rejected`, `current frontier`, and `canonical document`

The primitive should avoid broad natural-language summarization in v0.

## Evidence And Authority

Documentation observation needs authority boundaries.

A fact extracted from `docs/architectural_status_and_next_frontier.md` may be stronger than the same fact extracted from an old audit draft, but that authority should be explicit metadata, not hidden preference.

Potential metadata:

* source path
* source heading
* source line range
* document class
* document status
* extraction kind
* confidence
* created or modified timestamp when available

Authority should remain inspectable through existing explanation surfaces.

## Relationship To Repository Observation

Documentation observation is not the same as code observation.

Documentation observation asks:

```text
What does the repository say it is meant to be?
```

Repository/code observation asks:

```text
What does the repository actually contain?
```

The two become powerful only when compared carefully.

Possible future comparison questions:

* Does code ownership match documented ownership?
* Does an implemented module violate a documented non-goal?
* Does a README claim a capability that code does not expose?
* Does code contain a rejected concept under a different name?
* Does documentation describe a frontier that is already implemented?

Those comparisons are not v0.

They require separate code observation facts and explicit reconciliation semantics.

## Rejection Criteria

Do not implement documentation observation if the work requires:

* Runtime changes
* ToolExecutor changes
* EventLedger ownership changes
* ProjectionStore ownership changes
* provider execution
* shell execution
* model-required interpretation
* broad markdown summarization
* new central architecture engine
* hidden authority rules
* automatic truth arbitration

Do not continue the design unless there is a concrete operator question that existing documentation and existing query surfaces cannot answer.

## Recommended Next Step

Before implementation, add a narrow characterization document or issue defining the exact facts v0 would extract from:

1. `README.md`
2. `docs/README.md`
3. `docs/architectural_knowledge_map.md`

The safest first success criterion is:

```text
Given a small allowlist of canonical docs,
Seed can project evidence-backed architectural concern, ordering, status, and boundary facts
without changing runtime behavior.
```

## Conclusion

Mermaid hints were useful because they exposed a larger pattern: Seed can begin to form a mental image of a codebase by observing structured architectural documentation.

That mental image should not be magical, hidden, or model-only.

It should be evidence-backed projected knowledge.

Documentation observation is therefore a natural future Knowledge Acquisition slice, but it should start narrow, remain read-only, and preserve the existing architecture-first discipline.
