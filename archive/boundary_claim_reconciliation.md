# Boundary Claim Reconciliation

## 1. Purpose

This document reconciles the boundary layer in Seed's self-model evidence ladder.

It is documentation-only architecture research. It does not modify production code, tests, Repository Observation, Documentation Observation, Runtime, ToolExecutor, EventLedger, ProjectionStore, repository scanning, reconciliation behavior, acquisition behavior, runtime behavior, package exports, or any implementation path.

The current evidence ladder is:

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

Earlier reconciliation work established these adjacent layers:

- Existence primarily consumes `RepositoryArtifactFact` records to determine whether named artifacts are present.
- Structure primarily consumes `RepositoryArtifactFact` records plus containment or other static arrangement evidence.
- Behavior likely consumes `RelationshipFact` records because behavior describes operational connections between things.
- Ownership requires stronger evidence than behavior alone because it asserts architectural authority and responsibility.

Boundary reconciliation exists because behavior exposed a remaining middle layer between participation and ownership:

```text
X performs Y.
X is constrained to Y.
X owns Y.
```

Those statements are not equivalent. A component may perform an action without being the architectural boundary for that action. A component may serve as the architectural boundary for a responsibility without owning the entire domain. A component may own a responsibility only when authority, scope, responsibility, and competing-owner guardrails are also established.

Behavior alone is not enough because behavior describes what happens, not what is allowed, required, prohibited, constrained, or intentionally separated. A call site can show that `Runtime` calls `ToolExecutor`; it does not show that all execution must pass through `ToolExecutor`, that direct execution elsewhere is forbidden, or that `ToolExecutor` has architectural authority over execution.

Ownership is stronger than boundary because ownership asserts responsibility authority. A boundary can mark the edge where a concern must pass, where an operation may or may not occur, or where one layer hands off to another. Ownership additionally asks who is accountable for the concern, whether the owner has exclusive or primary authority under a declared scope, and whether competing owners are absent or intentionally subordinate.

## Files Inspected

Required context inspected for this reconciliation:

- `docs/relationship_fact_reconciliation.md`
- `docs/behavior_claim_reconciliation.md`
- `docs/structure_claim_reconciliation.md`
- `docs/repository_artifact_ontology_reconciliation.md`
- `docs/alignment_semantics_reconciliation.md`
- `docs/self_model_and_alignment_architecture_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

## 2. Central Finding

A boundary claim asserts that a responsibility, authority, capability, workflow, state transition, policy, or architectural concern is intentionally constrained to a specific component or set of components.

In compact form:

```text
Behavior describes what happens.
Boundary describes what is allowed, required, prohibited, or constrained.
Ownership describes authority and architectural responsibility.
```

A boundary claim answers questions such as:

```text
Where may Y occur?
Where must Y pass through?
Where is Y prohibited?
Which component separates concern A from concern B?
Which component constrains capability C?
Which component is the required handoff point for workflow W?
```

Examples of boundary-oriented meanings include:

```text
ToolExecutor is the execution boundary.
Repository Observation must not execute code.
Documentation Observation must not inspect repositories.
Only ProjectionStore may persist projection snapshots.
Runtime is the routing boundary between decisions and tool execution.
```

The central finding is:

```text
Boundary reconciliation needs constraint-oriented evidence,
not relationship evidence alone.
```

Behavior reconciliation did expose another missing evidence primitive. The missing primitive is not only `RelationshipFact`; boundary claims likely require an additional constraint-family primitive such as:

```text
ConstraintFact
InvariantFact
PolicyFact
```

The exact future representation is not recommended here. The architectural finding is narrower: relationship evidence can show participation, but boundary support requires evidence that the participation is intentionally constrained, required, prohibited, or guarded.

## 3. Examples Of Boundary Claims

The following examples show how similar phrases belong to different layers or mix layers.

| Claim | Classification | Reason |
| --- | --- | --- |
| `Runtime owns routing decisions.` | Ownership, with behavior and boundary prerequisites | `owns` asserts architectural authority over routing decisions. Behavior evidence may show that Runtime routes decisions, and boundary evidence may show routing is constrained to Runtime, but ownership requires stronger responsibility and authority evidence. |
| `ToolExecutor is the execution boundary.` | Boundary | This says execution is intentionally constrained to or mediated by ToolExecutor. It is stronger than `ToolExecutor executes operations` and weaker than `ToolExecutor owns execution`. |
| `ProjectionStore is the snapshot-storage boundary.` | Boundary | This says snapshot storage should cross or terminate at ProjectionStore. It does not by itself prove that ProjectionStore owns the broader projection-storage responsibility. |
| `ContextComposer is responsible only for context composition.` | Mixture of boundary and possible ownership | `responsible` can imply ownership, while `only` introduces a negative boundary limiting the component's scope. It should be decomposed into `ContextComposer composes context`, `ContextComposer is constrained to context composition`, and possibly `ContextComposer owns context composition` if authority is claimed. |
| `Repository Observation must not execute code.` | Boundary | This is a negative constraint over Repository Observation. It says a capability is prohibited for that component; it does not say which component owns execution. |
| `Documentation Observation must not inspect repositories.` | Boundary | This is a negative constraint separating Documentation Observation from repository inspection. It constrains acquisition responsibility without asserting ownership of repository inspection. |

Mixtures should be decomposed before reconciliation. For example:

```text
Runtime owns routing decisions and must route executable operations through ToolExecutor.
```

contains at least three claims:

1. `Runtime routes executable operations through ToolExecutor.` — behavior.
2. `Executable operations must pass through ToolExecutor.` — boundary.
3. `Runtime owns routing decisions.` — ownership.

## 4. Behavior vs Boundary

Behavior and boundary differ by the type of assertion being made.

```text
Runtime routes call_tool decisions.
```

is a behavior claim. It says that Runtime participates in an operational routing flow for `call_tool` decisions.

```text
Runtime is responsible for routing decisions.
```

is not merely behavior. It is at least a boundary claim and may be an ownership claim depending on how `responsible` is used. It says routing responsibility is assigned or constrained to Runtime, not merely that Runtime was observed routing something.

Likewise:

```text
ToolExecutor executes operations.
```

is a behavior claim. It says ToolExecutor participates in operation execution.

```text
ToolExecutor is the execution boundary.
```

is a boundary claim. It says execution is intentionally mediated by, constrained to, or required to pass through ToolExecutor.

The difference is:

| Question | Behavior | Boundary |
| --- | --- | --- |
| What does it ask? | Did X participate in action Y? | Is Y constrained, required, prohibited, or separated at X? |
| Typical evidence | Call site, dispatch path, mutation, event append, storage call, validation step, execution path. | Invariant, policy, design constraint, negative rule, test preserving separation, architecture metadata, rejected alternative, validation rule. |
| What it can support | Participation in a runtime-relevant action. | Intentional separation, permission, prohibition, scope limit, or required handoff. |
| What it cannot support alone | Boundary preservation or ownership. | Ownership authority or full responsibility unless ownership evidence is also present. |

A behavior claim may be evidence inside a boundary rule, but it does not become boundary support by itself. For example, a call from Runtime to ToolExecutor can help support a claim that execution is routed through ToolExecutor only if paired with evidence that this route is required, enforced, or intentionally constrained.

## 5. Boundary vs Ownership

This is the critical distinction.

```text
ToolExecutor is the execution boundary.
```

is a boundary claim. It asserts that execution is intentionally mediated by, constrained to, or required to pass through ToolExecutor under a declared scope.

```text
ToolExecutor owns execution.
```

is an ownership claim. It asserts that ToolExecutor is the architectural authority for execution responsibility under a declared scope.

Similarly:

```text
ProjectionStore is the snapshot boundary.
```

is a boundary claim. It says snapshot access, persistence, or lifecycle transitions are constrained to ProjectionStore or cross the ProjectionStore edge.

```text
ProjectionStore owns snapshot storage.
```

is an ownership claim. It says ProjectionStore has responsibility authority for snapshot storage, not merely that snapshot storage is constrained at that boundary.

Additional evidence that may move a claim from boundary to ownership includes:

- explicit documentation naming the component as the owner or authority for the responsibility;
- architecture metadata assigning responsibility to the component;
- evidence that relevant behaviors occur through the component under the declared scope;
- boundary evidence showing other components must route through, defer to, or avoid bypassing the component;
- tests or invariants preserving the responsibility boundary;
- policy or validation rules that reject competing paths;
- absence of competing owners within the declared evidence scope;
- positive authority evidence, not only negative prohibition evidence;
- a declared scope narrow enough that the ownership claim can be evaluated.

Boundary is therefore necessary but not sufficient for many ownership claims. A boundary can say:

```text
Do not cross this line except through X.
```

Ownership says:

```text
X is architecturally accountable for this responsibility.
```

A gate is not always an owner. A storage API can be the boundary for writes without owning all storage policy. A runtime route can be the boundary for dispatch without owning the entire capability domain. A negative constraint can prevent one component from acting without identifying the component that owns the action.

## 6. Candidate Boundary Evidence

Boundary support likely needs constraint-oriented evidence. Candidate evidence sources include:

| Evidence source | Strength | Weakness |
| --- | --- | --- |
| Architectural invariants | Strong evidence when explicit, scoped, and preserved as durable architecture. | May be aspirational if not connected to tests, validation, or repository behavior. |
| Documentation | Useful for intended boundaries and non-goals. | Documentation claims are not self-proving; they support claim existence unless paired with implementation, test, or policy evidence under an explicit rule. |
| Reconciliation documents | Strong for Seed's current architecture because they record evaluated findings, distinctions, and non-goals. | They can still be documentation-only and may not prove enforcement in code. |
| Design constraints | Strong when expressed as `must`, `must not`, `only`, `requires`, or `constrained to` under a clear scope. | Ambiguous constraints can collapse into ownership language if not decomposed. |
| Negative findings | Useful guardrails because rejected concepts show what must not be inferred or implemented. | A negative finding does not necessarily identify the positive boundary or owner. |
| Rejected concepts | Useful evidence that a path is outside a component's boundary. | Rejection of one implementation path does not prove all alternatives are forbidden. |
| Tests | Strong if they assert separation, prohibition, required route, or failed bypass. | Tests can be narrow, fixture-only, or implementation-specific; passing behavior tests may still not prove boundary. |
| Enforcement code | Strong when code rejects, prevents, validates, or routes according to the constraint. | Enforcement code may be local, bypassable, or not authoritative without scope evidence. |
| Validation rules | Strong for prohibited states, invalid operations, and required preconditions. | Validation of data is not always validation of architecture responsibility. |

The strongest candidate support for a boundary claim is usually combined evidence:

```text
behavior evidence
+
constraint evidence
+
explicit scope
```

The weakest candidate support is usually a single observed relationship or a single broad documentation sentence without constraint form, scope, or corroborating evidence.

## 7. RelationshipFact Impact

Can `RelationshipFact` alone support boundary claims?

Usually no.

`RelationshipFact` can support behavior because it describes connections between things:

```text
Runtime calls ToolExecutor.
Runtime routes call_tool decisions to ToolExecutor.
ProjectionStore stores ProjectionSnapshot.
```

Those facts describe what was observed. They do not, by themselves, describe what is allowed, required, prohibited, exclusive, constrained, or intentionally separated.

For example:

```text
RelationshipFact: Runtime calls ToolExecutor.
```

may support:

```text
Runtime calls ToolExecutor.
```

It does not by itself support:

```text
Runtime must route execution through ToolExecutor.
Only ToolExecutor may execute operations.
ToolExecutor is the execution boundary.
ToolExecutor owns execution.
```

Boundary support likely needs:

```text
relationship evidence
+
constraint evidence
```

Relationship evidence alone shows participation. Constraint evidence shows that the participation is architecturally required, prohibited elsewhere, constrained to a component, or intentionally separated from another concern.

There may be narrow exceptions if a future `RelationshipFact` subtype explicitly encodes constraint semantics, such as `prohibits`, `requires`, or `only_allows`. In that case, the support would come from constraint semantics embedded in the relationship representation, not from ordinary call, import, storage, or route evidence alone.

## 8. Candidate Boundary Rule Forms

The following possible future boundary-claim forms are evaluated only. They are not implementation recommendations.

### `X is the boundary for Y.`

Meaning:

```text
Concern Y is intentionally constrained to, mediated by, or separated at X.
```

Likely evidence requirements:

- X exists;
- Y is a defined concern, capability, workflow, operation, state transition, or policy;
- relationship evidence showing Y interacts with X when behavior is relevant;
- constraint, invariant, policy, test, or documentation evidence that Y is intentionally constrained at X;
- explicit scope for the boundary.

Weaknesses:

- `boundary` can be vague without a declared concern and scope;
- this form can be mistaken for ownership if `the boundary` is treated as `the owner`.

### `X is responsible for Y.`

Meaning:

```text
Y is assigned to X in some responsibility sense.
```

Likely evidence requirements:

- explicit disambiguation between boundary responsibility and ownership responsibility;
- documentation or architecture metadata using responsibility language;
- behavior evidence when the responsibility includes operational participation;
- boundary evidence when the responsibility constrains other components;
- stronger authority evidence if evaluated as ownership.

Weaknesses:

- `responsible` is ambiguous;
- it should often be decomposed into behavior, boundary, and ownership claims before evaluation.

### `X must not perform Y.`

Meaning:

```text
Y is prohibited for X.
```

Likely evidence requirements:

- explicit negative constraint, invariant, policy, non-goal, validation rule, or test;
- evidence identifying X and Y;
- scope explaining whether the prohibition is architectural, runtime, acquisition, repository, documentation, or test-only.

Weaknesses:

- a prohibition on X does not identify who may perform or own Y;
- absence of behavior is not sufficient proof of prohibition.

### `Only X may perform Y.`

Meaning:

```text
Y is exclusive to X under a declared scope.
```

Likely evidence requirements:

- explicit exclusivity evidence;
- behavior evidence that X performs Y if the claim includes actual performance;
- negative or validation evidence that non-X paths are rejected or forbidden;
- absence of competing performers within the declared evidence scope;
- careful scope limitation.

Weaknesses:

- this form is close to ownership and may require ownership-level guardrails;
- repository-wide absence is hard to prove without a scoped acquisition model.

### `Y is constrained to X.`

Meaning:

```text
Y may occur only through, inside, or at X under the declared constraint.
```

Likely evidence requirements:

- constraint, invariant, policy, or test evidence;
- relationship evidence when Y is an operational behavior;
- scope and bypass rules;
- conflict evidence if Y is observed outside X.

Weaknesses:

- `constrained to` can refer to location, authority, interface, workflow, or permission;
- broad versions risk accidental ownership inference.

## 9. Acquisition Impact

Future boundary reconciliation would likely require more than `RelationshipFact`.

A plausible evidence stack is:

```text
RepositoryArtifactFact
+
RelationshipFact
+
ConstraintFact / InvariantFact / PolicyFact
```

where:

- `RepositoryArtifactFact` identifies components, artifacts, and candidate participants;
- `RelationshipFact` identifies observed operational or structural connections;
- `ConstraintFact` identifies required, prohibited, exclusive, or constrained behavior;
- `InvariantFact` identifies durable rules that should remain true across implementations;
- `PolicyFact` identifies declared permissions, prohibitions, responsibilities, or allowed paths.

This document does not recommend implementing those records. It only records that boundary support probably needs a constraint-family evidence primitive because the existing lower layers do not carry enough semantics.

Alternative future representations may be possible. For example, a future architecture could encode constraints as relationship subtypes, metadata on documentation claims, test-derived facts, or invariant records. The important architectural requirement is not the name of the type. The requirement is that boundary reconciliation must distinguish:

```text
observed connection
```

from:

```text
intentional constraint
```

Without that distinction, Seed would risk treating every call, import, route, or storage operation as a boundary.

## 10. Alignment Impact

Boundary reconciliation should fit into the existing alignment outcomes:

```text
supported
missing_support
not_evaluable
potential_conflict
```

No new outcomes are required.

| Outcome | Boundary-claim meaning |
| --- | --- |
| `supported` | The boundary claim pattern is recognized, and supplied evidence satisfies the rule's constraint, relationship, and scope requirements. |
| `missing_support` | The boundary claim pattern is recognized, the rule knows what evidence is required, and supplied evidence lacks required constraint or supporting relationship evidence. |
| `not_evaluable` | The claim does not match a supported boundary pattern, uses ambiguous responsibility language that has not been decomposed, or the supplied evidence lacks the evidence type needed to evaluate boundary constraints. |
| `potential_conflict` | The boundary claim pattern is recognized, and supplied evidence suggests a bypass, competing boundary, prohibited action, incompatible constraint, or observed behavior outside the declared boundary. |

The default for broad or ambiguous boundary prose should be `not_evaluable`, not `missing_support`. For example:

```text
Runtime is responsible for everything important.
```

should not become `missing_support` merely because no boundary evidence exists. It is too broad and should be decomposed before evaluation.

A recognized but unsupported boundary form can be `missing_support`. For example:

```text
Only ToolExecutor may execute registered operations.
```

could be `missing_support` under a future rule if the evidence includes behavior that ToolExecutor executes operations but lacks any exclusivity, prohibition, invariant, policy, test, or bypass-prevention evidence.

## 11. Boundary Failure Modes

Boundary reconciliation must avoid these failure modes:

| Failure mode | Risk | Guardrail |
| --- | --- | --- |
| Inferring ownership from behavior | A component that participates in an action is incorrectly treated as the authority for that action. | Keep behavior verbs below boundary and ownership; require explicit authority evidence for ownership. |
| Inferring ownership from relationships | Calls, imports, routes, or storage edges become responsibility assignments. | Treat `RelationshipFact` as participation evidence unless it explicitly carries constraint or authority semantics. |
| Inferring boundaries from call sites alone | A single call path is mistaken for a required architectural boundary. | Require constraint, invariant, policy, test, or validation evidence plus scope. |
| Inferring authority from containment | A method or helper inside a class is treated as proof that the class owns the concern. | Structure supports arrangement, not behavior, boundary, or ownership. |
| Inferring prohibition from absence | Failure to observe X performing Y becomes proof that X must not perform Y. | Require explicit negative evidence for `must not` claims. |
| Inferring exclusivity from one path | One successful route through X becomes `only X may perform Y`. | Require exclusivity evidence and scoped absence of competing paths. |
| Treating documentation as enforcement | Architectural prose becomes proof that the repository enforces the boundary. | Separate documentation support from repository, test, invariant, and validation support. |
| Collapsing boundary into ownership | `X is the boundary for Y` is treated as `X owns Y`. | Require separate owner, authority, responsibility, and competing-owner evidence. |
| Collapsing negative findings into positive ownership | `Runtime must not execute tools` becomes `ToolExecutor owns all execution`. | Treat negative constraints as boundaries unless positive ownership evidence is present. |
| Using LLM semantic reasoning as proof | Plausible prose interpretation replaces evidence-backed rules. | Require explicit evidence primitives and rule forms; broad semantic claims remain not evaluable. |

The core guardrail is:

```text
Observed behavior is not a boundary.
Observed boundary is not ownership.
```

## 12. Non-Goals

This document rejects and does not perform:

- ownership inference;
- behavior implementation;
- Runtime integration;
- ToolExecutor integration;
- EventLedger integration;
- ProjectionStore integration;
- repository scanning expansion;
- Documentation Observation changes;
- Repository Observation changes;
- reconciliation behavior changes;
- acquisition behavior changes;
- test changes;
- production code changes;
- package export changes;
- LLM semantic reasoning as evidence;
- automatic architecture inference;
- automatic ownership inference;
- automatic boundary inference;
- new alignment outcomes;
- new fact types;
- new validators;
- new enforcement code.

## Questions Answered

### Did behavior reconciliation expose another missing evidence primitive?

Yes.

Behavior reconciliation exposed `RelationshipFact` for behavior claims, but boundary reconciliation exposes an additional missing constraint-family primitive. The likely primitive is one or more of:

```text
ConstraintFact
InvariantFact
PolicyFact
```

The purpose of that primitive would be to represent required, prohibited, exclusive, constrained, or intentionally separated architectural conditions. This document does not recommend implementing it; it only records that boundary claims need evidence beyond ordinary relationship evidence.

### Can boundary claims be supported by relationship evidence alone?

Usually no.

Relationship evidence can show that a connection occurred or is statically represented. Boundary claims require evidence that the connection is constrained, required, prohibited elsewhere, exclusive, guarded, or intentionally separated under a declared scope.

The likely future support shape is:

```text
behavior evidence
+
constraint or invariant evidence
+
explicit scope
```

not:

```text
relationship evidence alone
```

## Recommended Next Frontier

This document does not change the broader architectural recommendation that the near-term frontier remains knowledge acquisition expansion rather than Runtime implementation or additional engines.

The boundary-specific next frontier is documentation-only source mapping if maintainers choose to continue this research chain:

```text
Map existing invariant, non-goal, policy, and rejected-concept language
that could serve as future boundary evidence.
```

That mapping should remain documentation-only unless a concrete implementation need is separately approved. It should not modify Repository Observation, Documentation Observation, Runtime, ToolExecutor, EventLedger, ProjectionStore, tests, or reconciliation behavior.

The architectural conclusion is:

```text
Behavior describes what happens.
Boundary describes what is allowed, required, or constrained.
Ownership describes authority and architectural responsibility.
RelationshipFact is probably insufficient for boundary claims by itself.
Boundary claims likely require relationship evidence plus constraint/invariant evidence.
Ownership remains above boundary.
```
