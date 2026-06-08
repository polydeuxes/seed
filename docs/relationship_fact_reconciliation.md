# Relationship Fact Reconciliation

## 1. Purpose

This document reconciles the architectural representation needed for behavior-oriented repository evidence.

It exists because earlier reconciliation work separated Seed's self-model evidence ladder into:

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

Current acquisition distinguishes documentation claims from repository artifact facts:

```text
DocumentationClaim
RepositoryArtifactFact
```

`RepositoryArtifactFact` currently supports evidence such as:

```text
existence evidence
structure evidence
```

Examples include:

```text
class Runtime
method handle_user_message
function helper
import ToolExecutor
```

Those facts are sufficient to say that named things exist or are statically arranged. They are not, by themselves, sufficient to say that a runtime-relevant relationship occurs.

Behavior reconciliation exposed this gap. Claims such as:

```text
Runtime calls ToolExecutor.
Runtime emits UserMessageObserved.
Runtime stores ProjectionSnapshot.
Runtime validates Decision.
Runtime routes call_tool decisions.
```

are not merely claims that artifacts exist. They are claims that one artifact participates in an observed relationship with another artifact, event, state object, decision kind, or operation.

This reconciliation therefore exists to answer:

```text
Should behavior-oriented evidence be represented as RepositoryArtifactFact,
RelationshipFact, or something else?
```

It connects the evidence layers as follows:

| Layer | Primary evidence shape | Example | Boundary |
| --- | --- | --- | --- |
| Existence | Artifact fact | `ToolExecutor exists.` | Names an observed thing. |
| Structure | Artifact fact plus structural metadata or structural relationship | `Runtime defines method handle_user_message.` | Describes static repository shape. |
| Behavior | Relationship evidence | `Runtime calls ToolExecutor.` | Describes an observed connection or flow between things. |

Future acquisition will likely need to acquire both things and connections between things. This document evaluates that architecture only.

This is documentation-only architecture research. It does not modify production code, tests, Repository Observation, Documentation Observation, Runtime, ToolExecutor, EventLedger, ProjectionStore, repository scanning, reconciliation behavior, acquisition behavior, or package exports.

## 2. Central Finding

A relationship fact is an observed relationship between artifacts or between an artifact and another evidence-backed repository concept.

In compact form:

```text
Artifact facts describe things.
Relationship facts describe connections between things.
```

A relationship fact answers questions such as:

```text
What calls what?
What routes to what?
What stores what?
What emits what?
What validates what?
What imports what?
What depends on what?
What implements what?
What contains what?
```

Examples:

```text
Runtime calls ToolExecutor.
Runtime routes call_tool decisions.
Runtime emits UserMessageObserved.
Runtime stores ProjectionSnapshot.
Runtime validates Decision.
Runtime contains method handle_user_message.
Runtime imports ToolExecutor.
SQLiteProjectionStore implements ProjectionStore.
```

The central finding is:

```text
Behavior reconciliation exposed a missing acquisition primitive:
relationship evidence.
```

A distinct conceptual primitive is needed even if a future implementation chooses to encode it inside an existing record. The architectural primitive is:

```text
RelationshipFact
```

The likely direction is not that every relationship must immediately become a new production type. The finding is narrower:

```text
Behavior-oriented evidence should be modeled as relationships,
not as artifact existence alone.
```

## 3. Artifact Fact vs Relationship Fact

Artifact facts and relationship facts are fundamentally different evidence types.

An artifact fact describes an observed repository thing:

```text
ToolExecutor exists.
Runtime exists.
Runtime defines method handle_user_message.
helper exists as a function.
```

A relationship fact describes an observed edge, connection, or interaction involving one or more things:

```text
Runtime calls ToolExecutor.
Runtime routes call_tool decisions.
Runtime emits UserMessageObserved.
Runtime stores ProjectionSnapshot.
Runtime validates Decision.
ToolExecutor executes registered operations.
```

The difference is not just wording. It changes what evidence must be acquired.

| Question | Artifact fact | Relationship fact |
| --- | --- | --- |
| What is observed? | A named artifact or static artifact property. | A connection between a subject and an object. |
| Typical evidence | Definition, declaration, import symbol, parent symbol, source path. | Call site, route branch, event append, state transition, registration entry, invariant, integration path. |
| Supports | Existence and some structure claims. | Behavior claims and some structural dependency claims. |
| Insufficient for | Proving flow, execution, routing, storage, emission, validation. | Proving ownership or architectural authority by itself. |

For example:

```text
Artifact Fact:
ToolExecutor exists.
```

does not imply:

```text
Relationship Fact:
Runtime calls ToolExecutor.
```

Similarly:

```text
Artifact Fact:
Runtime defines method handle_user_message.
```

is stronger than mere existence but still does not imply:

```text
Relationship Fact:
handle_user_message routes call_tool decisions to ToolExecutor.
```

Therefore, `RepositoryArtifactFact` alone cannot reasonably support behavior reconciliation if it remains limited to artifact existence and static structure. It can name candidate participants, but behavior reconciliation needs relationship evidence to evaluate whether the participants are connected in the claimed way.

## 4. Candidate Relationship Vocabulary

The following vocabulary is a candidate evaluation only. It is not an implementation recommendation and should not be treated as a closed enum.

| Relationship kind | Evaluation | Likely layer |
| --- | --- | --- |
| `contains` | Strong structural relationship. Can represent lexical containment, receiver association, module membership, or other direct static association when evidence-backed. Must not imply behavior or ownership. | Structure |
| `calls` | Strong behavior relationship when acquired from call sites or integration traces. Static call-site evidence can support participation but may not prove dynamic execution under all conditions. | Behavior |
| `routes` | Strong behavior relationship when acquired from routing branches, dispatch tables, or decision handlers. Requires care because route labels may be domain concepts rather than artifact symbols. | Behavior |
| `stores` | Behavior relationship involving state or persistence. Stronger when tied to write operations, storage APIs, or projection updates. | Behavior |
| `emits` | Behavior relationship involving events, messages, envelopes, logs, or observations. Stronger when tied to event append or declaration sites. | Behavior |
| `validates` | Behavior relationship involving checks over inputs, decisions, invariants, or policies. Requires evidence of actual validation logic rather than naming alone. | Behavior |
| `depends_on` | Structural or build/dependency relationship. It can support possible coupling but does not prove runtime behavior. | Structure / dependency |
| `imports` | Static dependency or name-availability relationship. Useful but weaker than `calls`; importing a symbol does not prove it is used behaviorally. | Structure / dependency |
| `implements` | Structural conformance relationship when backed by language constructs or explicit metadata. It may have behavior implications but should not prove behavior by itself. | Structure / boundary candidate |
| `returns` | Behavior relationship about output shape. Static return statements may support it, but flow sensitivity and conditional paths require caution. | Behavior |
| `creates` | Behavior relationship where an artifact instantiates or constructs another artifact or value. Static construction evidence can support participation. | Behavior |
| `records` | Behavior relationship for ledger entries, observations, audit records, or durable facts. It overlaps with `emits` and `stores`; vocabulary should distinguish event creation from persistence if needed. | Behavior |
| `registers` | Structural or behavior-adjacent relationship for operation tables, handlers, tools, plugins, or callbacks. It may show availability without showing execution. | Structure / behavior-adjacent |
| `dispatches` | Behavior relationship for dynamic routing or handler invocation. Stronger than `registers` when evidence shows a selected target is invoked. | Behavior |

A careful relationship vocabulary should preserve the difference between:

```text
name availability
possible coupling
static structure
runtime-relevant behavior
architectural ownership
```

For that reason, vocabulary should start as descriptive and evidence-bound rather than normative.

## 5. Relationship Fact Shape

A hypothetical relationship fact shape could be evaluated as:

```text
subject
relationship_kind
object
source_path
evidence
```

Example:

```text
subject: Runtime
relationship_kind: calls
object: ToolExecutor
source_path: seed_runtime/runtime.py
evidence: call site or syntactic reference in handle_user_message
```

Another example:

```text
subject: Runtime
relationship_kind: emits
object: UserMessageObserved
source_path: seed_runtime/runtime.py
evidence: event append or event construction site
```

This shape has useful architectural properties:

- `subject` identifies the artifact or source concept initiating, containing, or participating in the relationship;
- `relationship_kind` identifies the observed edge type;
- `object` identifies the target artifact, state concept, event concept, decision kind, route label, or operation concept;
- `source_path` preserves the repository evidence boundary;
- `evidence` preserves why the relationship was emitted, such as a call site, import statement, routing branch, registration table, test path, or invariant.

Potential weaknesses:

- `subject` and `object` may need stable identity rules beyond display symbols;
- some relationships are ternary or contextual, such as `Runtime routes Decision(kind=call_tool) to ToolExecutor`;
- some objects are not repository artifacts, such as event names, operation names, route labels, or state concepts;
- static evidence may overstate dynamic behavior unless the evidence kind is preserved;
- relationship direction must be explicit and consistent;
- evidence should distinguish direct observation from documentation-derived assertions.

Therefore, the shape is architecturally plausible, but this document does not recommend code or schema changes. It only identifies the conceptual boundary that future design would need to preserve.

## 6. Relationship Evidence Sources

Future relationship acquisition could draw from several sources. Each source has different strength and risk.

| Evidence source | Strengths | Weaknesses |
| --- | --- | --- |
| AST relationships | Deterministic, local, source-backed, good for containment, call sites, imports, class bases, decorators, and simple construction. | Language-specific, may miss dynamic behavior, may require adapter-specific interpretation. |
| Imports | Easy to acquire and useful for dependency or name-availability relationships. | Importing does not prove calling, routing, storage, validation, or ownership. |
| Call sites | Stronger support for `calls`, `creates`, and some `dispatches` relationships. | Static call sites may be conditional, indirect, dynamically rebound, or hidden behind aliases. |
| Registration tables | Useful for handlers, tools, callbacks, routes, plugins, and operation availability. | Registration does not prove invocation; dynamic registration may be difficult to resolve. |
| Routing tables | Strong for `routes` and `dispatches` when table entries map decisions to handlers or executors. | Route labels may be strings or domain concepts rather than artifacts; table existence may not prove runtime reachability. |
| Event declarations | Useful for `emits`, `records`, and event vocabulary. | Declaration does not prove emission; event construction may not prove append or publication. |
| State transitions | Strong for `stores`, `mutates`, `records`, and projection behavior. | Requires careful state modeling and can become semantic analysis if not bounded. |
| Integration tests | Useful evidence that a relationship occurs in at least one exercised path. | Tests are partial, may use mocks, and should not be treated as exhaustive runtime proof. |
| Invariants | Useful for boundary and preservation claims around relationships. | Invariants often constrain what must be true but may not directly reveal who performs a behavior. |
| Documentation | Useful for identifying candidate relationships and expected architecture. | Documentation is a claim source, not repository proof; using it as relationship evidence risks circular support unless clearly labeled. |

The most important guardrail is:

```text
Evidence source must remain visible.
```

A relationship observed from a static call site, an integration test, a route table, and documentation prose should not collapse into the same confidence or interpretation.

## 7. Relationship Fact vs Structure

These two statements are different:

```text
Runtime contains method handle_user_message.
```

```text
Runtime calls ToolExecutor.
```

`Runtime contains method handle_user_message` is a structure statement. It describes a static arrangement in the repository: a callable definition is declared under, contained by, or structurally associated with `Runtime`.

`Runtime calls ToolExecutor` is a behavior statement. It describes an operational relationship: code associated with `Runtime` invokes, delegates to, constructs, or otherwise calls something associated with `ToolExecutor`.

The first can be supported by containment metadata such as:

```text
artifact_kind="method"
symbol="handle_user_message"
parent_symbol="Runtime"
```

The second requires relationship evidence such as:

```text
subject="Runtime"
relationship_kind="calls"
object="ToolExecutor"
evidence="call site"
```

The architectural distinction is:

```text
Structure says where things are.
Behavior says how things interact.
```

Containment can help locate the subject of behavior, but it does not prove behavior. A method can be contained by `Runtime` without calling `ToolExecutor`. `Runtime` can import `ToolExecutor` without routing decisions to it. Therefore, structure and behavior should remain separate evidence concerns even when both are acquired from source files.

## 8. Relationship Fact vs Ownership

These two statements are also different:

```text
Runtime calls ToolExecutor.
```

```text
ToolExecutor owns execution.
```

`Runtime calls ToolExecutor` is a behavior relationship. It says that one artifact participates in a call or delegation edge involving another artifact.

`ToolExecutor owns execution` is an ownership claim. It says that `ToolExecutor` has architectural responsibility or authority over execution within a defined scope.

A relationship can be evidence relevant to ownership, but it is not ownership by itself. For example:

```text
Runtime calls ToolExecutor.
```

may support a later claim that `Runtime` delegates execution, but it does not prove:

```text
ToolExecutor exclusively owns execution.
ToolExecutor is the only executor.
ToolExecutor defines the execution boundary.
Runtime does not share execution responsibility.
```

Guardrails:

- do not infer ownership from a single call relationship;
- do not infer ownership from imports, containment, naming, or route labels;
- require explicit ownership claims to remain separate from behavior facts;
- treat ownership as a higher-layer conclusion requiring behavior, boundary, authority, responsibility, and scope evidence;
- preserve the difference between participation and responsibility;
- preserve the difference between delegation and ownership;
- avoid converting relationship vocabulary into normative architecture language.

The safe interpretation is:

```text
Relationship facts can inform ownership reconciliation.
They do not determine ownership alone.
```

## 9. Acquisition Impact

Future acquisition would likely need separate concerns for:

```text
Artifact Observation
Relationship Observation
```

This does not require immediate implementation. It means the architecture should not force every repository observation into an artifact-only shape.

Artifact Observation asks:

```text
What things exist?
What definitions, declarations, modules, types, functions, methods, fields, imports, or static artifacts are present?
```

Relationship Observation asks:

```text
How are those things connected?
What calls, contains, imports, depends on, routes, stores, emits, validates, creates, records, registers, dispatches, or implements what?
```

Reasons to separate them architecturally:

- artifact extraction and relationship extraction have different evidence rules;
- relationship extraction often requires resolving subject/object identity;
- relationship extraction can be more language- and flow-sensitive;
- behavior reconciliation needs edges, not only nodes;
- separate concerns prevent existence support from being overstated as behavior support;
- separate concerns preserve the evidence ladder.

Reasons to be cautious:

- introducing a new primitive too early could create schema churn;
- relationship vocabularies can grow quickly and become inconsistent;
- static relationship evidence can be mistaken for runtime proof;
- complex relationship acquisition can drift toward semantic reasoning or call graph implementation.

The architectural impact is therefore best stated as:

```text
Future acquisition likely needs a relationship-observation concern,
but this document does not recommend implementing it now.
```

## 10. Alignment Impact

Future behavior reconciliation might consume:

```text
RelationshipFact
```

instead of relying only on:

```text
RepositoryArtifactFact
```

This would not change the meaning of alignment outcomes. It would change the evidence available to behavior reconciliation.

The existing outcome vocabulary can still apply:

| Outcome | Behavior reconciliation with relationship facts |
| --- | --- |
| `supported` | The behavior claim is recognized and supplied relationship facts satisfy the rule. Example: `Runtime routes call_tool decisions to ToolExecutor` is supported when a relationship fact shows that route. |
| `missing_support` | The behavior claim is recognized and the rule knows what relationship support should look like, but no matching relationship fact is supplied. |
| `not_evaluable` | The claim is outside current behavior rules or the relationship vocabulary is not recognized by current reconciliation. |
| `potential_conflict` | Supplied relationship facts appear to undermine the claim, such as a route to a different executor when the claim asserts a specific route. |

This preserves the established alignment guardrail:

```text
Alignment outcomes are support outcomes under known rules,
not global truth judgments.
```

Relationship facts would make behavior claims more evaluable, but they would not make reconciliation omniscient. A missing relationship fact would mean missing support under supplied evidence, not proof that the behavior never occurs. A supported relationship fact would mean support under the observed evidence, not proof that every runtime path behaves that way.

## 11. Future Evolution

This document evaluates future paths only. It does not recommend implementation.

### Option A: Everything remains RepositoryArtifactFact

In this option, relationships would be encoded as richer artifact facts or metadata on artifact facts.

Pros:

- simplest apparent schema surface;
- preserves the current named boundary;
- avoids introducing a new record type;
- may be adequate for simple structure relationships such as containment or imports.

Cons:

- blurs nodes and edges;
- risks treating behavior as artifact existence;
- makes subject/object direction harder to express;
- can overload `artifact_kind` with verbs;
- may make behavior reconciliation depend on awkward artifact encodings;
- does not clearly separate artifact observation from relationship observation.

Architectural assessment:

```text
Reasonable only for short-term simplicity or structure-only relationships.
Weak fit for behavior reconciliation.
```

### Option B: RelationshipFact becomes a distinct primitive

In this option, relationship evidence is represented by a distinct conceptual and possibly schema-level primitive.

Pros:

- cleanly separates things from connections;
- aligns with behavior reconciliation needs;
- preserves relationship direction, kind, source, and evidence;
- prevents artifact existence from masquerading as behavioral support;
- creates a natural boundary for future relationship acquisition.

Cons:

- requires vocabulary governance;
- may introduce schema, migration, export, and test work if implemented;
- could encourage premature call graph or semantic analysis;
- requires identity rules for subjects and objects;
- may be overkill before concrete behavior reconciliation rules exist.

Architectural assessment:

```text
Best conceptual fit for behavior evidence,
but should remain architecture research until a concrete implementation slice is chosen.
```

### Option C: RepositoryArtifactFact and RelationshipFact coexist

In this option, artifact facts represent observed things while relationship facts represent observed edges.

Pros:

- preserves existing artifact boundary;
- adds the missing behavior-oriented primitive without replacing artifact facts;
- supports existence, structure, and behavior with clearer evidence types;
- allows `contains` and `imports` to be represented either as structure metadata now or relationship facts later;
- supports gradual adoption.

Cons:

- requires clear rules for overlapping relationships such as `contains` and `imports`;
- requires reconciliation to consume multiple evidence streams;
- may need deduplication or precedence rules;
- may create temporary ambiguity during migration.

Architectural assessment:

```text
Likely best long-term direction:
RepositoryArtifactFact and RelationshipFact coexist.
Artifact facts describe things.
Relationship facts describe connections.
```

## 12. Non-Goals

This reconciliation rejects:

```text
behavior implementation
```

```text
call graph implementation
```

```text
repository scanning expansion
```

```text
LLM semantic reasoning
```

```text
ownership inference
```

```text
Runtime integration
```

```text
automatic architecture inference
```

It also rejects:

- modifying production code;
- modifying tests;
- changing Repository Observation;
- changing Documentation Observation;
- changing Runtime;
- changing ToolExecutor;
- changing EventLedger;
- changing ProjectionStore;
- changing reconciliation behavior;
- changing acquisition behavior;
- changing package exports.

## Explicit Questions Answered

### Did behavior reconciliation expose a missing acquisition primitive?

Yes.

Behavior reconciliation exposed that Seed can currently acquire artifacts and some static structure, but behavior claims require evidence of observed relationships between artifacts or between artifacts and repository concepts.

### If so, what is it?

The missing architectural primitive is:

```text
RelationshipFact
```

or, more generally:

```text
relationship evidence
```

The primitive represents an observed relationship such as:

```text
subject relationship_kind object
```

Examples:

```text
Runtime calls ToolExecutor.
Runtime routes call_tool decisions.
Runtime emits UserMessageObserved.
Runtime stores ProjectionSnapshot.
Runtime validates Decision.
```

### Can RepositoryArtifactFact alone reasonably support behavior reconciliation?

Not if `RepositoryArtifactFact` remains limited to existence and static structure.

`RepositoryArtifactFact` can support behavior reconciliation indirectly by naming candidate artifacts and providing static context. It can say:

```text
Runtime exists.
ToolExecutor exists.
Runtime defines method handle_user_message.
Runtime imports ToolExecutor.
```

It cannot, by itself, reasonably support:

```text
Runtime calls ToolExecutor.
Runtime routes call_tool decisions.
Runtime emits UserMessageObserved.
Runtime stores ProjectionSnapshot.
Runtime validates Decision.
```

unless it is expanded until it effectively contains relationship facts. In that case, the architecture would still need to acknowledge the relationship primitive, even if the implementation stores it inside a broadly named record.

## Recommended Architectural Direction

The recommended architectural direction is:

```text
RepositoryArtifactFact and RelationshipFact should coexist conceptually.
```

`RepositoryArtifactFact` remains the stable boundary for observed things:

```text
artifacts
definitions
declarations
static artifact metadata
```

`RelationshipFact` is the likely future primitive for observed connections:

```text
contains
calls
routes
stores
emits
validates
imports
depends_on
implements
creates
records
registers
dispatches
```

Existence primarily consumes artifact facts.

Structure consumes artifact facts and structural relationship evidence, especially containment and dependency.

Behavior likely consumes relationship facts.

Ownership remains above behavior and should not be inferred from relationships alone.

This direction preserves the evidence ladder:

```text
things
        ↓
static arrangement
        ↓
observed interaction
        ↓
preserved boundary
        ↓
architectural ownership
```

## Documentation-Only Status

This is architecture research only.

It changes documentation only.

It does not change production code.

It does not change tests.

It does not change Repository Observation.

It does not change Documentation Observation.

It does not change Runtime.

It does not change ToolExecutor.

It does not change EventLedger.

It does not change ProjectionStore.
