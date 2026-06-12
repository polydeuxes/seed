# Knowledge Navigation Layers Frontier

## Purpose

This document captures an architectural frontier discovered during documentation navigation, repository observation, relationship observation, and self-model work.

It is a frontier characterization.

It is not a reconciliation.

It does not define implementation.

It captures a newly observed architectural shape: Seed appears to be developing multiple navigation graphs at once, and navigation itself may be an architectural concern.

---

## Central Finding

Seed appears to be developing multiple navigation graphs simultaneously.

These graphs are related but not identical.

The emerging architectural finding is that navigation is not only a usability concern. It may become part of how Seed explains itself, maintains itself, and continues learning.

---

# Layer 1: Structural Navigation

Structural navigation answers:

```text
What is connected to what?
```

Examples:

```text
imports
calls
depends_on
contains
references
emits
consumes
```

Repository relationship observation, AST analysis, import observation, and relationship facts primarily operate at this layer.

Example:

```text
seed_local.py
    imports
observation_sources.py

observation_sources.py
    emits
Observation
```

This layer describes repository topology.

It is concerned with concrete implementation structures and observable code relationships.

---

# Layer 2: Architectural Navigation

Architectural navigation answers:

```text
What concept governs this behavior?
```

Examples:

```text
Observation
Evidence
Fact
Projection
Authority
Capability
Identity
```

Most reconciliation documents operate at this layer.

Example:

```text
Prometheus Observation
        ↓
Prometheus Observation Boundary
        ↓
Observation Interpretation
        ↓
Foundational Ontology
```

This layer describes architectural topology.

It is concerned with concepts, boundaries, authority, and the reasoning that governs implementation choices.

---

# Layer 3: Knowledge Navigation

Knowledge navigation answers:

```text
I have a question.

Where should I look?
```

Examples:

```text
Temporal reasoning
        ↓
Temporal documents

Host Observation
        ↓
Host Observation documents

Federation
        ↓
Federation documents
```

The documentation map and architectural knowledge map have begun operating at this layer.

This layer describes conceptual navigation.

It is concerned with helping operators and contributors move from a question to the documents, concepts, architecture, or implementation artifacts that can answer it.

---

# Emerging Observation

These layers appear independent.

However, they also appear connectable.

One possible navigation path is:

```text
Question
        ↓
Concept
        ↓
Architecture
        ↓
Implementation
```

which may expand into:

```text
Question
        ↓
Knowledge Graph
        ↓
Architectural Graph
        ↓
Repository Graph
        ↓
Implementation Artifact
```

This document does not decide whether those layers should be unified.

It only records that the same repository now contains evidence of multiple navigation structures that could be traversed together.

---

# Documentation Observation Implication

A reconciliation document is not merely a file.

It contains:

```text
concepts
definitions
claims
relationships
references
dependencies
```

This suggests documentation itself may eventually become observable.

Example:

```text
Host Observation
        references
Prometheus

Host Observation
        references
SSH

Host Observation
        related_to
Observation Interpretation
```

This is not repository topology.

It is knowledge topology.

The implication is that documentation observation may need to preserve the difference between:

- file-level structure;
- concept-level references;
- architectural dependency;
- navigation usefulness;
- authority or boundary ownership.

---

# Self-Model Implication

A future Seed self-model may need to understand more than source-code structure.

It may need to distinguish:

```text
Repository Structure
Architectural Structure
Knowledge Structure
```

Repository structure can explain where implementation artifacts live.

Architectural structure can explain which concepts and boundaries govern those artifacts.

Knowledge structure can explain where a contributor or operator should look when they have a question.

These structures may overlap, but they are not currently the same thing.

---

# Open Question

Are these:

```text
repository graph
architecture graph
knowledge graph
```

three independent graphs,

or three projections of a larger graph?

The answer is currently unknown.

This document does not reconcile that question.

---

# Frontier

The emerging frontier is not merely repository observation.

The emerging frontier is navigation itself.

Seed may eventually need to understand:

```text
where knowledge lives
how concepts connect
how architecture connects
how implementation connects
how operators navigate between them
```

in order to explain itself, maintain itself, and continue learning.

This frontier touches repository observation, documentation observation, relationship observation, architectural reconciliation, and self-model work without collapsing them into a single implementation plan.

---

# Final Finding

Relationship observation, documentation observation, architectural reconciliation, and the documentation index appear to be converging toward a broader concept:

```text
Knowledge Navigation
```

The repository is no longer only accumulating facts about systems.

It is beginning to accumulate knowledge about how knowledge itself is organized and discovered.
