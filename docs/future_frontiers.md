# Future Frontier Bounty Board

Purpose

This document is not a roadmap.

This document is not roadmap authority.

This document is not a commitment.

This document preserves candidate architectural frontiers that emerged from
investigations but have not yet been reconciled.

Items may be:

* explored;
* superseded;
* merged;
* rejected;
* resolved.

Presence on this list does not imply priority, sequencing, implementation readiness, or canonical ontology.

---

## High Signal Frontiers

### Inquiry Ontology Frontier

Status:

Characterized.

Questions:

* Does the repository contain Inquiry Objects?
* Is inquiry distinct from knowledge?
* Does inquiry have lineage?
* Can inquiries branch, merge, pause, or resume?

Related:

* inquiry_frontier.md
* handoff_and_continuation_lineage_frontier.md

---

### Operations Ontology Frontier

Status:

Characterized.

Questions:

* What are the primitive operations?
* Are operations distinct from objects?
* Is derivation primitive or composite?
* Are revision and reconciliation operations or outcomes?

Related:

* operations_frontier.md
* derivation_frontier.md

---

### Operation Composition Frontier

Status:

Emerging.

Questions:

* Can primitive operations compose into larger investigation or knowledge-change operations?
* Where is the boundary between operation, process, workflow, and runtime execution?
* How should composed operations preserve provenance, attribution, scope, and explanation?

Related:

* operations_frontier.md
* operation_attribution_frontier.md
* derivation_frontier.md
* handoff_and_continuation_lineage_frontier.md

---

### Knowledge Lineage / Provenance Frontier

Status:

Emerging.

Questions:

* How does represented knowledge arise?
* What lineage or provenance information is required for explainability?
* How much lineage and provenance must be preserved?

Related:

* operation_attribution_frontier.md
* derivation_frontier.md
* handoff_and_continuation_lineage_frontier.md

---

### Investigation Lineage Frontier

Status:

Emerging.

Questions:

* How do inquiries evolve?
* What survives successful handoffs?
* What is preserved across continuation?

Related:

* handoff_and_continuation_lineage_frontier.md
* inquiry_frontier.md

---

### Selection Lineage Frontier

Status:

Emerging.

Observed repeatedly but not yet characterized.

Questions:

* Why was a path selected?
* Why was a frontier prioritized?
* Why did continuation focus on one tension over another?
* Can selection rationale be preserved?

Observed in:

* working state
* handoff activation
* continuation
* inquiry characterization

---

## Federation Frontiers

### Cross-Seed Challenge And Reevaluation Frontier

Status:

Uncharacterized.

Questions:

* How can one Seed challenge another Seed's conclusion?
* How can support expansion trigger reevaluation?
* How can disagreement occur without authority transfer?

---

### Federated Knowledge Placement Frontier

Status:

Uncharacterized.

Questions:

* What belongs in a local Seed?
* What belongs in a federated Seed?
* What can be imported on demand?

---

### Federated Inquiry Frontier

Status:

Speculative.

Questions:

* Can inquiries be exchanged?
* Can one Seed inherit another Seed's frontier?
* Can investigation lineage cross Seed boundaries?

---

## Knowledge Burden Frontiers

### Knowledge Placement And Burden Frontier

Status:

Uncharacterized.

Questions:

* What belongs in runtime?
* What belongs in Git?
* What belongs in documentation?
* What should be re-derived instead of stored?

Motivation:

Preserve lightweight Seed deployments.

---

### Derivability Frontier

Status:

Speculative.

Questions:

* What should be stored?
* What should be reconstructed?
* What should be imported?
* What should be forgotten?

---

## Agency And Authority Frontiers

### Authority Versus Attribution Frontier

Status:

Emerging.

Questions:

* Who performed an operation?
* Who approved it?
* Who owns it?
* Who is accountable?

Related:

* operation_attribution_frontier.md

---

### Knowledge Adoption Frontier

Status:

Speculative.

Questions:

* When does a recommendation become adopted?
* When does adopted knowledge become policy?
* How does operator authority interact with learning?

---

## Meta Frontiers

### Frontier Ontology Frontier

Status:

Speculative.

Questions:

* What is a frontier?
* How does a frontier differ from a gap?
* How does a frontier become a reconciliation?

---

### Architectural Discovery Frontier

Status:

Speculative.

Questions:

* Is the repository accumulating discoveries in addition to knowledge?
* Can discovery itself be represented?
* What distinguishes a finding from a claim?

---

### Role Lineage Frontier

Question:

Can roles persist?

Examples:

active
selected
attention target
inquiry target
working-state content

Interesting tension:

Objects persist.

Roles change.

But do role histories matter?
Operation Lineage Frontier

Question:

Does an inquiry persist?

Or only its artifacts?

Examples:

Inquiry
Selection
Attention
Revision

Could be huge for continuation.

---

### Relationship Lineage Frontier

Question:

Can relationships evolve?

Example:

Claim A supports Claim B

later

Claim A weakly supports Claim B

later

Claim A contradicts Claim B

What persisted?

Investigation Cluster
Continuity Frontier

Neighbor to persistence.

Question:

How do we recognize sameness over time?

Different from identity.

Different from persistence.

Could become foundational.

---

### State Frontier

Question:

What is state?

Seed uses:

state
working state
knowledge state
repository state
investigation state

We've never actually reconciled state.

Context Frontier

Question:

What is context?

We've discussed:

active context
working state
selection rationale
handoff context

but never attacked context directly.

## Wildcard Frontiers

### Constraint Frontier

Question:

What constrains operations?

Candidates:

authority
policy
trust
scope
capability

Could explain a lot of execution behavior.

---

### Boundary Frontier

Question:

What is a boundary?

The word appears everywhere:

authority boundary
observation boundary
provider boundary
execution boundary
identity boundary

Yet we have never treated it as a first-class investigation.

### Relationship vs Role Pressure Test

This one may become necessary after Relationship Frontier.

Question:

When does a connection become a role?

When does a role become a connection?

Examples:

supports
evidence-for
attention-target
selected
depends_on
Dark Horse Candidate

### Grammar Frontier

Question:

What are the primitive kinds of things
in Seed's ontology?

Current pressure-generated candidates:

Object
Relationship
Role
Operation

Potential outcome:

Not all represented things are objects.

## Notes

A frontier appearing on this board means:

```text
Interesting enough to revisit.
```

It does not mean:

```text
Ready for implementation.
```
