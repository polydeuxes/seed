# Documentation Observation Seed Characterization

## Purpose

This document characterizes what Documentation Observation would extract from Seed's own canonical documentation if implemented.

It is the first Seed-specific characterization of Documentation Observation.

It answers:

```text
What claims exist in Seed's documentation today?
```

This is documentation-only.

It does not implement extraction, repository observation, repository reconciliation, claim support projection, runtime behavior, or tests.

## Scope

Documentation Observation for Seed should initially inspect only canonical front-door architecture documents.

Initial source allowlist:

```text
README.md
docs/README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
docs/architectural_findings_preservation.md
docs/reasoning_roadmap.md
```

These documents are enough to characterize the first extraction surface because they contain:

* repository identity claims;
* process-layer claims;
* representation-layer claims;
* ownership and boundary claims;
* status and frontier claims;
* rejected concept claims;
* reading-order and canonical-document claims.

Do not scan all docs recursively in v0.

## Extraction Principle

Documentation Observation should extract claims only when they are capable of receiving support.

A sentence is not automatically a claim.

A useful v0 documentation claim should be:

* explicit;
* bounded;
* attributable to a source document;
* capable of later support, partial support, conflict, or non-evaluation;
* useful for operator or architecture navigation.

## Claims To Extract

### Repository Identity Claims

Expected claims:

```text
Seed is a knowledge-oriented runtime.
Seed transforms observations into evidence-backed projected knowledge.
Seed uses projected knowledge to support decisions, recommendations, explanations, capability resolution, and operator understanding.
Seed is knowledge-first rather than execution-first.
```

Likely sources:

```text
README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
```

Reconciliation hook:

```text
Mostly not evaluable by Repository Observation v0.
Some structural support may exist through presence of observation, evidence, projection, explanation, and capability-resolution modules.
```

### Process-Layer Claims

Expected claims:

```text
Knowledge Acquisition precedes Knowledge Integrity.
Knowledge Integrity precedes Knowledge Selection.
Knowledge Selection precedes Response.
Acquisition creates knowledge.
Integrity characterizes knowledge.
Selection chooses knowledge.
Response communicates knowledge.
```

Likely sources:

```text
README.md
docs/README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
```

Reconciliation hook:

```text
Partially evaluable by documentation-only observation.
Repository Observation v0 may identify modules and docs named around these concerns but should not infer lifecycle ownership.
```

### Representation-Layer Claims

Expected claims:

```text
Observations lead to evidence.
Evidence supports facts.
Facts project into current knowledge structures.
Projected knowledge structures include relationships, entity types, contradictions, state views, and explanations.
Facts support claims through support relationships.
FactSupport and Claim Support are distinct concepts.
Claim Support is deterministic and inspectable.
Claim Support is not a reasoning engine, inference engine, truth system, or architecture engine.
```

Likely sources:

```text
README.md
docs/knowledge_representation_map.md
docs/knowledge_representation_reconciliation.md
docs/claim_support_frontier.md
docs/claim_support_characterization.md
docs/claim_support_design.md
docs/architectural_knowledge_map.md
```

Note:

```text
The first v0 allowlist may not include every representation document.
If representation extraction is the target, expand the allowlist explicitly rather than scanning all docs.
```

Reconciliation hook:

```text
Repository Observation can later inspect whether FactSupport structures exist.
Claim Support implementation is not expected yet unless future work adds it.
```

### Ownership Claims

Expected claims:

```text
EventLedger owns append-only events and audit history.
ProjectionStore owns cached projected state.
ToolExecutor owns registered-operation execution.
CapabilityCatalog owns non-executable provider and handoff recommendations.
PredicateCatalog defines canonical predicate vocabulary.
RelationshipCatalog defines topology semantics.
EntityTypeCatalog defines entity classification vocabulary.
InferenceCatalog defines deterministic inference rules.
```

Likely sources:

```text
README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
docs/reasoning_roadmap.md
```

Reconciliation hook:

```text
Repository Observation can look for matching classes, modules, imports, tests, catalog files, and CLI references.
```

### Boundary Claims

Expected claims:

```text
Capability resolution does not imply execution.
Capability resolution does not imply verification.
Provider recommendations do not imply availability.
Local configuration does not imply reachability.
Integrity does not determine truth.
Response does not create knowledge.
Documentation Observation observes documentation claims, not implementation truth.
Repository Observation observes artifacts, not architecture meaning.
Repository Reconciliation compares claims and artifacts, but does not arbitrate truth.
```

Likely sources:

```text
README.md
docs/architectural_knowledge_map.md
docs/documentation_observation_frontier.md
docs/repository_observation_frontier.md
docs/repository_reconciliation_frontier.md
docs/claim_support_design.md
```

Reconciliation hook:

```text
Some boundary claims may be evaluable by absence or presence of specific rejected classes or execution paths.
Most remain requires_human_review unless repository artifact evidence is explicit.
```

### Status Claims

Expected claims:

```text
Knowledge Acquisition is the active capability frontier.
Knowledge Integrity is stable.
Knowledge Selection is stable.
Response is stable or complete enough.
Architectural Findings are partially reconciled.
Response Caveats are complete enough and paused.
Knowledge Representation is emerging and reconciled.
```

Likely sources:

```text
README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
docs/README.md
```

Reconciliation hook:

```text
Status claims are documentation-grounded.
Repository Observation may support implemented/absent slices, but should not determine architectural status by itself.
```

### Frontier Claims

Expected claims:

```text
Users Observation is a current capability-growth priority.
Groups Observation is a current capability-growth priority.
Package Observation is a current capability-growth priority.
Systemd Observation is a current capability-growth priority.
Documentation Observation is an emerging acquisition frontier.
Repository Observation is an emerging acquisition frontier.
Repository Reconciliation is an emerging comparison frontier.
Claim Support projection semantics remain an open frontier.
```

Likely sources:

```text
README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
docs/README.md
```

Reconciliation hook:

```text
Frontier claims may be supported by absence of implementation when the claim explicitly describes future or active work.
This requires claim-family-aware support rules.
```

### Rejected Concept Claims

Expected claims:

```text
ReasoningEngine is rejected.
InferenceEngine as claim support is rejected.
TruthEngine is rejected.
IntegrityEngine is rejected.
SelectionEngine is rejected.
ResponseEngine is rejected.
CaveatEngine is rejected.
ContextEngine is rejected.
Planner is rejected.
WorkflowEngine is rejected.
ClaimStore is rejected.
SupportStore is rejected.
Automatic claim-to-claim reasoning chains are rejected.
Runtime integration as a default solution is rejected.
ToolExecutor integration as a default solution is rejected.
```

Likely sources:

```text
docs/architectural_knowledge_map.md
docs/architectural_findings_preservation.md
docs/claim_support_design.md
docs/reasoning_roadmap.md
```

Reconciliation hook:

```text
Repository Observation can later check whether rejected concept symbols or files exist.
Absence of rejected symbols may support rejection claims.
Presence of rejected symbols may produce potential_conflict.
```

### Reading-Order Claims

Expected claims:

```text
docs/architectural_knowledge_map.md is recommended early for new readers.
docs/README.md is recommended early for new readers.
docs/knowledge_representation_map.md is recommended for representation architecture.
docs/knowledge_representation_reconciliation.md is recommended for representation reconciliation.
docs/architectural_status_and_next_frontier.md is recommended for current frontier status.
docs/reasoning_roadmap.md is recommended for roadmap context.
```

Likely sources:

```text
README.md
docs/README.md
docs/architectural_knowledge_map.md
```

Reconciliation hook:

```text
Mostly not evaluable by Repository Observation beyond file existence.
```

## Claims Not To Extract

Documentation Observation v0 should not extract claims from:

* narrative examples;
* historical commentary;
* assistant/user phrasing preserved in docs;
* speculative future possibilities;
* code snippets unless explicitly describing architecture;
* CLI usage examples unless the claim is about CLI surface existence;
* broad philosophical statements that cannot receive support.

Examples that should usually not become claims:

```text
Seed should feel less like this.
The model does not get unrestricted power.
This is where things get interesting.
```

These may be useful prose, but they are not good v0 claim facts.

## Example Claim Inventory

### Claim: ProjectionStore owns cached projected state

Family:

```text
ownership claim
```

Expected documentation evidence:

```text
README.md
docs/architectural_knowledge_map.md
```

Expected repository support:

```text
ProjectionStore protocol exists.
InMemoryProjectionStore exists.
SQLiteProjectionStore exists.
State cache CLI references ProjectionStore.
```

Expected reconciliation outcome:

```text
supported or partially_supported depending on observed artifacts
```

### Claim: ToolExecutor owns registered-operation execution

Family:

```text
ownership claim
```

Expected documentation evidence:

```text
README.md
docs/reasoning_roadmap.md
```

Expected repository support:

```text
ToolExecutor class exists.
Runtime imports ToolExecutor.
Runtime calls ToolExecutor.
ToolExecutor tests exist.
```

Expected reconciliation outcome:

```text
supported, partially_supported, or requires_human_review depending on call/use evidence
```

### Claim: ResponseEngine is rejected

Family:

```text
rejection claim
```

Expected documentation evidence:

```text
docs/architectural_knowledge_map.md
docs/response_reconciliation.md
```

Expected repository support:

```text
No ResponseEngine class exists.
No response engine subsystem exists.
```

Expected reconciliation outcome:

```text
supported if rejected symbol is absent
potential_conflict if rejected symbol exists
```

### Claim: Users Observation is a current frontier

Family:

```text
frontier claim
```

Expected documentation evidence:

```text
README.md
docs/architectural_knowledge_map.md
docs/architectural_status_and_next_frontier.md
```

Expected repository support:

```text
No Users Observation implementation exists yet.
No Users Observation tests exist yet.
```

Expected reconciliation outcome:

```text
supported if absence matches future-frontier semantics
```

## Evidence Metadata Requirements

Every extracted claim should retain:

```text
source_path
source_heading
line_range when available
extraction_kind
original_text_span
claim_family
claim_text
```

Recommended extraction kinds:

```text
heading
bullet
numbered_list
table_row
fenced_text_diagram
explicit_boundary_phrase
explicit_rejection_phrase
```

## Output Requirements

A future Documentation Observation implementation should produce documentation-backed claim facts such as:

```text
source document claims X
```

It should not project claim text as implementation truth.

Correct:

```text
README.md claims Seed is a knowledge-oriented runtime.
```

Incorrect:

```text
Seed is proven to be a knowledge-oriented runtime.
```

## Query Expectations

Documentation Observation over Seed should answer:

```text
What does Seed claim to be?
What does Seed claim is the active frontier?
Which concepts are rejected?
Which documents are canonical for representation architecture?
Which claims may later be reconciled against repository artifacts?
```

It should not answer:

```text
Does the code match these claims?
Which claim is true?
Which document should be changed?
What should be implemented next?
```

Those require Repository Observation, Repository Reconciliation, or human judgment.

## Completion Criteria

Seed-specific Documentation Observation is characterized when it has:

* a canonical source allowlist;
* extractable claim families;
* expected claims by family;
* claims not to extract;
* example claim inventory;
* evidence metadata requirements;
* query expectations;
* reconciliation hooks.

This document provides that characterization.

## Recommended Next Step

The next implementation-adjacent step is a tiny fixture or checklist for Documentation Observation v0:

```text
Given README.md and docs/architectural_knowledge_map.md,
extract only explicit repository identity, process-layer, status, frontier, ownership, boundary, and rejection claims
with source path and heading evidence.
```

No repository observation or reconciliation should be added until claim extraction is narrow and deterministic.

## Conclusion

Seed's documentation already contains extractable claims.

Documentation Observation should begin by acquiring those claims as documentation-backed knowledge.

It should not interpret them as implementation truth.

It should preserve them so Repository Observation and Repository Reconciliation can later compare claims against artifacts.
