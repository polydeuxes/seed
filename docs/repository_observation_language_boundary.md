# Repository Observation Language Boundary

## Purpose

This document clarifies the architectural boundary between Repository Observation and the current Python AST extraction implementation.

It is documentation-only. It does not modify production code, tests, runtime behavior, repository observation behavior, documentation observation, reconciliation behavior, tool execution, event storage, projection behavior, package exports, or local CLI behavior.

The motivating concern is:

```text
What happens if Seed is pointed at a C repository?
A Go repository?
Rust?
Java?
TypeScript?
```

The answer should not accidentally collapse:

```text
Repository Observation
```

into:

```text
Python AST Observation
```

## Files Inspected

Required context inspected for this finding:

- `docs/repository_reconciliation_v1_frontier.md`
- `docs/existence_claim_reconciliation.md`
- `docs/structure_claim_reconciliation.md`
- `docs/self_model_and_alignment_architecture_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

Additional context inspected:

- `docs/repository_observation_frontier.md`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/knowledge/self_model_alignment.py`

## Central Finding

Repository Observation should be treated as:

```text
language-neutral acquisition
```

with:

```text
language-specific adapters
```

rather than:

```text
Python-specific architecture
```

The stable architectural concern is not Python syntax. The stable concern is acquisition of evidence-backed facts about repository artifacts.

The current implementation happens to use Python AST extraction because Seed itself is currently a Python codebase and because Python AST extraction is a small, deterministic, standard-library-safe first adapter. That implementation choice should not define the architecture.

Repository Observation remains the acquisition layer that asks:

```text
What repository artifacts exist, and what direct structural facts can be observed about them?
```

It must not become a claim that only Python repositories are observable.

## Architectural Layer Boundary

The architectural layer is:

```text
Repository Observation
        ↓
RepositoryArtifactFact
```

This layer should remain stable across languages.

`RepositoryArtifactFact` is the boundary record consumed by downstream reconciliation. Reconciliation should continue to consume supplied artifact facts rather than owning source parsing, file IO, repository traversal, language parsing, runtime routing, tool execution, event storage, or projection.

The current extraction path is better described as:

```text
Python source text
        ↓
Python AST adapter
        ↓
RepositoryArtifactFact
```

The adapter is replaceable. The artifact fact boundary is the stable architecture.

## Distinguishing Repository Observation From Python AST Extraction

Repository Observation is an acquisition capability.

Python AST extraction is one acquisition adapter.

Repository Observation may eventually have several adapters, each responsible for extracting direct, bounded, language-appropriate facts from a source representation. The adapter can use a parser, AST, token stream, manifest format, filename pattern, or other deterministic evidence source, provided it preserves the same safety boundaries.

The important distinction is:

| Concern | Architectural status |
| --- | --- |
| Repository Observation | Language-neutral acquisition layer |
| `RepositoryArtifactFact` | Stable artifact-fact boundary record |
| Python AST parsing | First language-specific adapter |
| Python vocabulary such as `class`, `method`, and `import` | Useful artifact kinds for Python, not the whole architecture |
| Reconciliation rules | Downstream consumers of supplied facts |

## RepositoryArtifactFact Vocabulary Review

Current artifact vocabulary includes:

```text
module
class
function
method
import
```

These terms are useful, but they are not equally language-neutral.

| Current term | Language-neutral status | Notes |
| --- | --- | --- |
| `module` | Partly neutral | Many ecosystems have modules or module-like compilation/package units, but C and Java may map better to file, translation unit, package, or namespace. |
| `class` | Not universal | Natural in Python, Java, TypeScript, and C++; not primary in C; Rust and Go use different type/impl constructs. |
| `function` | Mostly neutral | C, Go, Rust, Python, JavaScript, and TypeScript all have function-like definitions, though Java methods are normally class members and not top-level functions. |
| `method` | Mostly neutral structural category | Many languages have receiver/member functions or methods, but how methods attach to parents differs by language. |
| `import` | Partly neutral | Python, Go, Java, and TypeScript have imports; C has includes; Rust has `use`; build systems may express dependencies outside source syntax. |

The current vocabulary is therefore best understood as a mixed first-pass vocabulary:

```text
some language-neutral concepts
+
some Python adapter terminology
```

That is acceptable for a first adapter as long as architecture documents do not treat those terms as the complete Repository Observation ontology.

## Cross-Language Examples

### Python

Python maps naturally to the current vocabulary:

```text
module
class
function
method
import
```

`parent_symbol` can identify that `Runtime.handle_user_message` is structurally contained by `Runtime`.

### Go

Go may map to:

```text
package
file
type
function
method
import
```

Go methods are not textually nested inside a type. They are associated through receivers. A Go adapter could still emit containment or association metadata such as:

```text
artifact_kind="method"
symbol="ServeHTTP"
parent_symbol="Server"
```

but that parent relationship would come from receiver analysis, not lexical nesting.

### Rust

Rust may map to:

```text
crate
module
struct
enum
trait
impl
function
method
use
```

Rust methods often appear inside `impl` blocks rather than inside the `struct` declaration. A Rust adapter might represent both the `impl` artifact and the associated type or trait. `parent_symbol` could still name the associated type or trait when the adapter has direct evidence.

### C

C may map to:

```text
translation_unit
header
function
struct
typedef
macro
include
```

C does not have classes or methods in the Python sense. A C adapter should not be forced to invent `class` facts. It should emit language-appropriate artifact facts such as `struct`, `function`, `macro`, and `include`.

### Java

Java may map to:

```text
package
class
interface
enum
method
field
import
```

Java fits class/method vocabulary well, but package and file boundaries differ from Python module boundaries.

### TypeScript

TypeScript may map to:

```text
module
file
class
interface
type
function
method
import
export
```

TypeScript also has ambient declarations, type-only imports, exports, and structural types. A TypeScript adapter should preserve those distinctions where directly observable and useful.

## Candidate Neutral Vocabulary

Future Repository Observation may benefit from normalizing toward a small neutral vocabulary such as:

```text
artifact
definition
containment
dependency
```

This does not require implementation changes now.

A neutral vocabulary could separate general relationships from language-specific labels:

| Neutral concept | Meaning | Possible language-specific examples |
| --- | --- | --- |
| `artifact` | An observed repository object or source construct | file, module, package, class, struct, function, macro, interface |
| `definition` | A construct defined in source | Python class, Go type, Rust trait, C function, Java method |
| `containment` | A direct structural parent/child relationship or adapter-supported association | class contains method, module contains function, impl associates method with type |
| `dependency` | A direct source-level dependency declaration | Python import, C include, Rust use, Go import, Java import, TypeScript import |

This kind of neutral vocabulary would prevent the architecture from depending on any one language's syntax while still allowing adapters to preserve precise language terms in `artifact_kind` or metadata.

The near-term guardrail should be:

```text
Do not promote Python artifact names into universal architecture.
```

## Method Containment Finding

Recent Repository Observation work added:

```text
method
parent_symbol
```

This does not, by itself, overfit Repository Observation to Python.

Expected conclusion:

```text
parent_symbol is acceptable structural metadata.
```

Why:

- containment is a language-neutral structural relationship;
- many languages have parent/child or owner/member relationships between artifacts;
- the field can represent direct lexical containment where that exists;
- the field can also represent adapter-supported structural association where direct syntax supports it, such as Go receiver methods or Rust impl-associated methods;
- downstream reconciliation can use `parent_symbol` to distinguish same-path existence from actual structure;
- it preserves the evidence ladder distinction between existence and structure.

However, `parent_symbol` must be treated carefully.

It should mean:

```text
the adapter has direct structural evidence that this artifact belongs to,
is declared under, or is associated with the named parent artifact
```

It should not mean:

```text
the adapter guessed ownership from naming similarity
```

It should not imply architectural ownership, behavior, runtime routing, or semantic correctness.

## Did Method Containment Accidentally Overfit Repository Observation To Python?

No, not if the boundary is documented and maintained.

The recent method-containment work added a Python adapter capability, but the underlying fact shape is compatible with a language-neutral structural model:

```text
child artifact
        ↓
parent / containing / associated artifact
```

The risk is not the existence of `method` or `parent_symbol`.

The risk is future documentation or code treating:

```text
Python AST extraction output
```

as equivalent to:

```text
all Repository Observation output
```

That is the boundary this document exists to prevent.

## Guardrail

The architectural guardrail should be:

```text
Repository Observation is language-neutral acquisition.
Language adapters may emit language-specific artifact kinds.
RepositoryArtifactFact remains the stable downstream boundary.
No reconciliation rule may assume that the Python adapter vocabulary is the universal repository ontology unless the rule is explicitly scoped to Python-derived facts.
```

Additional guardrails:

- Keep parser behavior inside acquisition adapters.
- Keep reconciliation downstream of supplied `RepositoryArtifactFact` records.
- Treat `artifact_kind` values as adapter vocabulary unless a future normalized vocabulary explicitly defines them as universal.
- Require direct adapter evidence for containment metadata.
- Do not infer ownership, behavior, route authority, or correctness from `parent_symbol`.
- Do not require non-Python adapters to emit Python terms such as `class` or `import` when the source language has better native terms.

## Possible Future Adapter Model

A future model could look like:

```text
Source Text
        ↓
Language Adapter
        ↓
RepositoryArtifactFact
```

Examples:

### Python adapter

```text
class
method
function
import
```

### C adapter

```text
struct
function
include
macro
```

### Go adapter

```text
type
method
function
import
```

### Rust adapter

```text
struct
trait
impl
function
use
```

### Java adapter

```text
package
class
interface
method
field
import
```

### TypeScript adapter

```text
module
class
interface
type
function
method
import
export
```

The point is not to implement this now. The point is to preserve architectural flexibility so Seed can later acquire repository facts from multiple languages without rewriting reconciliation around one parser.

## Recommended Future Shape

A future `RepositoryArtifactFact` model could remain stable while adding explicit adapter/source metadata, for example:

```text
artifact_kind="method"
symbol="handle_user_message"
parent_symbol="Runtime"
path="seed_runtime/runtime.py"
adapter="python_ast"
```

or:

```text
artifact_kind="include"
symbol="stdio.h"
path="src/main.c"
adapter="c_adapter"
```

This document does not require adding those fields. It only records that adapter identity and normalized relationship vocabulary may become useful if multi-language observation becomes a real implementation goal.

## Non-Goals

This document rejects:

- rewriting Repository Observation now;
- implementing a general parser framework;
- implementing multi-language observation;
- changing Runtime;
- integrating with Runtime;
- changing ToolExecutor;
- integrating with ToolExecutor;
- changing EventLedger;
- changing ProjectionStore;
- changing Repository Observation behavior;
- changing tests;
- adding LLM code understanding;
- adding repository-wide semantic inference;
- inferring ownership from symbols, methods, containment, imports, includes, or naming.

## Final Answer To The Boundary Question

Repository Observation remains language-neutral.

Python AST extraction is simply the first adapter.

`RepositoryArtifactFact` should remain the stable architectural boundary.

`method` is acceptable as a language-specific artifact kind and as a broadly recognizable structural category.

`parent_symbol` is acceptable as language-neutral containment or structural-association metadata, provided adapters emit it only from direct evidence and downstream rules do not treat it as ownership or behavior.

The architectural guardrail is to keep language parsing in adapters and keep downstream reconciliation dependent on supplied `RepositoryArtifactFact` records rather than on Python AST concepts.

## Documentation-Only Status

This document is an architectural finding only.

It does not modify production code.

It does not modify tests.

It does not change Runtime, ToolExecutor, EventLedger, ProjectionStore, Repository Observation behavior, repository reconciliation behavior, acquisition behavior, event storage, projection behavior, package exports, or local CLI behavior.
