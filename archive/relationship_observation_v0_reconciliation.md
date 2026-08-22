# Relationship Observation v0 Reconciliation

## 1. Purpose

This reconciliation exists to determine the smallest justified implementation scope for future Relationship Observation.

It is architecture and implementation-scoping only. It does not implement `RelationshipFact`, Relationship Observation, Behavior Reconciliation, Boundary Reconciliation, Ownership Reconciliation, Repository Observation changes, Documentation Observation changes, Runtime changes, repository-wide graph building, runtime tracing, production behavior, or tests.

The self-model evidence architecture reconciliation established that Seed is converging on evidence appropriate to each claim type rather than treating documentation or repository structure as universal proof. In that architecture, artifact facts support existence and some structure, relationship evidence is needed for behavior, and constraint or authority evidence is needed for boundary and ownership.

Behavior reconciliation identified the gap more narrowly: behavior claims need relationship-oriented evidence that links a participant to an operation or flow. Structure can show that things exist or are contained; it cannot show that one thing invokes, routes, records, stores, emits, validates, returns, or executes another thing.

Relationship fact reconciliation gave the conceptual name for the missing primitive: relationship evidence, represented conceptually as `RelationshipFact`. That finding did not require an immediate production type. It required preserving the distinction between observed things and observed connections between things.

This document therefore asks a narrower implementation-scoping question:

```text
What is the smallest useful and safe Relationship Observation v0 capability?
```

The purpose is not to design all relationship acquisition. The purpose is to determine whether there is now enough architecture to justify a bounded first acquisition slice, and if so, which slice is smallest.

## Files Inspected

Required context inspected for this reconciliation:

- `docs/self_model_evidence_architecture_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/behavior_claim_reconciliation.md`
- `docs/boundary_claim_reconciliation.md`
- `docs/ownership_claim_reconciliation.md`
- `docs/repository_observation_language_boundary.md`
- `docs/repository_artifact_ontology_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

## 2. Central Finding

The smallest justified relationship acquisition capability is:

```text
static imports-style relationship evidence acquired from source syntax
```

In conceptual terms, v0 should acquire relationships of this form:

```text
subject imports object
```

where:

- `subject` is the importing module, file, or other source artifact identity available from repository observation context;
- `relationship_kind` is `imports`;
- `object` is the imported module, imported symbol, or import target as deterministically observed from source syntax.

This is the smallest justified capability because it establishes the missing relationship-acquisition primitive without crossing into behavior interpretation. Imports are syntactic, local, deterministic, already adjacent to current repository artifact observation, and useful as dependency or name-availability evidence. They do not require call graph construction, runtime execution, semantic inference, routing analysis, ownership rules, boundary constraints, or integration-test interpretation.

The evidence architecture reconciliations did identify a concrete missing acquisition primitive. The primitive is relationship evidence: observed connections between repository artifacts or between artifacts and other evidence-backed concepts. Relationship Observation v0 should acquire that primitive in its weakest safe form, not interpret it as behavior.

Relationship Observation v0 is therefore a smaller step than Behavior Reconciliation because it acquires one limited kind of relationship evidence. Behavior Reconciliation would evaluate behavior claims against relationship evidence and rules. An import edge can become input to future reconciliation, but v0 should not decide whether an import means a call, route, behavior, boundary, ownership, or architectural authority.

## 3. Candidate Relationship Kinds

The following candidate relationship kinds are evaluated for implementation complexity, inference risk, architectural risk, and v0 suitability.

| Relationship kind | Implementation complexity | Inference risk | Architectural risk | Suitability for v0 |
| --- | --- | --- | --- | --- |
| `contains` | Low to moderate when limited to lexical containment or existing parent metadata. | Low for structure; high if interpreted as behavior. | Medium because Repository Observation already owns artifact structure, so adding this could blur whether Relationship Observation is distinct from structure observation. | Not recommended for v0. It is useful, but it does not best demonstrate the missing relationship primitive because containment is already structurally adjacent. |
| `imports` | Low. Static import syntax can be parsed deterministically by language adapters and scoped to source files. | Low if treated only as name availability or dependency evidence; high only if overread as use or behavior. | Low when guarded carefully. It creates a relationship edge while avoiding operational claims. | Recommended for v0. It is the smallest safe relationship edge. |
| `calls` | Moderate to high. Requires call-site extraction, caller identity, callee resolution, alias handling, method/member handling, and source spans. | Medium to high because static calls may be conditional, unreachable, test-only, dynamically rebound, or semantically ambiguous. | High because call evidence is behavior-adjacent and can pressure the system toward behavior inference or call graph construction. | Not recommended for v0. It is a plausible later relationship kind but too behavior-adjacent for the smallest safe first slice. |
| `routes` | High. Requires understanding dispatch tables, branch conditions, route labels, handler mappings, and whether the route structure is used. | High because route labels may be strings or domain concepts, and declarations may not be executed. | High because routing quickly implicates behavior, boundary, and ownership claims. | Not recommended for v0. It belongs after relationship evidence and behavior guardrails are proven. |
| `stores` | High. Requires identifying mutation or persistence operations and distinguishing durable storage from local assignment, caching, or temporary state. | High because writes can be incidental, conditional, temporary, rollback-only, or not architecturally meaningful. | High because storage claims often imply ProjectionStore, persistence, ownership, or boundary questions. | Not recommended for v0. |
| `emits` | Moderate to high. Requires distinguishing event declarations, event construction, append/publication, logs, messages, and output values. | High because constructing or naming an event is not emission. | High because emission can imply event taxonomy, ledger behavior, response behavior, or integration paths. | Not recommended for v0. |
| `validates` | High. Requires identifying predicates, checks, schemas, assertions, failure consequences, and ordering. | Very high because incidental exceptions or guard names may be mistaken for validation behavior. | Very high because validation often supports boundary and policy claims. | Not recommended for v0. |
| `registers` | Moderate. Static tables and decorators may be observable, but dynamic registration and handler identity can be difficult. | Medium because registration proves availability, not execution. | Medium to high because handler availability can be misread as dispatch, execution, or ownership. | Not recommended for v0. It may be a later behavior-adjacent relationship after imports prove the acquisition path. |
| `dispatches` | High. Requires selected target evidence, invocation evidence, branch or table interpretation, and often call-site analysis. | High because dispatch can be indirect and context-dependent. | High because it is directly behavior-oriented and can invite automatic architecture inference. | Not recommended for v0. |

The comparison supports a conservative conclusion: `imports` is the only candidate that meaningfully exercises relationship acquisition while keeping inference risk and architectural risk low.

## 4. Recommended v0 Scope

Relationship Observation v0 should choose:

```text
imports
```

The recommended v0 scope is static import relationship acquisition only.

The smallest acceptable scope is:

- read source syntax;
- identify import declarations supported by the relevant language adapter;
- emit or prepare evidence for `subject imports object` relationships;
- preserve source path and evidence source;
- preserve the fact that the evidence source is static syntax;
- avoid interpreting the relationship beyond name availability, dependency, or static coupling.

This scope is justified because it establishes the ability to acquire an edge rather than only a node. It is safer than `calls`, `routes`, `stores`, `emits`, `validates`, `registers`, or `dispatches` because it does not require method-body interpretation, runtime-path reasoning, data-flow analysis, event semantics, persistence semantics, validation semantics, handler execution, or architectural authority.

`contains` is also small, but it is not the recommended v0 relationship kind. Containment is already close to the existing structure layer, especially where method parent metadata exists. Choosing containment would risk making Relationship Observation look like a repackaging of Repository Observation structure. Imports better demonstrate the missing relationship primitive while remaining safely non-behavioral.

## 5. RelationshipFact Review

Relationship fact reconciliation found that artifact facts describe things while relationship facts describe connections between things. For this v0 scoping document, the conceptual shape should remain minimal:

```text
subject
relationship kind
object
```

At a conceptual level:

- `subject` is the source-side artifact or concept participating in the observed relationship;
- `relationship kind` names the observed edge type;
- `object` is the target-side artifact, symbol, module, route label, event concept, operation concept, state concept, or other evidence-backed target.

For imports-style v0 evidence:

```text
subject = importing source artifact
relationship kind = imports
object = imported module or symbol target
```

This review does not define a production schema, type, event, package export, storage model, reconciliation rule, or implementation path. It only preserves the conceptual boundary needed for future implementation: a relationship is an observed edge with direction and kind, not a claim interpretation.

## 6. Evidence Source Review

Possible acquisition sources have different safety profiles.

| Evidence source | Complexity | Safety | v0 assessment |
| --- | --- | --- | --- |
| AST imports | Low. Import declarations are syntactic and usually adapter-local. | Highest. They are deterministic static evidence when source path and syntax are preserved. | Recommended source for v0. |
| Call sites | Moderate to high. Requires enclosing-scope attribution and callee resolution. | Medium. Static calls can be conditional, unreachable, test-only, aliased, or dynamically rebound. | Not v0. |
| Routing tables | High. Requires domain interpretation of route keys, handlers, and usage. | Low to medium. Declared routes may be dormant or configuration-only. | Not v0. |
| Event declarations | Moderate. Event classes or names can be found, but emission is separate. | Medium for declarations; low if interpreted as emission. | Not v0. |
| Registration tables | Moderate. Some entries are static; others are dynamic. | Medium. Registration does not prove dispatch or execution. | Not v0. |
| Runtime traces | High. Requires execution, instrumentation, trace interpretation, and instance scoping. | Low for architecture generalization. Strong for observed instances but risky as general proof. | Explicitly out of v0. |
| Integration tests | High. Requires test execution or static test interpretation and mock awareness. | Medium. Tests prove scoped examples, not exhaustive architecture. | Explicitly out of v0. |

The smallest and safest source for v0 is:

```text
AST import syntax
```

This source preserves the acquisition boundary: it is local, read-only, static, deterministic, and non-semantic. It can create relationship evidence without claiming behavior.

## 7. Relationship Observation vs Repository Observation

Repository Observation should not simply absorb relationships as undifferentiated repository artifacts.

Repository Observation currently asks:

```text
What repository artifacts exist?
```

Relationship acquisition asks a different question:

```text
What observed connections exist between artifacts or evidence-backed concepts?
```

The acquisition may share scanners, adapters, source parsing, file traversal, and repository context with Repository Observation. However, the conceptual output should remain separate because a node and an edge support different reconciliation questions.

Recommendation:

```text
Relationship acquisition should remain conceptually separate,
even if a future implementation reuses Repository Observation infrastructure.
```

This preserves the evidence ladder:

```text
Artifact facts support existence and some structure.
Relationship evidence supports dependency and behavior-adjacent questions.
Constraint and authority evidence support boundary and ownership questions.
```

If relationships are absorbed into generic artifact facts without preserving relationship kind, direction, source, and guardrails, Seed risks treating repository shape as behavior proof again. The conceptual separation is therefore architecturally important even for an imports-only v0.

## 8. What v0 Does Not Prove

Relationship Observation v0 must preserve strict guardrails. Imports-style relationship evidence does not prove behavior, boundary, ownership, or architectural authority.

Required non-equivalences:

```text
imports ≠ calls
imports ≠ routes
imports ≠ stores
imports ≠ emits
imports ≠ validates
imports ≠ registers
imports ≠ dispatches
imports ≠ ownership
imports ≠ behavior
imports ≠ architectural authority
imports ≠ runtime participation
imports ≠ execution
imports ≠ responsibility
imports ≠ boundary
imports ≠ constraint
imports ≠ implementation completeness
imports ≠ documentation correctness
imports ≠ support for broad behavior claims
```

An import can show that a name, module, or symbol is made available in a source file. It can support dependency or name-availability evidence. It cannot show that the imported target is used, invoked, reached, selected, executed, emitted, persisted, validated, owned, or architecturally authoritative.

Examples:

- `Runtime imports ToolExecutor` does not prove `Runtime calls ToolExecutor`.
- `Runtime imports ToolExecutor` does not prove `Runtime routes decisions to ToolExecutor`.
- `Projection code imports ProjectionStore` does not prove that it stores snapshots.
- `A module imports an event class` does not prove that it emits or records that event.
- `A package imports an owner-like component` does not prove ownership, boundary control, or responsibility.

These guardrails are not caveats to be weakened later. They are the reason imports are safe enough for v0.

## 9. Relationship Observation v0 Boundaries

Relationship Observation v0 should explicitly reject:

- call graph construction;
- behavior inference;
- boundary inference;
- ownership inference;
- repository-wide graph building;
- runtime tracing;
- LLM semantic reasoning;
- automatic architecture inference;
- routing analysis;
- registration execution analysis;
- event emission analysis;
- validation analysis;
- persistence or storage analysis;
- integration-test behavior interpretation;
- documentation-claim truth arbitration;
- Runtime integration;
- Repository Observation expansion beyond the bounded import source needed for v0;
- Documentation Observation changes;
- new runtime behavior;
- new tests as part of this reconciliation.

The v0 boundary is intentionally narrow:

```text
Acquire a static import edge.
Do not interpret the edge as behavior.
```

## 10. Acquisition Impact

If imports-style relationship evidence exists, future work becomes possible without being recommended for implementation in this document.

Potential future capabilities enabled by import evidence include:

- comparing documentation dependency claims against observed static dependency evidence;
- identifying candidate participants for later call-site or behavior evidence review;
- distinguishing artifact existence from dependency edges in the self-model evidence ladder;
- preserving source-backed relationship evidence for future reconciliation rules;
- improving architecture discussions by naming when evidence is only import-level;
- evaluating whether later relationship kinds need separate acquisition sources or stronger guardrails;
- demonstrating that Relationship Observation can emit bounded, read-only evidence without becoming Runtime, Repository Observation, or a graph inference engine.

This impact is deliberately modest. Imports evidence is useful because it creates a relationship acquisition foothold, not because it settles behavior, boundary, or ownership claims.

## 11. Current Frontier Assessment

Relationship Observation v0 is now justified as an architecture-scoped future implementation candidate.

Additional architecture work is not required before identifying the smallest justified scope. The existing reconciliations already establish:

- artifact facts are insufficient for behavior claims;
- behavior needs relationship-oriented evidence;
- relationship evidence should preserve subject, kind, object, source, and evidence boundaries;
- boundary and ownership require stronger evidence than relationships alone;
- current acquisition expansion should remain bounded, read-only, and non-runtime.

The justified v0 scope is not full behavior acquisition. It is imports-style relationship acquisition. That scope is small enough to be considered the next missing acquisition primitive while preserving all higher-layer guardrails.

Answer to the central frontier question:

```text
Yes. Relationship Observation v0 is justified.
```

The concrete missing acquisition primitive is:

```text
relationship evidence
```

The smallest safe first expression of that primitive is:

```text
static imports-style relationship evidence
```

Behavior, boundary, and ownership remain out of scope.

## 12. Non-Goals

This reconciliation rejects the following as non-goals:

- `RelationshipFact` implementation;
- Relationship Observation implementation;
- Behavior Reconciliation implementation;
- Boundary Reconciliation implementation;
- Ownership Reconciliation implementation;
- Runtime integration;
- ToolExecutor integration;
- EventLedger integration;
- ProjectionStore integration;
- Repository Observation production changes;
- Documentation Observation production changes;
- repository scanning expansion;
- repository-wide dependency graph construction;
- call graph construction;
- route graph construction;
- automatic architecture inference;
- LLM semantic reasoning as evidence;
- runtime tracing;
- provider calls;
- projection mutation;
- event appends;
- new runtime behavior;
- new tests;
- package export changes;
- production code changes.

## Explicit Answers

### Did the evidence architecture reconciliations identify a concrete missing acquisition primitive?

Yes.

The concrete missing acquisition primitive is:

```text
relationship evidence
```

This is evidence for observed connections between things, distinct from artifact evidence for observed things.

### What is the smallest justified relationship acquisition capability?

The smallest justified capability is:

```text
static imports-style relationship evidence
```

It is small because it is syntax-backed, local, deterministic, read-only, and non-runtime. It is useful because it establishes acquisition of an edge rather than only acquisition of a node.

### Why is Relationship Observation v0 a smaller step than Behavior Reconciliation?

Relationship Observation v0 is smaller because it acquires only one weak relationship evidence kind and performs no claim interpretation.

Behavior Reconciliation would require rules that evaluate behavior claims such as `calls`, `routes`, `stores`, `emits`, or `validates` against evidence. That requires stronger relationship kinds, source-specific confidence, and more guardrails. Imports-style v0 only says that a static import relationship was observed. It does not say that behavior occurred.

## Documentation-Only Status

This document is documentation-only architecture and implementation-scoping. It changes no production code, no tests, no Runtime behavior, no Repository Observation implementation, no Documentation Observation implementation, no behavior reconciliation implementation, no boundary reconciliation implementation, and no ownership reconciliation implementation.
