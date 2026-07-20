# Documentation Observation Design

## Purpose

This document defines the smallest possible implementation design for Documentation Observation v0.

It exists to answer a single architectural question:

```text
How do documentation facts enter
Observation → Evidence → Fact → Projection
without creating a special documentation path?
```

This document intentionally stops before implementation.

It defines integration boundaries, ownership boundaries, and rejection criteria.

## Design Goal

Documentation Observation should behave like any other observation source.

Desired lifecycle:

```text
Documentation File
        ↓
Documentation Observation
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

The design goal is architectural reuse.

Documentation should enter through the same conceptual lifecycle already used elsewhere in Knowledge Acquisition.

## Primary Architectural Constraint

Documentation Observation must not create:

```text
DocumentationEngine
ArchitectureEngine
DocumentationKnowledgeStore
DocumentationProjectionStore
DocumentationFactStore
```

The repository already has:

```text
Observation
Evidence
Fact
Projection
Explanation
```

Documentation Observation should reuse those concepts.

## Ownership

Documentation Observation belongs to:

```text
Knowledge Acquisition
```

It does not belong to:

```text
Knowledge Integrity
Knowledge Selection
Response
Runtime
ToolExecutor
ProjectionStore
```

Documentation Observation acquires documentation-backed knowledge.

Everything after acquisition remains unchanged.

## Proposed Observation Shape

Documentation Observation should produce ordinary observations.

Conceptually:

```text
Observation
  source_type=documentation
  source_path=README.md
  extraction_kind=heading
  subject=Seed
  predicate=is
  object=knowledge-oriented runtime
```

Another example:

```text
Observation
  source_type=documentation
  source_path=docs/architectural_knowledge_map.md
  extraction_kind=fenced_text_diagram
  subject=Knowledge Acquisition
  predicate=precedes
  object=Knowledge Integrity
```

The observation should describe what the document claims.

The observation should not claim implementation truth.

## Evidence Requirements

Every documentation observation should create evidence.

Required evidence metadata:

```text
source_path
source_heading
line_range
extraction_kind
text_span
```

The evidence should be sufficient for explanation surfaces to answer:

```text
Why does Seed believe this documentation claim exists?
```

without reopening the document.

## Fact Semantics

Documentation-derived facts are architectural claims.

They are not implementation facts.

Conceptually:

```text
README claims Seed is a knowledge-oriented runtime.
```

is different from:

```text
Code proves Seed behaves as a knowledge-oriented runtime.
```

Documentation Observation owns only the first claim.

Repository Observation owns the second.

## Predicate Strategy

Documentation Observation should avoid introducing a large documentation-specific vocabulary.

Preferred approach:

Reuse existing relationship and ownership concepts whenever possible.

Examples:

```text
precedes
owns
does_not_own
implements
rejects
has_status
```

New predicates should only be introduced if existing architectural vocabulary cannot express the claim.

## Extraction Strategy

Documentation Observation v0 should favor explicit structure.

Priority order:

```text
1. Headings
2. Numbered lists
3. Bullet lists
4. Tables
5. Fenced text diagrams
6. Mermaid diagrams
7. Explicit boundary phrases
```

V0 should avoid:

```text
Broad summarization
LLM interpretation
Semantic rewriting
Hidden inference
```

The extraction path should remain deterministic.

## Authority Model

Documentation authority should remain visible.

Documentation Observation should not silently decide:

```text
This document is correct.
This document wins.
This document overrides another document.
```

Instead, authority should remain metadata.

Possible metadata:

```text
source path
source class
source status
confidence
```

Future reconciliation work may consume that metadata.

Documentation Observation should not.

## Relationship To Existing Documentation

Documentation Observation v0 should initially be limited to:

```text
README.md
docs/README.md
docs/architectural_knowledge_map.md
```

This intentionally avoids repository-wide scanning.

The purpose is proving the architectural path before expanding scope.

## Query Expectations

A successful implementation should support questions such as:

```text
What does Seed claim to be?
What are Seed's architectural concerns?
What is the active frontier?
What concepts are explicitly rejected?
Which component owns append-only events?
Which component owns cached projected state?
```

without requiring repository observation.

## Interaction With Repository Observation

Documentation Observation answers:

```text
What does the repository say it is?
```

Repository Observation will answer:

```text
What does the repository contain?
```

The two should remain independent.

Neither should silently consume the other.

## Interaction With Repository Reconciliation

Repository Reconciliation is expected to consume:

```text
Documentation facts
Repository facts
```

and compare them.

Documentation Observation should not perform that comparison.

## Runtime Impact

Documentation Observation should not require:

```text
Runtime changes
ToolExecutor changes
Decision changes
Policy changes
ContextComposer changes
```

The observation source should produce knowledge.

Existing systems should consume projected knowledge exactly as they do today.

## ProjectionStore Impact

None.

ProjectionStore ownership remains unchanged.

Documentation Observation should project through existing projection mechanisms rather than introducing a documentation-specific projection layer.

## EventLedger Impact

None.

EventLedger ownership remains unchanged.

Documentation observations should enter through normal observation/event patterns.

## Integrity Impact

None.

Knowledge Integrity may later characterize documentation facts exactly as it characterizes other projected knowledge.

No documentation-specific integrity subsystem should exist.

## Selection Impact

None.

Knowledge Selection may later choose documentation facts when they are relevant.

Documentation Observation does not own selection behavior.

## Response Impact

None.

Response may communicate documentation-derived facts.

Documentation Observation does not own formatting or communication behavior.

## Success Criteria

Documentation Observation v0 succeeds if:

```text
Seed can project documentation-backed concern,
status,
frontier,
ownership,
and rejection facts
```

from the canonical allowlist.

And:

```text
Every projected fact can be traced back to documentation evidence.
```

And:

```text
No special runtime path is introduced.
```

## Failure Criteria

The design fails if implementation requires:

```text
DocumentationEngine
ArchitectureEngine
Runtime modifications
ToolExecutor modifications
ProjectionStore ownership changes
EventLedger ownership changes
LLM-required interpretation
repository-wide semantic analysis
```

## Conclusion

Documentation Observation is not a documentation system.

It is a narrow Knowledge Acquisition slice.

Its responsibility is simple:

```text
Observe documentation.
Create evidence.
Support facts.
Project knowledge.
```

Nothing more.

Once that path exists, Repository Observation can be designed as a separate concern that observes code rather than documentation.
