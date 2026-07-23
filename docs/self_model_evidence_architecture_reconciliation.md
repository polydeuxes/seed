# Self Model Evidence Architecture Reconciliation

## 1. Purpose

This document summarizes Seed's current self-model evidence architecture in one place.

It answers a single synthesis question:

```text
How does Seed know something?
```

This is a capstone synthesis of already-established findings. Authority remains with the underlying reconciliation, vocabulary, inventory, status, and preservation documents. This document does not replace those documents, change their scope, redefine their concepts, or create new evidence classes.

Use this document as a navigation and synthesis layer only:

- for self-model and alignment authority, use `docs/self_model_and_alignment_architecture_reconciliation.md`;
- for documentation-observation authority, use the existing documentation-observation design and characterization documents;
- for repository-observation authority, use `docs/repository_observation_language_boundary.md` and `docs/repository_artifact_ontology_reconciliation.md`;
- for claim-layer authority, use the existence, structure, behavior, boundary, and ownership reconciliation documents;
- for relationship and constraint-evidence findings, use `docs/relationship_fact_reconciliation.md` and `docs/constraint_evidence_inventory.md`;
- for currentness, frontier ownership, and preserved negative findings, use `docs/architectural_knowledge_map.md`, `docs/architectural_status_and_next_frontier.md`, and `docs/architectural_findings_preservation.md`.

## 2. Central Finding

Seed is converging on an evidence-based self-model architecture.

The central finding is:

```text
Claims are not supported directly from documentation.
Claims are not supported directly from repository structure.
Claims are supported by evidence appropriate to the claim type.
```

Documentation can state a claim. Repository observation can supply artifact facts. Reconciliation compares claims and evidence under explicit rules and produces alignment results. The self model is derived from those claims, facts, support relationships, and alignment records; it is not a parallel truth engine, implementation planner, or LLM interpretation layer.

In compact form:

```text
Documentation
        ↓
DocumentationClaim

Repository
        ↓
RepositoryArtifactFact

DocumentationClaim + appropriate evidence
        ↓
Reconciliation
        ↓
AlignmentRecord
        ↓
Self Model
```

The important architectural distinction is that different claims need different evidence. A class fact can support a narrow existence claim. It cannot, by itself, support behavior, boundary, or ownership. A relationship can support behavior, but it cannot by itself prove boundary or ownership. A constraint can help support boundary or ownership, but it is not automatically ownership authority.

## 3. Current Acquisition Surfaces

### Input Inspection

Input Inspection is the user-intake and decision-routing surface. It records user text, composes decision context, obtains or derives a decision, validates the decision, applies guardrails, and routes through the existing runtime decision path.

Its responsibility in this synthesis is narrow: it explains how user input becomes inspected and routed before any future self-model evidence work might classify user utterances as questions, commands, observations, documentation claims, corrections, or other input acts.

Input Inspection does not itself prove repository claims, bypass validation, execute tools directly, or turn user language into self-model truth. Its authority remains in `docs/input_inspection_reconciliation.md` and remains bounded by existing implementation evidence.

### Documentation Observation

Documentation Observation is the acquisition surface for what repository documentation says.

Its responsibility is to acquire documentation-backed claims. It asks:

```text
What does the repository say?
```

It does not ask whether the documentation is correct, whether code matches the documentation, which claim wins, or what should be implemented. In the current self-model architecture, its key implemented evidence-facing output is `DocumentationClaim`.

Documentation Observation must remain an acquisition concern. It should not become a documentation engine, architecture engine, projection store, response layer, runtime path, or LLM truth interpreter. Authority remains with the documentation-observation design and characterization documents and the self-model/alignment reconciliation.

### Repository Observation

Repository Observation is the acquisition surface for observed repository artifacts.

Its responsibility is to acquire repository artifact facts. It asks:

```text
What repository artifacts exist?
```

It does not decide what those artifacts mean architecturally, whether they match documentation, whether they are correct, or who owns a concern. In the current self-model architecture, its key implemented evidence-facing output is `RepositoryArtifactFact`.

Repository Observation should preserve the `RepositoryArtifactFact` boundary for downstream reconciliation. Current artifact labels are acceptable adapter vocabulary, but they should not be treated as a complete normalized language-neutral ontology. Authority remains with `docs/repository_observation_language_boundary.md` and `docs/repository_artifact_ontology_reconciliation.md`.

## 4. Current Evidence Types

### Implemented evidence and reconciliation records

Current implemented self-model evidence records are:

| Record | Current role |
| --- | --- |
| `DocumentationClaim` | A documentation-backed statement capable of receiving support. |
| `RepositoryArtifactFact` | A structural fact observed from repository artifacts. |
| `AlignmentRecord` | The deterministic comparison result between a claim and supplied evidence under reconciliation rules. |

`DocumentationClaim` and `RepositoryArtifactFact` are acquisition-side records. `AlignmentRecord` is a reconciliation result, not raw evidence. Together they form the currently implemented spine for documentation/repository self-model alignment.

### Conceptual evidence findings

Prior reconciliations also established conceptual future evidence needs. These are findings only, not new implemented classes in this document:

| Conceptual finding | Established need |
| --- | --- |
| `RelationshipFact` | Behavior-oriented evidence should model observed relationships, flows, calls, routes, emissions, mutations, storage, validation, and execution paths rather than artifact existence alone. |
| `ConstraintFact` | Boundary-oriented evidence likely needs scoped constraints: required, prohibited, exclusive, guarded, or separated paths. |
| `InvariantFact` | Some invariant material may be evidence source material if scoped and normalized by a future approved design. |
| `PolicyFact` | Policy-like material exists across documentation, validation, execution policy, guards, and tests, but it is not yet a first-class acquisition output. |

This document does not recommend implementing these concepts. It only preserves that they are already-established architectural findings elsewhere.

## 5. Evidence Ladder

Seed's current self-model evidence ladder is:

```text
Existence
        ↓
Structure
        ↓
Behavior
        ↓
Boundary
        ↓
Ownership
```

Each layer asks a different question and requires different evidence.

### Existence

An existence claim asserts that a named repository artifact exists or that a named artifact defines another named artifact in the narrow existence sense.

Typical current evidence:

- `RepositoryArtifactFact` records whose symbols, kinds, paths, or directly equivalent matching rules identify the named artifact;
- for the narrow `X defines Y.` rule, supplied artifact facts for both names in the same source path.

Existence evidence does not prove structure beyond its narrow rule, runtime behavior, boundary, or ownership. Authority: `docs/existence_claim_reconciliation.md`.

### Structure

A structure claim asserts that artifacts are arranged or related in a specific static repository shape.

Typical evidence discussed in prior reconciliation:

- artifact facts with structural metadata, such as method containment or parent-symbol information;
- static relationships such as definition, containment, import, implementation, or association where supported by supplied repository observation evidence.

Structure begins where same-path existence stops. It can show static arrangement, but it does not prove runtime behavior or architectural ownership. Authority: `docs/structure_claim_reconciliation.md` and `docs/repository_artifact_ontology_reconciliation.md`.

### Behavior

A behavior claim asserts that a component participates in a runtime-relevant action, flow, state transition, routing path, validation step, recording step, emitted effect, storage operation, or operation execution.

Evidence discussed in prior reconciliation:

- relationship-oriented evidence such as call sites, route branches, state mutation, event appends, handler registration, integration paths, storage calls, validation paths, or execution paths;
- the conceptual `RelationshipFact` primitive, if future acquisition is approved.

Behavior must not be inferred from names, same-path evidence, method existence, imports, documentation prose alone, containment, or LLM semantic reasoning. Authority: `docs/behavior_claim_reconciliation.md` and `docs/relationship_fact_reconciliation.md`.

### Boundary

A boundary claim asserts that a responsibility, capability, workflow, state transition, policy, or architectural concern is intentionally constrained to, required through, prohibited from, or separated by a component or set of components.

Evidence discussed in prior reconciliation:

- relationship evidence showing the observed path or participation;
- constraint-oriented evidence showing what is allowed, required, prohibited, exclusive, guarded, or intentionally separated;
- invariants, policy rules, validation rules, tests, architecture metadata, non-goals, or rejected alternatives when scoped and explicit.

Relationship evidence alone usually supports behavior, not boundary. Boundary support likely needs relationship evidence plus constraint evidence under explicit scope. Authority: `docs/boundary_claim_reconciliation.md`, `docs/relationship_fact_reconciliation.md`, and `docs/constraint_evidence_inventory.md`.

### Ownership

An ownership claim asserts that a component is the authoritative architectural responsibility holder for a scoped concern.

Evidence discussed in prior reconciliation:

- artifact evidence identifying candidate owners;
- relationship evidence showing participation or delegation;
- boundary, constraint, invariant, or policy evidence showing required routes, prohibited bypasses, allowed responsibilities, or preserved invariants;
- explicit scope;
- competing-owner analysis and absence or subordination of alternatives under that scope.

Ownership is the highest current evidence layer. It must not be inferred from lower-layer evidence by default. Behavior can show participation. Boundary can show constraint. Neither automatically proves ownership authority. Authority: `docs/ownership_claim_reconciliation.md`.

## 6. Evidence Flow

High-level flow:

```text
User Input
        ↓
Input Inspection
        ↓
Observation
        ↓
Evidence
        ↓
Reconciliation
        ↓
Alignment Result
```

Briefly:

1. **User Input** is text supplied by the operator. Input-act vocabulary can describe what kind of utterance it is, but user language does not become truth by itself.
2. **Input Inspection** records, contextualizes, validates, guards, and routes user input through existing runtime decision surfaces.
3. **Observation** acquires source-specific material. Documentation Observation reads documentation claims; Repository Observation reads repository artifacts.
4. **Evidence** preserves acquisition outputs appropriate to the source and claim type, such as `DocumentationClaim` and `RepositoryArtifactFact` today, with relationship and constraint-family concepts identified as future findings.
5. **Reconciliation** applies explicit claim-family rules. It compares claims with evidence suitable to the claim layer.
6. **Alignment Result** records the outcome, currently through `AlignmentRecord` outcomes such as `supported`, `missing_support`, `potential_conflict`, or `not_evaluable`.

The flow is deliberately conservative. It prevents documentation prose, repository shape, or LLM interpretation from directly becoming architectural knowledge without evidence and reconciliation.

## 7. Implemented vs Conceptual

### Implemented today

Implemented today:

- `DocumentationClaim` acquisition from documentation observation;
- `RepositoryArtifactFact` acquisition from repository observation;
- `AlignmentRecord` reconciliation output;
- explicit fixture-scale reconciliation for supported lower-layer claim families already covered by implementation and tests;
- input inspection, validation, guard, and routing surfaces for user messages.

These implemented surfaces are the current evidence spine.

### Architectural findings not yet implemented

Architectural findings not yet implemented as first-class acquisition outputs include:

- `RelationshipFact`;
- `ConstraintFact`;
- `InvariantFact`;
- `PolicyFact`;
- owner-candidate or competing-owner analysis records.

These findings are important because they explain why lower-layer evidence is insufficient for higher-layer claims. They are not implementation requirements in this document, and this document does not recommend adding them.

## 8. Architectural Guardrails

The current architecture is protected by the following guardrails:

- Do not infer ownership from behavior. Behavior shows participation, not authority.
- Do not infer behavior from containment. Containment shows static structure, not runtime participation.
- Do not infer architecture from existence. A named artifact being present does not prove structure, behavior, boundary, or ownership.
- Do not infer boundary from relationship alone. A relationship can show what happens; it does not by itself show what is required, prohibited, exclusive, or guarded.
- Do not bypass validation. User input and model decisions must remain subject to validation, guard, policy, and routing boundaries.
- Do not replace evidence with LLM interpretation. LLM language can help produce or route decisions only within the validated path; it is not a substitute for acquired evidence and explicit reconciliation.
- Do not create parallel truth systems. The self model is derived from claims, evidence, support, and alignment, not from an independent authority layer.
- Do not default to new engines, universal stores, Runtime integration, or ToolExecutor integration when existing surfaces already own the concern.

Authority for these guardrails lives across the claim reconciliations, relationship and constraint evidence documents, input-inspection documents, and architectural findings preservation documents.

## 9. Current Frontier

Current frontier ownership remains with `docs/architectural_status_and_next_frontier.md`.

At a high level, the active frontier is bounded Knowledge Acquisition expansion rather than recursive architecture invention. Documentation maintenance remains valuable where it preserves authority boundaries, currentness, and navigation. Future investigations should begin only when a concrete operator question is important, recurring, and not answered by existing documents or surfaces.

This document does not duplicate frontier ownership, reorder priorities, or create implementation backlog.

## 10. Direct Answers

### How does Seed know something?

Seed knows something by acquiring evidence from bounded observation surfaces, preserving that evidence in typed records, and reconciling claims against evidence appropriate to the claim type under explicit rules.

Documentation tells Seed what is claimed. Repository observation tells Seed what artifacts are observed. Reconciliation determines whether the supplied evidence supports, lacks support for, conflicts with, or cannot evaluate the claim. The self model is derived from that reconciled relationship.

### What evidence exists today?

Evidence and records implemented today include:

- `DocumentationClaim` for documentation-backed claims;
- `RepositoryArtifactFact` for observed repository artifacts;
- `AlignmentRecord` for reconciliation outcomes comparing claims and supplied evidence.

### What evidence is conceptual?

Conceptual evidence findings include:

- `RelationshipFact` for behavior-oriented relationships and flows;
- `ConstraintFact` for scoped required, prohibited, exclusive, guarded, or separated paths;
- `InvariantFact` for scoped invariant evidence if future normalization is approved;
- `PolicyFact` for policy-like source material if future normalization is approved;
- competing-owner analysis concepts for ownership support.

These are not implemented by this document.

### What remains unresolved?

Unresolved areas remain with their owning documents and future approved work:

- how, whether, and when to implement relationship evidence;
- how, whether, and when to normalize constraint, invariant, or policy evidence;
- how to represent competing-owner analysis if ownership reconciliation is later implemented;
- how to preserve scope metadata across future evidence classes;
- how far Knowledge Acquisition expansion should proceed within the active frontier.

This document does not resolve those questions. It only summarizes where the architecture currently stands.

## 11. Non-Goals

This document does not:

- introduce new architecture;
- define new evidence classes;
- redefine `DocumentationClaim`, `RepositoryArtifactFact`, `AlignmentRecord`, `RelationshipFact`, `ConstraintFact`, `InvariantFact`, or `PolicyFact`;
- define ownership;
- define behavior;
- define boundary semantics;
- replace any authority document;
- modify production code;
- modify tests;
- create implementation requirements;
- recommend an implementation sequence;
- assign current frontier ownership;
- create a new audit chain;
- treat documentation, repository shape, or LLM interpretation as self-proving truth.

## Authority References Introduced

This synthesis references the following authority documents without replacing them:

- `docs/input_inspection_reconciliation.md`
- `docs/self_model_and_alignment_architecture_reconciliation.md`
- `docs/documentation_observation_design.md`
- `docs/documentation_observation_v0_implementation_characterization.md`
- `docs/repository_observation_language_boundary.md`
- `docs/repository_artifact_ontology_reconciliation.md`
- `docs/existence_claim_reconciliation.md`
- `docs/structure_claim_reconciliation.md`
- `docs/behavior_claim_reconciliation.md`
- `docs/boundary_claim_reconciliation.md`
- `docs/ownership_claim_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/constraint_evidence_inventory.md`
- `docs/architectural_knowledge_map.md`
- `docs/architectural_status_and_next_frontier.md`
- `docs/architectural_findings_preservation.md`
