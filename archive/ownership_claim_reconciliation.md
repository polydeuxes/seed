# Ownership Claim Reconciliation

## 1. Purpose

This document reconciles the ownership layer in Seed's self-model evidence ladder.

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

Earlier reconciliation work established these lower layers:

- Existence primarily consumes `RepositoryArtifactFact` records to determine whether named artifacts are present.
- Structure primarily consumes `RepositoryArtifactFact` records plus containment or other static arrangement evidence.
- Behavior likely consumes `RelationshipFact` records because behavior describes operational connections between things.
- Boundary likely consumes `RelationshipFact` records plus constraint-family evidence such as `ConstraintFact`, `InvariantFact`, or `PolicyFact` because boundary describes what is required, prohibited, constrained, or intentionally separated.

Ownership reconciliation exists because the lower layers can show that a component exists, is structurally arranged in a particular way, participates in a behavior, or is part of a boundary without proving that it is architecturally accountable for the concern.

Behavior is not ownership. A component can execute, route, store, emit, validate, compose, delegate, or record something without being the authoritative responsibility holder for that thing. Participation can be incidental, delegated, narrow, temporary, test-only, or subordinate to a different component.

Boundary is not ownership. A boundary can show where something must pass, where something may not occur, or which edge separates concerns. That does not by itself identify the component that is accountable for the capability, workflow, state transition, policy, or architectural concern. A boundary may be shared, delegated, enforced by a different owner, or scoped only to one entry point.

Ownership is the highest layer in the current evidence ladder because it is an architectural judgment about authority, responsibility, scope, and competing alternatives. It usually depends on lower-layer evidence but adds a further question:

```text
Given what exists, how it is structured, what it does, and what boundaries constrain it,
which component is the authoritative responsibility holder for this concern?
```

## Files Inspected

Required context inspected for this reconciliation:

- `docs/boundary_claim_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/behavior_claim_reconciliation.md`
- `docs/structure_claim_reconciliation.md`
- `docs/alignment_semantics_reconciliation.md`
- `docs/self_model_and_alignment_architecture_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

## 2. Central Finding

An ownership claim asserts that a component is the authoritative architectural responsibility holder for a capability, workflow, concern, state transition, execution path, policy, or boundary.

In compact form:

```text
Existence describes what is present.
Structure describes how present things are statically arranged.
Behavior describes what participates in operational flow.
Boundary describes what is required, prohibited, constrained, or separated.
Ownership describes architectural authority and responsibility.
```

Therefore, the central answer is:

```text
An ownership claim asserts that X is the authoritative architectural responsibility holder for Y under an explicit scope.
```

Ownership claims answer questions such as:

```text
Who is accountable for Y?
Who has primary or exclusive architectural authority over Y?
Where should changes to Y's semantics be made?
Which component is responsible for preserving Y's invariants?
Which component delegates Y, and to whom?
Which alternative owner candidates were considered and rejected, subordinated, or scoped away?
```

Ownership support is not merely a match between a documentation sentence and a named artifact. It likely emerges from converging evidence:

```text
artifact evidence
+
relationship evidence
+
boundary or constraint evidence
+
policy or invariant evidence
+
explicit scope
+
competing-owner evaluation
```

The exact future representation is not recommended here. The architectural finding is narrower: ownership should not be inferred from any lower layer by default.

## 3. Examples Of Ownership Claims

The following examples show how ownership wording can mix behavior, boundary, and ownership meanings.

| Claim | Classification | Reason |
| --- | --- | --- |
| `ToolExecutor owns registered-operation execution.` | Ownership, with behavior and boundary prerequisites | The phrase asserts that `ToolExecutor` is the authoritative responsibility holder for executing registered operations. Behavior evidence may show execution occurs there; boundary evidence may show execution is constrained there; ownership still requires scope, authority, and competing-owner evaluation. |
| `Runtime owns user-message intake.` | Mixture of behavior, boundary, and possible ownership | `Runtime` may receive or handle user messages as behavior. It may be the entry boundary for user-message intake. Ownership requires evidence that user-message intake semantics are architecturally assigned to Runtime rather than the CLI, an adapter, a transport layer, or another input component. |
| `ProjectionStore owns projection snapshot storage.` | Ownership, with boundary and storage behavior prerequisites | Storage behavior may show snapshots are saved or loaded through ProjectionStore. Boundary evidence may show snapshot persistence is constrained to ProjectionStore. Ownership requires evidence that ProjectionStore is accountable for snapshot storage semantics under a defined projection-storage scope. |
| `Repository Observation owns repository artifact acquisition.` | Ownership, with acquisition behavior and source-boundary prerequisites | Repository Observation may acquire repository artifacts and may be bounded to repository evidence. Ownership requires evidence that repository artifact acquisition is assigned to Repository Observation and not Documentation Observation, reconciliation, runtime, or a general acquisition engine. |

Each example should be decomposed before reconciliation. For example:

```text
ToolExecutor executes registered operations.
Only ToolExecutor may execute registered operations in the registered-operation path.
ToolExecutor is the authoritative owner of registered-operation execution.
```

These are not the same claim. They belong to behavior, boundary, and ownership respectively.

## 4. Ownership vs Behavior

Compare:

```text
ToolExecutor executes operations.
```

with:

```text
ToolExecutor owns operation execution.
```

The first claim is behavioral. It says ToolExecutor participates in an execution behavior. Candidate evidence might include call sites, dispatch paths, handler invocation, operation registry use, or integration tests that exercise execution.

The second claim is ownership. It says ToolExecutor is architecturally accountable for operation execution under a defined scope. Candidate evidence must address more than the fact that execution happens. It must address authority, scope, intended responsibility, delegated alternatives, and competing execution components.

Compare:

```text
Runtime routes decisions.
```

with:

```text
Runtime owns decision routing.
```

The first claim is behavioral. It says Runtime participates in routing decisions. Candidate evidence might include route branches, dispatch tables, or calls from Runtime to downstream handlers.

The second claim is ownership. It says Runtime is accountable for the decision-routing concern. It requires evidence that routing semantics are intentionally assigned to Runtime rather than ToolExecutor, a planner, a decision engine, a CLI adapter, or a future routing component.

Participation is not ownership because:

- a component can participate under another component's authority;
- a component can participate only in one path or one fixture;
- a component can participate by delegation rather than responsibility;
- a component can perform a behavior but not define its policy;
- a component can call an operation but not own the operation's semantics;
- a component can be a helper, adapter, facade, or implementation detail.

Behavior evidence is therefore usually necessary but insufficient. It can establish that an owner candidate participates in the claimed concern, but it cannot by itself establish architectural responsibility.

## 5. Ownership vs Boundary

Compare:

```text
ToolExecutor is the execution boundary.
```

with:

```text
ToolExecutor owns execution.
```

The first claim is boundary-oriented. It asserts that execution is constrained to, mediated by, or required to pass through ToolExecutor under some scope.

The second claim is ownership-oriented. It asserts that ToolExecutor is accountable for execution semantics under that scope. A boundary can be enforced by a component without that component owning the larger concern. For example, a runtime may route work to an execution boundary while the policy governing allowed work is owned elsewhere.

Compare:

```text
ProjectionStore is the snapshot boundary.
```

with:

```text
ProjectionStore owns snapshot storage.
```

The first claim asserts that snapshot persistence crosses or terminates at ProjectionStore. The second asserts that ProjectionStore is the authoritative responsibility holder for snapshot-storage semantics.

Additional evidence that may elevate a claim from boundary to ownership includes:

- explicit responsibility language, such as `owner`, `authoritative`, `responsible for`, or `delegated to`, under a clear scope;
- invariant evidence showing the component preserves the concern's rules;
- policy evidence showing the component is the intended decision authority for the concern;
- enforcement code showing bypasses are rejected or impossible within the claimed scope;
- tests that assert not only that a path works but that alternative paths are not valid;
- negative findings rejecting other plausible owner components;
- competing-owner analysis showing alternatives are absent, subordinate, delegated, or scoped differently.

Boundary evidence can be strong ownership support, but it remains insufficient if it does not answer who is architecturally accountable.

## 6. Candidate Ownership Evidence

Ownership likely requires multiple evidence classes. The table below evaluates candidate evidence sources without recommending implementation.

| Evidence source | Strength | Weakness / guardrail |
| --- | --- | --- |
| Architectural invariants | Strong when they state which component must preserve a concern's rules. | Invariants can be broad or aspirational if not tied to a component, scope, or enforcement path. |
| Constraint evidence | Strong when it states that only one component may perform, mutate, route, store, or decide something. | A constraint can identify a boundary without identifying the accountable owner. |
| Policy evidence | Strong when it assigns decision authority or permitted behavior to a component. | Policy can be enforced by one component and owned by another. |
| Negative findings | Strong guardrails when they reject proposed owners, engines, integrations, or inference paths. | Absence or rejection of one alternative does not prove a positive owner unless the candidate set and scope are known. |
| Boundary evidence | Useful prerequisite because owners often preserve boundaries. | Boundary is not responsibility; a component can be a gate without being the owner of the gated concern. |
| Behavior evidence | Useful prerequisite because an owner usually participates in or delegates the behavior. | Behavior is participation, not authority. |
| Tests | Strong when they assert responsibility, required paths, prohibited bypasses, or owner-specific invariants. | Tests can be narrow, mock-based, fixture-only, or examples rather than architecture-wide proof. |
| Enforcement code | Strong when it prevents bypass, rejects invalid responsibility transfer, or centralizes authority under a clear scope. | Code may be local, bypassable, or merely implementation detail without documentation or invariant support. |
| Reconciliation documents | Strong architectural memory because they record evaluated distinctions, non-goals, and findings. | Documentation-only findings should not be treated as executable enforcement. |
| Design documents | Useful for explicit assignment of responsibility and intended delegation. | Design intent can drift from repository behavior and must be paired with current evidence. |
| Rejected concepts | Useful for narrowing owner candidates and avoiding engine traps. | Rejecting a concept does not automatically prove a current component owns the concern. |
| Competing-owner analysis | Essential for broad ownership claims because ownership is comparative. | Requires careful scope; a component may be a competing owner in one scope and subordinate in another. |

The strongest candidate support for ownership is converging evidence rather than one evidence class:

```text
X participates in Y.
Y is constrained to X or delegated to X.
X preserves Y's relevant invariants or policy.
Alternative owner candidates are absent, rejected, subordinate, or separately scoped.
The claim scope is explicit.
```

The weakest candidate support is a single sentence, call site, containment relationship, or artifact name match.

## 7. Competing Owner Analysis

Can ownership be supported without considering competing owners?

Usually no for non-trivial ownership claims.

Ownership asserts architectural responsibility, and responsibility is often comparative. A component can be the best-supported owner only after the candidate set is understood under the claim's scope.

For example:

```text
ToolExecutor executes operations.
Runtime also executes operations.
```

If both statements are true under the same scope, then `ToolExecutor owns operation execution` is not fully supported by ToolExecutor behavior alone. The analysis must ask:

- Does Runtime execute directly, or does it route to ToolExecutor?
- Is Runtime an entry-point coordinator while ToolExecutor is the registered-operation execution owner?
- Is ToolExecutor delegated execution authority by Runtime?
- Are the two statements using different meanings of `execute`?
- Is one behavior test-only, fallback-only, or outside the registered-operation path?
- Does an invariant or policy assign execution authority to one component?

A competing owner need not defeat an ownership claim. It may instead refine the claim:

```text
Runtime owns decision routing.
ToolExecutor owns registered-operation execution.
ProjectionStore owns projection snapshot storage.
```

Competing-owner analysis therefore prevents over-broad ownership claims and encourages scoped ones. It is especially important when multiple components participate in the same workflow.

## 8. Ownership And Absence Evidence

Absence evidence can support ownership only as scoped corroboration.

Examples:

```text
No other execution component exists.
No competing snapshot owner exists.
```

These statements can help when they are derived from a clearly scoped search space and paired with positive evidence. For example, if repository evidence, design documents, and reconciliation findings all identify ProjectionStore as the snapshot-storage participant and no competing snapshot-storage owner exists in the scoped evidence set, absence evidence strengthens the ownership claim.

However, absence evidence has strict limitations:

- absence in supplied facts does not mean absence in the whole repository;
- absence in the repository does not mean absence in design intent;
- absence of a named component does not mean no helper, adapter, or external owner exists;
- absence of a competing class does not prove exclusive authority;
- absence findings can be invalidated by future acquisition slices;
- scope must be explicit, such as supplied fixture facts, selected source paths, current docs, or repository-wide acquisition.

Absence evidence should therefore never be considered sufficient by itself. It is a guardrail and corroborating signal, not a positive ownership proof.

## 9. Ownership And Repository Evidence

Can `RepositoryArtifactFact` support ownership?

Not by itself.

`RepositoryArtifactFact` can identify candidate owner artifacts such as `Runtime`, `ToolExecutor`, `ProjectionStore`, `ContextComposer`, or Repository Observation modules. It can also support existence and some structure claims when the rule is appropriately narrow.

But ownership is not existence. The fact that `ToolExecutor` exists does not prove that ToolExecutor owns execution. The fact that `ProjectionStore` exists does not prove that ProjectionStore owns snapshot storage. The fact that a method is contained in a class does not prove the class owns the method's broader architectural concern.

Repository artifact evidence can be a prerequisite for ownership support because an owner candidate should usually exist. It is insufficient because it does not establish behavior, boundary, authority, responsibility, policy, delegation, scope, or competing-owner status.

## 10. Ownership And Relationship Evidence

Can `RelationshipFact` support ownership?

Not by itself.

`RelationshipFact` can support behavior claims and can help show that an owner candidate participates in the claimed concern. For example, it may show that Runtime calls ToolExecutor, ToolExecutor invokes registered operations, ProjectionStore stores snapshots, or ContextComposer composes decision context.

But relationship evidence is still about connections and flow. It does not prove that the subject is architecturally accountable for the relationship. A call can be delegated. A route can be mechanical. A store operation can be one persistence implementation. A composition relationship can be shared with budget, selection, evidence, or state components.

Relationship evidence is therefore helpful and often necessary, but it must be combined with authority, scope, boundary, invariant, policy, and competing-owner evidence before an ownership claim can be reasonably supported.

## 11. Ownership And Constraint Evidence

Can `ConstraintFact`, `InvariantFact`, or `PolicyFact` support ownership?

Helpful, but insufficient alone.

Constraint-family evidence is stronger than behavior evidence for ownership because it can express required routes, prohibited bypasses, allowed responsibilities, invariants, and policies. It can say:

```text
Only X may perform Y.
Y must pass through X.
X must preserve invariant Z for Y.
Policy P is enforced at X.
```

Those statements may support boundary and may contribute to ownership. However, they still may not identify the complete owner. A policy can be authored elsewhere and enforced by X. An invariant can be preserved by multiple components. A boundary can be delegated to X by another owner. A constraint can be limited to one workflow path while the ownership claim is broader.

Constraint, invariant, and policy evidence should therefore be treated as high-value ownership evidence, not as automatic ownership proof.

## 12. Candidate Ownership Rule Forms

No rule is implemented or recommended here. The following rule forms are evaluated only.

### `X owns Y.`

Likely meaning:

```text
X is the authoritative responsibility holder for Y.
```

Likely evidence requirements:

- X exists as a candidate artifact or documented component;
- Y is explicitly scoped;
- X participates in, delegates, enforces, or preserves Y;
- architecture evidence assigns responsibility to X;
- competing owner candidates are absent, rejected, subordinate, delegated, or differently scoped.

### `Only X may perform Y.`

Likely meaning:

```text
Y is constrained to X under a defined scope.
```

This is primarily boundary evidence, not ownership by itself. It can support ownership if paired with evidence that X is accountable for Y rather than merely serving as the gate or enforcement point.

### `Y is delegated to X.`

Likely meaning:

```text
Some upstream owner or coordinator transfers responsibility for Y to X under a defined scope.
```

This can be strong ownership evidence if the delegator, delegatee, delegated scope, and authority transfer are explicit. It can also show that the delegating component is not the owner for the delegated subconcern.

### `X is the authoritative owner of Y.`

Likely meaning:

```text
X has explicit architectural authority and responsibility for Y.
```

This is the strongest ownership phrasing but still needs evidence. A future rule should likely require multiple evidence classes and competing-owner analysis before returning `supported`.

## 13. Alignment Impact

Ownership claims should fit the existing alignment outcomes. No new outcomes are needed.

```text
supported
missing_support
not_evaluable
potential_conflict
```

Possible ownership interpretations:

| Outcome | Ownership interpretation |
| --- | --- |
| `supported` | The ownership claim is recognized, the supplied evidence satisfies the ownership rule's support conditions, and competing-owner evaluation under the rule does not undermine the claim. This is still not an absolute truth value. |
| `missing_support` | The ownership claim is recognized, the rule knows what ownership support requires, and the supplied evidence does not meet those requirements. |
| `not_evaluable` | The claim may be ownership-like, but current rules do not know how to evaluate the claim, evidence classes, scope, or candidate owner set. |
| `potential_conflict` | Supplied evidence suggests a competing owner, bypass, inconsistent scope, rejected-owner contradiction, or artifact that may undermine the ownership claim. |

A future ownership rule should be conservative. Broad ownership claims should often be `not_evaluable` unless their scope and evidence requirements are explicit. Recognized ownership claims with only artifact or behavior evidence should usually be `missing_support`, not `supported`, if the rule expects stronger evidence.

## 14. Ownership Failure Modes

Ownership reconciliation should preserve guardrails against common inference errors.

| Failure mode | Why it is unsafe | Guardrail |
| --- | --- | --- |
| Inferring ownership from behavior | Behavior shows participation, not authority. | Require explicit responsibility, scope, and competing-owner evidence. |
| Inferring ownership from boundaries | Boundary shows constraint or separation, not accountability. | Require evidence that the boundary component is the authoritative holder, not only the gate. |
| Inferring ownership from call sites | Call sites can be delegation, helpers, tests, fallback paths, or implementation details. | Treat call sites as relationship evidence only. |
| Inferring ownership from containment | A method or field contained in a class does not prove the class owns the broader concern. | Treat containment as structure evidence only. |
| Inferring ownership from documentation alone | Documentation claims can express intended ownership but are not self-proving. | Pair documentation with repository, relationship, constraint, invariant, policy, or competing-owner evidence. |
| Inferring ownership from artifact names | A name such as `Executor`, `Store`, or `Composer` may indicate intent but does not prove authority. | Use names as candidate discovery only. |
| Inferring ownership from absence alone | Missing alternatives in supplied evidence may reflect incomplete acquisition. | Scope absence findings and pair them with positive evidence. |
| Inferring broad ownership from narrow tests | Tests may cover one path, fixture, or mocked interaction. | Keep claim scope no broader than exercised evidence. |

## 15. Acquisition Impact

Ownership reconciliation likely requires richer acquisition than the current artifact-only spine.

Candidate evidence classes:

```text
ArtifactFact
RelationshipFact
ConstraintFact
InvariantFact
PolicyFact
```

Ownership likely also requires analysis concepts such as:

```text
OwnerCandidate analysis
CompetingOwner analysis
```

Potential acquisition implications:

- `ArtifactFact` identifies candidate owners and relevant artifacts.
- `RelationshipFact` identifies participation, delegation, calls, routing, storage, emission, validation, and composition.
- `ConstraintFact` identifies required, prohibited, or exclusive paths.
- `InvariantFact` identifies rules a component must preserve.
- `PolicyFact` identifies intended authority, allowed actions, and decision responsibility.
- `OwnerCandidate analysis` identifies possible owners under the claim scope.
- `CompetingOwner analysis` evaluates whether alternatives are absent, rejected, delegated, subordinate, or differently scoped.

This document does not recommend implementation. It only records that ownership support likely cannot be responsibly evaluated with `RepositoryArtifactFact` alone and probably cannot be reduced to relationship evidence alone.

## 16. Non-Goals

This reconciliation explicitly rejects:

```text
ownership implementation
Runtime integration
repository scanning expansion
LLM semantic reasoning
automatic architecture inference
code changes
test changes
```

It also rejects changing:

```text
Repository Observation
Documentation Observation
Runtime
ToolExecutor
EventLedger
ProjectionStore
reconciliation behavior
```

## Questions Answered

### Is ownership fundamentally different from all lower layers?

Yes.

Ownership is fundamentally different because it is an architectural responsibility and authority judgment. Lower layers ask narrower questions:

```text
Does X exist?
How is X arranged?
Does X participate in Y?
Is Y constrained to or separated by X?
```

Ownership asks:

```text
Is X the authoritative responsibility holder for Y under this scope?
```

That question depends on lower-layer evidence but is not reducible to any of it. The ownership claim can be false, too broad, or not evaluable even when the candidate owner exists, performs the behavior, and sits at the relevant boundary.

### Can ownership ever be supported by a single evidence class?

Usually no.

A very narrow future rule could define a special case where one evidence class is treated as sufficient under an explicit deterministic rule. However, as an architectural principle, ownership should not normally be supported by a single evidence class because it combines existence, participation, constraint, responsibility, authority, scope, and competing alternatives.

The safe default is:

```text
ArtifactFact alone is insufficient.
RelationshipFact alone is insufficient.
ConstraintFact / InvariantFact / PolicyFact alone is insufficient.
Ownership support likely emerges from converging evidence plus competing-owner evaluation.
```

## Recommended Architectural Conclusion

Ownership is an architectural judgment, not a lower-layer observation.

Seed should treat ownership as the highest current evidence layer because it requires a component to be established not merely as present, structured, active, or bounded, but as accountable and authoritative for a scoped concern.

The recommended architectural conclusion is:

```text
Ownership claims should remain conservatively evaluated.
They should require explicit scope, multiple converging evidence classes,
and competing-owner analysis before being considered supported.
```

This conclusion preserves the distinction between what Seed can observe and what Seed can responsibly claim about its own architecture.
