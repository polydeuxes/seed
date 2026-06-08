# Behavior Claim Reconciliation

## 1. Purpose

This document reconciles the behavioral evidence boundary in Seed's self-model evidence ladder.

It is documentation-only architecture research. It does not modify production code, tests, Runtime, Repository Observation, Documentation Observation, ToolExecutor, EventLedger, ProjectionStore, repository scanning, reconciliation behavior, acquisition behavior, or package exports.

The current documented ladder is:

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

Previous reconciliation documents established these lower layers:

- Existence asks whether named artifacts exist or whether one artifact co-occurs with another under the narrow existence rule.
- Structure asks whether artifacts are arranged in a static repository shape, such as method containment.
- Repository Observation supplies `RepositoryArtifactFact` records as bounded artifact facts, not full semantic or runtime facts.
- Documentation Observation supplies claims, not proof that those claims are true.
- Alignment outcomes describe support under known rules, not global truth.

Behavior reconciliation exists because a gap remains between static structure and architectural ownership:

```text
X exists.
X defines method Y.
X participates in action Z.
X owns responsibility Z.
```

Those statements are not equivalent. A class may exist without participating in any action. A method may be declared without being used in the claimed flow. A component may participate in a behavior without owning that behavior. Behavior reconciliation defines the evidence boundary for the middle statement: when Seed may say a component participates in a runtime-relevant action, flow, operation, route, state transition, or emitted effect.

Behavior connects to the adjacent layers as follows:

| Layer | Question | Relationship to behavior |
| --- | --- | --- |
| Existence | Does `X` exist? Does `X` define `Y` under a narrow existence rule? | Existence can name candidate participants, but it does not show participation in an action. |
| Structure | Does `X` contain, import, declare, or statically relate to `Y`? | Structure can show possible affordances, but it does not show that those affordances are invoked or operationally relevant. |
| Behavior | Does `X` participate in action, flow, operation, routing, state transition, validation, recording, emission, or storage? | Behavior requires relationship-oriented evidence, not merely symbol or containment evidence. |
| Boundary | Is a responsibility edge preserved by tests, invariants, contracts, or architecture metadata? | Boundary evidence can constrain behavior, but behavior alone does not prove a preserved boundary. |
| Ownership | Does `X` architecturally own responsibility `Z`? | Ownership sits above behavior and requires stronger guardrails, including behavior plus responsibility, exclusivity or authority evidence, and absence of competing owners under an explicit scope. |

The motivating question is:

```text
What evidence is sufficient to support a behavior claim,
and how is that different from existence, structure, boundary, and ownership?
```

## 2. Central Finding

A behavior claim asserts that a component participates in a runtime-relevant action, flow, state transition, routing path, validation step, recording step, emitted effect, storage operation, or operation execution.

Examples of behavior-claim verbs include:

```text
calls
routes to
records
stores
emits
validates
executes
handles
composes
returns
mutates
selects
loads
persists
```

The central finding is:

```text
Structure proves containment or static arrangement.
Behavior requires relationship evidence.
```

A behavior claim is stronger than these statements:

```text
Runtime exists.
Runtime defines method handle_user_message.
Runtime imports ToolExecutor.
```

It is weaker than this statement:

```text
Runtime owns all user-message intake and decision routing.
```

Behavior evidence should normally show an operational relationship, such as a call, route, state mutation, event append, handler registration, or integration-level execution path. It should not be inferred from names, same-path evidence, method existence, imports, documentation prose alone, or LLM semantic reasoning.

## 3. Examples Of Behavior Claims

The following examples illustrate how similar sentences can belong to different layers or combine several layers.

| Claim | Classification | Reason |
| --- | --- | --- |
| `Runtime routes call_tool decisions to ToolExecutor.` | Behavior, with boundary implications | The verb `routes` asserts a runtime-relevant flow from `Runtime` to `ToolExecutor`. It may also imply a boundary if it claims that `Runtime` decides while `ToolExecutor` executes, but routing participation itself is behavioral. |
| `Runtime handles user messages.` | Behavior, possibly broad | The verb `handles` asserts participation in a runtime flow. It is broad because handling might include receiving input, composing context, invoking decisions, routing tools, recording events, and returning envelopes. Narrower behavior claims would be easier to evaluate. |
| `ProjectionStore stores projection snapshots.` | Behavior, and possibly structure depending on wording | `stores` asserts an operation that changes or persists projection state. If the claim only said `ProjectionStore defines get_snapshot`, it would be structure. If it said `ProjectionStore owns snapshot storage`, it would be ownership. |
| `ContextComposer composes decision context.` | Behavior | `composes` asserts an operation over inputs into a decision context. It may need call-site, return-value, or integration evidence showing actual composition behavior. |
| `ToolExecutor executes registered operations.` | Behavior | `executes` asserts runtime operation execution. This does not by itself assert that ToolExecutor owns all execution responsibility. |
| `Runtime validates decisions before routing.` | Behavior, with boundary implications | `validates` and `routing` assert ordered operational participation. The phrase `before routing` adds sequence requirements that need stronger evidence than a single method definition. |
| `Runtime defines method handle_user_message.` | Structure | This says a method is contained in or associated with `Runtime`; it does not prove the method is called or what it does. |
| `ToolExecutor owns operation execution.` | Ownership | This asserts architectural authority over responsibility, not merely participation in execution. It requires stronger guardrails than behavior. |
| `Runtime is the boundary between user input and decision execution.` | Boundary | This asserts a responsibility edge or separation, not merely a runtime action. It may need tests, invariants, or architecture metadata. |

Mixtures should be decomposed before reconciliation. For example:

```text
Runtime validates decisions before routing them to ToolExecutor, which owns operation execution.
```

contains at least three claims:

1. `Runtime validates decisions.` — behavior.
2. `Runtime routes decisions to ToolExecutor.` — behavior.
3. `ToolExecutor owns operation execution.` — ownership.

## 4. Behavior vs Structure

The distinction between structure and behavior is critical.

```text
Runtime defines method handle_user_message.
```

is a structure claim. It asserts that `handle_user_message` is a method of `Runtime` under supplied structural artifact facts.

```text
Runtime handles user messages.
```

is a behavior claim. It asserts that `Runtime` participates in the user-message flow.

Method containment is not behavior:

```text
method containment
≠
behavior
```

A method can be present but unused. A method can be called only in tests. A method can delegate all meaningful work elsewhere. A method can have a name that suggests behavior but an implementation that does something different. A method can raise `NotImplementedError`, return a constant, or be unreachable in the claimed runtime path.

Examples:

| Evidence | Supports | Does not support |
| --- | --- | --- |
| `Runtime` class exists. | `Runtime exists.` | `Runtime handles user messages.` |
| `Runtime` and `handle_user_message` appear in the same source path. | Narrow existence-level `Runtime defines handle_user_message.` under the existing same-path rule. | `Runtime defines method handle_user_message.` or `Runtime handles user messages.` |
| `handle_user_message` is a method with `parent_symbol="Runtime"`. | `Runtime defines method handle_user_message.` | `Runtime handles user messages.` |
| A call site invokes `Runtime.handle_user_message(input)` in the runtime entry path. | Candidate support for `Runtime handles user messages.` | `Runtime owns user-message intake.` |
| `handle_user_message` appends an event and returns a response envelope. | Candidate support for specific behavior claims about recording and returning. | Broad ownership of response composition or event storage. |

The evidence boundary that separates structure from behavior is the move from static containment to operational relationship:

```text
Structure evidence: X contains, declares, imports, subclasses, or associates with Y.
Behavior evidence: X calls, routes, mutates, emits, records, stores, validates, returns, or executes Y in a runtime-relevant path.
```

### Did Structure Reconciliation v1 accidentally prove behavior?

No.

Structure Reconciliation v1 did not accidentally prove behavior because its supported rule only establishes method containment:

```text
artifact_kind="class", symbol=X
artifact_kind="method", symbol=Y, parent_symbol=X
```

That evidence can support:

```text
X defines method Y.
```

It cannot support:

```text
X calls Y.
X routes to Y.
X handles inputs.
X validates decisions.
X records events.
X executes operations.
X owns responsibility Z.
```

Structure v1 therefore proves containment only. It does not inspect method bodies, call sites, event writes, state changes, return values, handler registrations, routing tables, tests, or runtime traces. Without relationship-oriented evidence, behavior remains unproven.

## 5. Candidate Behavioral Evidence

Behavior claims need evidence that links a participant to an operation. The following evidence types are candidates for future behavior reconciliation. This document evaluates them only; it does not recommend implementation.

| Evidence type | Possible support | Strengths | Weaknesses / guardrails |
| --- | --- | --- | --- |
| Direct call sites | `X calls Y.` or `X invokes Y during Z.` | Strong for invocation when caller, callee, and path are explicit. | A call site alone may be unreachable, test-only, error-only, or not part of the claimed runtime flow. Dynamic dispatch and dependency injection can obscure the real callee. |
| Explicit function invocation | `Runtime invokes ToolExecutor.execute`. | Concrete and often deterministic from source. | Still does not prove ordering, success, ownership, or complete behavior. |
| Event emission | `X emits event Y.` or `X records Y.` | Strong for behavior that leaves an event side effect. | Needs clear event API semantics. An event name in code is not enough if it is never emitted or is emitted by another component. |
| State mutation | `X stores Y.` or `X updates state Z.` | Strong for storage, projection, cache, and transition claims. | Mutation may be local, temporary, rollback-only, test-only, or incidental. Requires distinguishing durable storage from in-memory assignment. |
| Returned values | `X returns response envelope Y.` or `X returns decision context.` | Useful for output behavior and composition claims. | Return shape alone may show structure of output, not the path that produced it. It may not prove downstream use. |
| Routing tables | `X routes decision kind K to handler H.` | Strong for dispatch or routing behavior when table entries are executable and used. | A table can be declared but unused. Registration is not routing unless dispatch uses the table. |
| Registered handlers | `X registers handler H for operation K.` | Useful for operation execution, plugin, command, or event handling behavior. | Registration is often structure-plus-configuration; it does not prove execution unless paired with dispatch or integration evidence. |
| Integration tests | `Flow Z causes X to call Y / emit E / store S.` | Strong when the test exercises the claimed path end to end. | Tests are scoped examples, not complete proof. They can assert mocks rather than production behavior. Test existence is not ownership. |
| Invariants | `X must validate before routing` or `only Y may execute operations`. | Strong for boundary-preserving behavior when executable or enforced. | Documentation invariants alone are claims; executable invariants need scope and clear failure semantics. |
| Runtime traces or ledger records | `Operation Z occurred through X.` | Strong evidence for observed behavior in an execution. | Trace evidence is instance-specific and may not prove source-level general behavior unless tied to deterministic paths. |
| Error handling paths | `X rejects invalid decision Y.` | Useful for validation behavior. | Must separate intended validation from incidental exceptions. |
| Configuration or manifests | `K maps to handler H.` | Useful for registered routing. | Configuration alone may be dormant unless loaded and used. |

No single evidence type should automatically support every behavior claim. The required evidence depends on the verb:

- `calls` requires call or invocation evidence.
- `routes` requires dispatch or routing evidence.
- `records` and `emits` require side-effect evidence.
- `stores` requires mutation or persistence evidence.
- `validates` requires predicate/check evidence plus a consequence for failure or routing.
- `executes` requires invocation of an operation body or registered handler.
- `handles` should usually be decomposed into narrower verbs before evaluation.

## 6. Repository Observation Impact

Can `RepositoryArtifactFact` alone support behavior claims?

Usually no.

The current `RepositoryArtifactFact` boundary is designed around observed repository artifacts such as modules, classes, functions, methods, imports, and possible future structural metadata. Those facts can support existence and some structure claims, but behavior claims normally require relationship-oriented evidence.

For example, these artifact facts may support structure:

```text
artifact_kind="class", symbol="Runtime"
artifact_kind="method", symbol="handle_user_message", parent_symbol="Runtime"
```

They do not show:

```text
Runtime.handle_user_message is called.
Runtime.handle_user_message receives user input.
Runtime.handle_user_message mutates state.
Runtime.handle_user_message routes decisions.
Runtime.handle_user_message records events.
```

RepositoryArtifactFact alone might support behavior only if the model were explicitly extended to include relationship facts or if a future artifact kind had behavior semantics by definition. Even then, the architectural boundary should remain clear: behavior support would come from relationship-oriented facts supplied to reconciliation, not from plain symbol existence.

Therefore:

```text
RepositoryArtifactFact as currently documented is usually insufficient for behavior claims.
Behavior reconciliation likely needs future relationship-oriented evidence.
```

## 7. Documentation Observation Impact

Documentation Observation can acquire claims such as:

```text
Runtime routes decisions.
ToolExecutor executes operations.
ProjectionStore stores snapshots.
```

Those claims are not self-proving.

Documentation-only support can establish that Seed says a behavior exists. It cannot by itself establish that the repository implements or exercises that behavior. Documentation Observation asks:

```text
What does the repository say?
```

It does not ask:

```text
Is the repository correct?
Does code match the claim?
Which claim wins?
```

Behavior reconciliation should distinguish three support modes:

| Support mode | Meaning | Limit |
| --- | --- | --- |
| Documentation-only support | A behavior claim appears in documentation or architectural prose. | Supports claim existence, not code behavior. Should not become `supported` for behavior under repository reconciliation unless the rule is explicitly documentation-only. |
| Repository-only support | Relationship evidence in source or tests indicates behavior, even without documentation prose. | May support a behavior fact, but not that documentation claimed it. Does not prove ownership or intended boundary. |
| Combined support | Documentation claim and repository relationship evidence align under an explicit rule. | Best candidate for `supported` behavior claims, but still not global truth or ownership. |

A future behavior reconciliation rule should be explicit about which mode it is evaluating. If the alignment record compares a `DocumentationClaim` against supplied repository evidence, documentation prose alone should not satisfy the repository evidence requirement.

## 8. Candidate Behavioral Rules

The following possible future behavior-claim forms are evaluated only. They are not implementation recommendations.

### `X calls Y.`

Meaning:

```text
Source behavior in X includes an invocation of Y.
```

Possible evidence requirements:

- supplied call-site relationship fact;
- caller identity or enclosing scope;
- callee identity with sufficient resolution;
- source path and line/span evidence;
- exclusion of purely textual/name matches.

Weaknesses:

- dynamic dispatch may complicate callee resolution;
- calls may be unreachable or test-only;
- calls do not imply ownership.

### `X routes to Y.`

Meaning:

```text
X dispatches, directs, or forwards an input, decision, event, operation, or request to Y.
```

Possible evidence requirements:

- call-site evidence from X to Y;
- dispatch table or match/branch evidence;
- condition or decision kind being routed;
- evidence that the dispatch structure is used.

Weaknesses:

- a declared route table is not necessarily executed;
- a direct call may be delegation rather than routing;
- route ownership remains a separate question.

### `X records Y.`

Meaning:

```text
X appends, logs, persists, or otherwise records Y as an event, fact, or history entry.
```

Possible evidence requirements:

- invocation of an event ledger, repository, log, or persistence API;
- event/fact type or payload evidence;
- caller/enclosing component evidence.

Weaknesses:

- logging and architectural event recording are different;
- helper functions may obscure the actual recorder;
- recording a fact does not mean owning the ledger.

### `X stores Y.`

Meaning:

```text
X writes Y to a durable or scoped storage location.
```

Possible evidence requirements:

- state mutation or persistence call;
- storage target identity;
- payload/snapshot identity;
- durable versus in-memory semantics when relevant.

Weaknesses:

- assignment is not always storage;
- caching, projection, and persistence have different semantics;
- storage behavior does not prove storage ownership.

### `X emits Y.`

Meaning:

```text
X produces an event, signal, message, or output Y.
```

Possible evidence requirements:

- event/message construction and emission call;
- emitter identity;
- channel or sink identity;
- optional integration evidence that consumers receive it.

Weaknesses:

- constructing an event is not emitting it;
- emitting does not imply recording;
- emitting does not imply owning the event taxonomy.

### `X validates Y.`

Meaning:

```text
X checks Y against a rule and acts on success or failure.
```

Possible evidence requirements:

- predicate, guard, schema, assertion, or validator invocation;
- failure path or rejection consequence;
- ordering evidence if the claim says validation happens before another action.

Weaknesses:

- incidental exceptions are not validation;
- a validator object existing is not validation behavior;
- validation does not imply ownership of the validated domain.

## 9. Boundary Between Behavior And Ownership

This boundary is critical.

```text
ToolExecutor executes operations.
```

is a behavior claim. It says ToolExecutor participates in operation execution.

```text
ToolExecutor owns operation execution.
```

is an ownership claim. It says ToolExecutor is the architectural authority for that responsibility.

These statements need different evidence.

Behavior evidence for `ToolExecutor executes operations` might include:

- an execute method invoked by Runtime or another caller;
- dispatch to registered operation handlers;
- integration tests showing a registered operation is run through ToolExecutor;
- return values or events showing operation execution occurred.

Ownership evidence for `ToolExecutor owns operation execution` may require all or some of the following under an explicit scope:

- existence of ToolExecutor;
- structure exposing execution affordances;
- behavior showing execution occurs through ToolExecutor;
- boundary evidence showing other components route to ToolExecutor rather than executing registered operations directly;
- tests or invariants preserving that boundary;
- documentation or architecture metadata naming ToolExecutor as the responsibility owner;
- absence of competing owners within the declared acquisition scope.

The guardrails are:

1. Do not infer ownership from behavior participation.
2. Do not infer ownership from method names such as `execute`.
3. Do not infer ownership from calls into a component.
4. Do not infer exclusive authority from a single route.
5. Do not infer boundary preservation from a successful operation.
6. Keep `executes`, `routes`, `stores`, `records`, and `validates` below `owns` in the evidence ladder.
7. Require explicit ownership rules before using `supported` for ownership claims.

A component may execute operations without owning the operation domain. A component may own a responsibility while delegating some behavior. A component may participate in a behavior as caller, callee, orchestrator, adapter, store, validator, or recorder. Ownership is about responsibility authority, not just participation.

## 10. Relationship To Existing Alignment Outcomes

Behavior reconciliation should use the existing alignment outcomes only:

```text
supported
missing_support
potential_conflict
not_evaluable
```

No new outcomes are required for behavior claims.

| Outcome | Behavior-claim meaning |
| --- | --- |
| `supported` | The behavior claim pattern is recognized, and supplied evidence satisfies the rule's relationship requirements. |
| `missing_support` | The behavior claim pattern is recognized, the rule knows what evidence is required, and the supplied evidence does not contain it. |
| `not_evaluable` | The claim does not match a supported behavior pattern, or the supplied evidence lacks the evidence type needed to evaluate that pattern. |
| `potential_conflict` | The behavior claim pattern is recognized and supplied evidence suggests a competing behavior, incompatible route, opposite ordering, different actor, or other conflict under an explicit rule. |

Important guardrail:

```text
not_evaluable
```

should remain the default for broad or ambiguous behavior prose until a rule knows how to evaluate it. For example:

```text
Runtime handles everything.
```

should not become `missing_support` merely because no call-site fact exists. It is too broad unless decomposed into explicit behavior forms.

## 11. Future Acquisition Needs

Future behavior reconciliation would likely require evidence beyond current artifact facts. Candidate future acquisition needs include:

| Candidate acquisition | What it could provide | Why it may matter |
| --- | --- | --- |
| Call-site extraction | Caller/callee relationship facts, source spans, enclosing scopes. | Supports `X calls Y`, invocation parts of `X routes to Y`, and some execution claims. |
| Relationship facts | Normalized records for calls, routes, registrations, handler mappings, reads, writes, emits, and returns. | Moves reconciliation beyond artifact existence and containment. |
| Event facts | Event construction, emission, append, ledger recording, payload type, event sink. | Supports `X emits Y` and `X records Y`. |
| State-transition facts | Mutated state, before/after fields, storage target, persistence calls. | Supports `X stores Y`, `X updates Y`, and transition claims. |
| Routing or dispatch facts | Branch conditions, decision kinds, routing tables, handler maps, dispatch calls. | Supports `X routes K to Y`. |
| Registration facts | Operation name, handler, registry owner, registration site. | Supports handler availability, but should be paired with dispatch evidence for execution. |
| Return-value facts | Returned object/value categories and enclosing behavior. | Supports output and composition claims. |
| Integration-test behavior facts | Test-exercised paths, mocks, assertions, expected side effects. | Supports scoped behavior examples and boundary-preserving checks. |
| Invariant facts | Executable or documented constraints over behavior. | Supports boundary-adjacent behavior such as validation-before-routing. |

This document does not recommend implementation yet. It only identifies that behavior reconciliation probably requires relationship-oriented acquisition if Seed later chooses to evaluate behavior claims deterministically.

## 12. Non-Goals

Behavior reconciliation must reject the following as non-goals:

- ownership inference;
- behavior inference from symbol existence;
- behavior inference from method containment alone;
- behavior inference from same-path evidence;
- behavior inference from imports alone;
- behavior inference from naming similarity;
- LLM semantic reasoning as proof;
- broad repository scanning expansion;
- Runtime integration;
- ToolExecutor integration;
- EventLedger integration;
- ProjectionStore integration;
- call graph implementation;
- automatic architecture inference;
- production code changes;
- test changes;
- package export changes;
- changing Repository Observation;
- changing Documentation Observation.

## Explicit Answers

### What counts as behavioral evidence?

Behavioral evidence is relationship-oriented evidence that connects a component to an operation or flow, such as a call, route, emission, event record, state mutation, storage operation, validation check, returned value, registered handler being dispatched, or integration-tested path.

### What evidence is insufficient?

The following are insufficient by themselves:

- `X` exists;
- `Y` exists;
- `X` and `Y` appear in the same source path;
- `X` defines method `Y`;
- `X` imports `Y`;
- documentation says `X` performs behavior `Z`;
- a handler is registered but no dispatch evidence exists;
- an event type exists but no emission or record evidence exists;
- an operation name appears in code;
- an LLM judges the names semantically related.

### Did Structure Reconciliation v1 accidentally prove behavior?

No. Structure Reconciliation v1 proves containment for the explicit structure form `X defines method Y.` It does not prove calls, routing, mutation, emission, recording, storage, validation, execution, or runtime participation.

### What evidence boundary separates structure from behavior?

The boundary is operational relationship evidence.

```text
Structure: X contains/declares/imports/associates with Y.
Behavior: X invokes/routes/records/stores/emits/validates/returns/executes Y in a runtime-relevant relationship.
```

## Recommended Next Frontier

The recommended next frontier remains documentation and evidence-boundary clarification before implementation.

If behavior reconciliation becomes a future implementation candidate, the likely first architectural question should be:

```text
What is the smallest relationship fact that can be acquired deterministically
without turning Repository Observation into a call graph, runtime simulator,
or architecture inference engine?
```

A narrow future candidate might be a fixture-only relationship-fact design review for one verb such as:

```text
X calls Y.
```

But that should not be implemented until Seed explicitly decides to extend acquisition beyond artifact and structure facts. Ownership should remain above behavior, and Runtime integration should remain a non-default solution.

## Documentation-Only Status

This document is a documentation-only architectural reconciliation. It changes no production behavior, no tests, no Runtime code, no Repository Observation code, no Documentation Observation code, no ToolExecutor code, no EventLedger code, and no ProjectionStore code.
