# Source Definitions And Entrypoint Observation Reconciliation

## Purpose

This document performs a documentation-only reconciliation of source ownership, symbol definitions, entrypoint discovery, implementation navigation, reachability, codebase observability, and source-level knowledge acquisition.

This is an architectural boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify observations, claims, projections, capabilities, authority systems, handoff behavior, ontology definitions, or tests.

It does not introduce runtime semantics.

The goal is to determine what implementation knowledge Seed requires in order to navigate, explain, audit, and reason about its own source code without collapsing distinct architectural relationships.

---

## Current Context

Current repository self-observation primarily captures a narrow structural path:

```text
file
    ↓
imports
    ↓
symbol/module
```

That path provides dependency knowledge.

Dependency knowledge is necessary, but it is insufficient for implementation navigation. It can show that one module references another module. It cannot, by itself, answer where behavior is owned, where a command is exposed, how an operator reaches a behavior, which definition implements a capability surface, or where a projected fact is produced.

Recent implementation navigation exposed questions such as:

```text
Where is Prometheus acquired?
Where is Prometheus interpreted?
Where are claims promoted?
Where are projections produced?
Where is --impact implemented?
Where is --state-build implemented?
Which capability owns this behavior?
Which file defines this symbol?
How is this code reached?
```

Those questions require source-level knowledge beyond imports.

---

## Core Finding

Seed needs multiple source relationship types because different relationships answer different implementation questions.

```text
imports
    reveal dependency knowledge

defines
    reveals ownership knowledge

entrypoints
    reveal reachability knowledge

calls / registrations / reads / writes / emits
    reveal behavior knowledge
```

No single relationship should be treated as the whole implementation model.

The source observation model should therefore preserve the following distinctions:

```text
Import != Ownership
Definition != Invocation
Entrypoint != Capability
Dependency != Reachability
Symbol != Behavior
File != Capability
```

These distinctions matter because Seed must explain implementation navigation without overstating what any single source observation proves.

---

## 1. What Is A Source Definition?

A source definition is a syntactic declaration that creates or assigns a named implementation unit inside a source artifact.

Examples include:

```text
function definition
async function definition
class definition
constant assignment
module-level variable assignment
command definition
capability definition
route handler definition
registration object definition
```

A definition has at least:

```text
source file
module path
symbol name
definition kind
line range
containing scope
```

A definition may optionally carry additional structural metadata:

```text
decorators
base classes
assigned literal value shape
signature
return annotation
argument names
containing class or function
```

A definition is not an execution. It says that a symbol is declared somewhere. It does not say that the symbol is used, reachable, correct, current, authoritative, or behaviorally important.

### Definition Versus Import

An import observes that a source file references an external module or symbol.

A definition observes that a source file declares a symbol.

```text
file imports symbol
    answers: what does this file depend on?

file defines symbol
    answers: what does this file own?
```

Import facts are dependency facts. Definition facts are ownership facts.

Importing `StateProjector` does not mean the importing file owns projection semantics. Defining `StateProjector` does not mean every projection behavior is reachable from an operator command. Those are separate relationships.

---

## 2. What Is Ownership?

Source ownership is the architectural relationship between a source artifact and the implementation unit it defines or is responsible for maintaining.

Minimal ownership examples:

```text
file
    defines
    function

file
    defines
    class

module
    defines
    constant

catalog file
    defines
    capability entry
```

Ownership means the definition's canonical source location is in that file or artifact.

Ownership does not mean:

```text
the owner executes the behavior
the owner exposes the behavior to operators
the owner is the only user of the symbol
the owner has authority to mutate runtime state
the owner is a capability
the owner is a policy authority
```

### Ownership Versus Dependency

Dependency says one source unit relies on another source unit.

Ownership says one source artifact defines a source unit.

```text
A imports B
    A depends on B

B defines Symbol
    B owns Symbol's definition
```

A dependency edge points toward something used. An ownership edge points from a file to something declared by that file.

The distinction matters because implementation navigation often starts with ownership questions:

```text
Who owns this symbol?
Where is this function defined?
Which file contains the command definition?
```

Imports cannot reliably answer those questions. They may identify many files that mention a symbol while missing the file that defines the behavior if the defining file has no import edge back to the caller.

---

## 3. What Is An Entrypoint?

An entrypoint is a source-level surface through which behavior becomes externally, operator, runtime, scheduler, framework, or test reachable.

Examples include:

```text
CLI command
CLI flag
API route
runtime registration
scheduler registration
plugin registration
tool registration
test function
fixture-driven test path
script main function
module __main__ surface
```

An entrypoint has at least:

```text
entrypoint kind
entrypoint name or selector
source file
line range
registration or declaration mechanism
initial handler or dispatch target when determinable
```

An entrypoint is not merely a definition. It is a reachable surface.

A function definition can exist without being an entrypoint. A CLI flag can be an entrypoint even when the implementation it reaches lives in a separate helper. A test function is an entrypoint into test behavior, not necessarily production behavior.

### Entrypoint Versus Definition

```text
definition
    answers: where is this symbol declared?

entrypoint
    answers: where can this behavior be entered?
```

A function named `state_summary` may define summary construction. The `--state-build` CLI flag may expose that behavior to an operator. The definition and the entrypoint should remain separate observations connected by an invocation or dispatch relationship when supported.

---

## 4. What Is Reachability?

Reachability is a supported relationship showing that behavior can be reached from an entrypoint or caller through invocation, dispatch, registration, or framework execution.

Examples:

```text
CLI flag
    invokes
    function

API route
    invokes
    handler

runtime registry
    invokes
    capability adapter

test function
    invokes
    production function

scheduler registration
    invokes
    job function
```

Reachability is not the same as imports.

An import may make a symbol available in a file, but it does not prove that an operator command invokes the symbol. Conversely, framework registration can make behavior reachable through a route, command, or scheduler without a simple local call edge that import-only observation can explain.

Reachability should be evidence-backed and conservative. A direct call is stronger than a name match. A decorator route registration is stronger than a comment. A command dispatch table is stronger than a filename convention.

---

## 5. What Implementation Questions Cannot Be Answered By Imports Alone?

Imports alone cannot answer the most important implementation navigation questions.

| Question | Why imports are insufficient | Needed relationship |
| --- | --- | --- |
| Where is behavior defined? | Many files may import or mention a symbol. The defining file may be only one of them. | `file defines symbol` |
| Where is behavior invoked? | Imports do not prove calls or dispatch. | `function calls function`, `command invokes function`, `route invokes handler` |
| How is behavior reached? | Imports do not identify CLI flags, routes, scheduler hooks, or runtime registrations. | `entrypoint invokes handler`, `registration exposes symbol` |
| Who owns this symbol? | Importers are consumers, not owners. | `file defines symbol`, `module defines symbol` |
| Which command exposes this functionality? | Command names and flags are entrypoint declarations, not dependencies. | `command/flag entrypoint declared_by file`, `entrypoint invokes function` |
| Which capability owns this behavior? | Capability ownership is a catalog or architecture relationship, not a Python import. | `capability implemented_by symbol`, `capability declared_in catalog` |
| Where are claims promoted? | Promotion is behavior performed by functions or projectors, not an import edge. | `function promotes claim`, `function emits fact`, `function writes projection` |
| Where are projections produced? | Projection creation is behavior, not module dependency. | `function produces projection`, `function writes state` |

Import observation can narrow a search space. It cannot replace ownership, entrypoint, or behavior observations.

---

## 6. What Is Behavior Knowledge?

Behavior knowledge is source-level knowledge about what implementation units do, as supported by observable source structure.

Behavior knowledge may include:

```text
function calls function
function instantiates class
function reads state
function writes state
function emits observation
function promotes claim
function produces projection
function registers entrypoint
function registers capability
function parses command flag
function dispatches command branch
function queries external source
function serializes output
function mutates ledger
function formats projection
```

Behavior knowledge differs from definition knowledge.

A definition says a function exists. Behavior knowledge says what the function does or causes, within an evidence boundary.

Behavior knowledge should be layered carefully because it is more interpretive than definitions and imports. A conservative order is:

```text
1. definitions and ownership
2. entrypoints and registrations
3. explicit invocation / dispatch edges
4. domain-specific behavior markers
5. higher-level semantic summaries
```

The first three are mostly structural. The last two require more caution because they may cross from syntax into interpretation.

---

## 7. What Should Be Observed Next?

The highest-value next source-observation layer after imports is definition and entrypoint observation, connected by conservative invocation or registration edges.

Candidate relationships:

| Relationship | Architectural value | Caution |
| --- | --- | --- |
| `file defines symbol` | Highest value for ownership and implementation lookup. | Must preserve line ranges and symbol kind. |
| `module defines symbol` | Highest value for module-level navigation. | Should not imply runtime authority. |
| `command declares flag` | High value for operator navigation. | CLI declaration is not the same as behavior implementation. |
| `entrypoint invokes function` | High value for reachability. | Only emit when direct dispatch evidence exists. |
| `function calls function` | High value for implementation navigation after entrypoints exist. | Full call graphs can be noisy and dynamic. |
| `capability implemented_by symbol` | High value for capability audit. | Requires explicit catalog/registration evidence, not name matching alone. |
| `function emits observation` | High value for observation pipeline audits. | Requires domain-specific markers. |
| `function promotes claim` | High value for claim authority audits. | Requires careful definition of promotion verbs. |
| `function produces projection` | High value for projection authority audits. | Should distinguish construction, caching, and rendering. |
| `function reads state` | Medium-high value for authority and data-flow audits. | Static reads may be ambiguous. |
| `function writes state` | High value for mutation boundary audits. | Must distinguish object construction from durable mutation. |
| `function registers route/tool/scheduler` | High value for framework reachability. | Registration mechanisms vary by framework. |

### Recommended Priority

Recommended source-observation priority:

```text
1. file defines symbol
2. source file declares entrypoint
3. entrypoint invokes or dispatches to symbol
4. module/function direct call edges
5. capability implemented_by symbol, only when explicit registration/catalog evidence exists
6. domain behavior markers: emits, promotes, produces, reads, writes
```

This order is deliberate. Ownership should precede reachability. Entrypoint observation should precede broad call-graph observation because a call graph without entrypoints can produce many edges without explaining which behavior an operator can actually reach.

---

## 8. Relationship Between Imports And Definitions

Imports and definitions are complementary but not interchangeable.

```text
imports
    provides dependency knowledge

defines
    provides ownership knowledge
```

Dependency knowledge helps answer:

```text
What modules does this file rely on?
What external names are available here?
What source units may need consideration when this file changes?
```

Ownership knowledge helps answer:

```text
Where is this symbol declared?
Which file owns this implementation unit?
What source file should I inspect to understand this behavior's definition?
```

An implementation navigator needs both.

Imports can point from consumer to dependency. Definitions can map name to owner. Together they can support navigation such as:

```text
import edge identifies a referenced module

definition edge identifies the symbol owner inside that module

entrypoint edge identifies how the owner is reached
```

---

## 9. Relationship Between Entrypoints And Implementation Navigation

Entrypoint knowledge is required to locate behavior from the perspective of an operator, runtime, external caller, or test.

A repository-wide search for a flag such as `--impact` or `--state-build` can locate parser declarations, but Seed self-knowledge should not depend on ad hoc search. A source observation layer should be able to represent:

```text
CLI flag --impact
    declared in source file
    parsed by CLI parser
    dispatches to impact view construction / rendering path

CLI flag --state-build
    declared in source file
    dispatches to state summary view construction / rendering path
```

This enables implementation navigation questions:

```text
Which source file exposes this operator surface?
Which function handles this flag?
Which read-model helper owns summary semantics?
Which renderer owns terminal output?
```

Entrypoint knowledge bridges source ownership and operator reachability.

---

## 10. What Should Not Be Collapsed Together?

### Import != Ownership

An import shows dependency. It does not prove ownership.

If `scripts/seed_local.py` imports `state_summary`, that import indicates the CLI depends on a summary helper. It does not mean the CLI owns summary semantics.

### Definition != Invocation

A function definition shows a symbol exists. It does not prove the function is called.

A function can be unused, test-only, callback-only, or reachable only through dynamic registration.

### Entrypoint != Capability

An entrypoint is a reachability surface. A capability is a declared ability or provider domain.

A CLI flag may expose a diagnostic view. A capability entry may describe a model-visible or operator-visible ability. They can be related, but neither should be collapsed into the other.

### Dependency != Reachability

A dependency edge says code can reference another module. A reachability edge says execution can flow from one surface to another.

A dependency can exist without reachability. Reachability can be mediated by registration, decorators, or configuration rather than obvious imports.

### Symbol != Behavior

A symbol is a named source unit. Behavior is what the source unit does when executed or registered.

A symbol named `build_state_summary` is not itself the whole state-summary behavior unless observations also show how it reads state, aggregates facts, and is reached.

### File != Capability

A file can define several symbols across several concerns. A capability can be implemented by multiple symbols and surfaced through multiple files.

Collapsing file and capability would obscure partial implementation, shared helpers, tests, and catalog declarations.

---

## Special Investigation: Prometheus Audit Navigation

### Observed Difficulty

The observed implementation difficulty can be summarized as:

```text
Prometheus behavior exists.
Relevant files exist.
Repository participant cannot locate implementation surfaces.
```

This is not primarily a Prometheus problem. It is an implementation navigation problem.

If Seed only knows imports, it may know that a CLI file imports observation-source helpers or that runtime modules import fact models. It still may not know:

```text
which CLI flag acquires Prometheus data
which source object wraps Prometheus filtering
which function converts Prometheus output into observations
which projection path interprets promoted facts
which view exposes impact or state summary outputs
```

### Questions And Required Source Observations

| Navigation question | Source observations that would answer it |
| --- | --- |
| Where is Prometheus acquired? | `CLI flag declares --observe-prometheus`; `flag invokes build_prometheus_observation_source`; `function instantiates PrometheusObservationSource`; `observation source queries endpoint`. |
| Where is Prometheus interpreted? | `function emits observation`; `normalizer/interpreter function reads metric labels`; `function produces fact candidates`; `predicate mapping defined_by file`. |
| Where are claims promoted? | `function promotes claim`; `function emits Fact`; `promotion rule defined_by file`; `projector applies rule`. |
| Where are projections produced? | `function produces projection`; `StateProjector.project invoked_by entrypoint`; `ProjectionStore loads/writes projection snapshot`. |
| Where is `--impact` implemented? | `CLI flag --impact declared_by file`; `flag dispatches to impact formatter/view builder`; `view helper defines impact semantics`; `renderer formats impact output`. |
| Where is `--state-build` implemented? | `CLI flag --state-build declared_by file`; `flag dispatches to state_summary / build_state_summary`; `read-model helper owns aggregation`; `CLI renderer formats terminal output`. |

### Prometheus-Specific Finding

Prometheus navigation requires at least four relationship families:

```text
entrypoint declarations
    to locate CLI acquisition surfaces

definitions / ownership
    to locate functions and classes that own acquisition, filtering, interpretation, projection, and rendering

reachability edges
    to connect flags to implementation paths

behavior markers
    to distinguish acquisition, interpretation, promotion, projection, and rendering
```

Repository-wide text search can answer these questions manually. Source-level observations should make them answerable structurally.

---

## Authority Boundaries

Source observation should remain read-only and evidence-backed.

It may support statements such as:

```text
this file defines this function
this CLI flag is declared in this file
this function directly calls this function
this capability catalog entry names this capability
this registration maps this entrypoint to this handler
```

It must not by itself assert:

```text
this behavior is correct
this behavior is canonical architecture
this behavior should be refactored
this capability is verified
this entrypoint should be executed
this code is safe to mutate
this projection is fresh
this source observation authorizes runtime behavior
```

Source observation can inform explanation and audit. It should not become execution, verification, governance, or self-modification authority.

---

## Non-Goals

This reconciliation does not require implementation work.

It does not recommend changing schemas unless a future implementation task explicitly chooses to encode these relationships.

It does not require call-graph construction now.

It does not require static type analysis, control-flow analysis, data-flow analysis, module imports, source execution, test execution, runtime introspection, LLM semantic summarization, or repository-wide indexing.

It does not change the meaning of observations, claims, projections, capabilities, authority systems, handoffs, ontology definitions, runtime behavior, or tests.

---

## Implementation Implications

If a future source-observation layer is implemented, it should be staged and conservative.

A safe future sequence would be:

```text
1. Preserve source file identity.
2. Preserve module identity.
3. Preserve symbol definitions with line ranges.
4. Preserve command / route / registration entrypoints.
5. Preserve direct dispatch from entrypoint to first handler when explicit.
6. Preserve direct call edges inside selected source roots.
7. Preserve domain behavior markers only where evidence is explicit and vocabulary is defined.
```

Each emitted relationship should carry evidence:

```text
file path
line range
extraction method
relationship kind
confidence / extraction strength
source snippet boundary or AST node kind
```

The extraction should distinguish structural observations from interpreted behavior observations.

---

## Architectural Invariants

The findings support the following architectural invariants:

```text
Imports reveal dependency.
Definitions reveal ownership.
Entrypoints reveal reachability.
Ownership is not dependency.
Reachability is not ownership.
Definition is not invocation.
Invocation is not behavior summary.
Entrypoint is not capability.
Symbol is not behavior.
File is not capability.
Implementation navigation requires more than imports.
Behavior should remain discoverable.
Source knowledge should support explainable implementation navigation.
Source observation must remain read-only and evidence-backed.
Source observation must not authorize runtime mutation or self-modification.
```

---

## Source Observation Priorities

Highest-value relationship types discovered:

```text
file defines symbol
module defines symbol
source file declares entrypoint
entrypoint invokes function
registration exposes symbol
function calls function
capability implemented_by symbol
function emits observation
function promotes claim
function produces projection
function reads state
function writes state
```

Recommended next source-observation layer after imports:

```text
definitions + entrypoints + conservative dispatch edges
```

Entrypoint observation should precede broad call-graph observation because entrypoints provide reachability anchors. A call graph without entrypoints may show many possible internal edges while failing to answer which behavior an operator, API caller, scheduler, runtime registry, or test can actually reach.

---

## Major Findings

1. Imports provide dependency knowledge, not ownership knowledge.
2. Definitions provide ownership knowledge, not invocation knowledge.
3. Entrypoints provide reachability knowledge, not capability authority.
4. Reachability differs from imports because reachability requires invocation, dispatch, registration, or framework execution evidence.
5. Implementation navigation requires ownership, reachability, and behavior knowledge in addition to dependency knowledge.
6. Behavior discovery may require additional observations such as calls, emits, reads, writes, registrations, promotions, and projection production.
7. Repository self-knowledge should preserve multiple relationship types instead of collapsing source facts into a single dependency graph.
8. Prometheus audit navigation requires entrypoint, ownership, reachability, and behavior markers to answer implementation-surface questions without repository-wide search.
9. Entrypoint observation should be prioritized before broad call-graph observation.
10. Source observation must remain read-only, evidence-backed, and non-authoritative over runtime behavior.

---

## Documents Intentionally Left Unchanged

This reconciliation intentionally leaves existing architecture, ontology, observation, claim, projection, capability, handoff, runtime, and test documents unchanged.

Representative intentionally unchanged areas include:

```text
docs/repository_observation_source_design.md
docs/repository_observation_v0_implementation_characterization.md
docs/prometheus_observation_boundary_reconciliation.md
docs/state_summary_cli_boundary_audit.md
docs/local_cli_responsibility_boundary_audit.md
docs/ontology.md
docs/invariants.md
seed_runtime/**
scripts/**
tests/**
```

