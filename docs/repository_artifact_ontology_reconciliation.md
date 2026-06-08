# Repository Artifact Ontology Reconciliation

## 1. Purpose

This document reconciles the ontology question that follows from the Repository Observation language-boundary finding:

```text
Repository Observation
        ↓
RepositoryArtifactFact
```

The previous boundary finding established that Repository Observation is a language-neutral acquisition concern and that Python AST extraction is only the first adapter. The remaining architectural question is narrower:

```text
What repository concepts are stable enough to be architecture vocabulary,
and which concepts should remain adapter vocabulary?
```

This matters because Structure Reconciliation depends on `RepositoryArtifactFact` records to evaluate static relationships. If the artifact vocabulary is mistaken for a universal ontology too early, Structure Reconciliation may accidentally reason over Python-shaped concepts rather than over evidence-backed repository structure. If the vocabulary is treated as a meaningless transport payload, however, reconciliation loses a stable boundary for existence, structure, and dependency claims.

This document is documentation-only. It does not modify production code, tests, Repository Observation behavior, Runtime, ToolExecutor, EventLedger, ProjectionStore, reconciliation behavior, package exports, or local CLI behavior.

## Files Inspected

Required context inspected for this reconciliation:

- `docs/repository_observation_language_boundary.md`
- `docs/structure_claim_reconciliation.md`
- `docs/existence_claim_reconciliation.md`
- `docs/repository_reconciliation_v1_frontier.md`
- `docs/self_model_and_alignment_architecture_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

## 2. Central Finding

`RepositoryArtifactFact` is more than a raw transport object for arbitrary adapter output, but it should not yet be treated as a fully normalized language-neutral ontology.

The two possible interpretations are:

| Interpretation | Strength | Risk |
| --- | --- | --- |
| `RepositoryArtifactFact` as a language-neutral ontology | Gives Structure Reconciliation stable concepts to reason over and prevents Python AST details from leaking downstream. | Overstates the maturity of the current vocabulary and may force non-Python adapters into Python-shaped terms. |
| `RepositoryArtifactFact` as a transport object for adapter output | Preserves adapter flexibility and allows each language to emit its native terms. | Makes downstream reconciliation depend on unstable strings without a clear architectural meaning. |

The recommended interpretation is a middle position:

```text
RepositoryArtifactFact is the stable architectural boundary.
Current artifact kinds are acceptable adapter vocabulary.
The durable ontology is the relationship layer: artifacts, definitions,
containment, and dependencies.
```

In other words, `RepositoryArtifactFact` should remain the record that crosses from Repository Observation into reconciliation. Its current `artifact_kind` values may include Python-friendly terms such as `class`, `method`, `function`, and `import`, but architecture should treat those values as adapter-emitted labels unless and until a normalized ontology is explicitly introduced.

This preserves the important boundary:

```text
Language adapter vocabulary
        ↓
RepositoryArtifactFact boundary
        ↓
Structure / Existence Reconciliation over evidence-backed facts
```

## 3. Current Vocabulary Review

The current vocabulary contains useful terms, but those terms are not equally language-neutral.

| Term | Assessment | Why |
| --- | --- | --- |
| `module` | Mixed | Many languages have module-like compilation, packaging, or namespace concepts, but the boundaries differ. Python modules are often files; Go has packages and modules; Java has packages and optional modules; C has translation units and headers; Rust has crates and modules; TypeScript has files, ECMAScript modules, namespaces, and packages. |
| `class` | Adapter-specific / partially shared | Natural in Python, Java, and TypeScript, but not universal. C has `struct` and function patterns rather than classes. Rust has structs, enums, traits, and impl blocks. Go has structs, interfaces, and methods without classes. |
| `function` | Mostly language-neutral | Function-like definitions exist in Python, Go, Rust, C, and TypeScript. Java mostly exposes functions as methods or constructors inside classes. The neutral concept is closer to `callable_definition` than to the exact word `function`. |
| `method` | Mixed | Methods appear in Python, Go, Rust, Java, and TypeScript, but the attachment model differs. Python, Java, and TypeScript methods are commonly class members; Go methods are associated by receiver; Rust methods often appear in `impl` blocks. The neutral concept is a callable definition with containment or receiver/type association. |
| `import` | Mixed | Python, Go, Java, and TypeScript have imports, while C has preprocessor includes and Rust has `use`, `extern crate`, crate dependencies, and module declarations. The neutral concept is dependency or name-availability edge, not necessarily the spelling `import`. |

Conclusion:

```text
The current vocabulary is acceptable as adapter vocabulary.
It should not be frozen as the complete repository ontology.
```

## 4. Cross-Language Comparison

### Python

Python maps naturally to the current vocabulary:

```text
module
class
function
method
import
```

A Python adapter can directly observe lexical containment for a method inside a class body. For example, a method fact may carry `parent_symbol="Runtime"` when the AST shows that the method is declared inside `class Runtime`.

### Go

Go commonly exposes:

```text
package
file
type
struct
interface
function
method
import
```

Go has methods, but methods are not lexically nested inside a type. They are associated with a receiver. A Go adapter could emit `artifact_kind="method"` and `parent_symbol="Server"` only if the receiver provides direct structural evidence for that association.

### Rust

Rust commonly exposes:

```text
crate
module
struct
enum
trait
impl
function
method
field
use
```

Rust methods are often declared inside `impl` blocks rather than inside the type definition itself. Traits define required or default callable signatures. A Rust adapter may need to distinguish type definitions, trait definitions, impl blocks, associated functions, and methods even if downstream reconciliation only consumes neutral definition, containment, implementation, and dependency relationships.

### C

C commonly exposes:

```text
translation unit
header
function
struct
union
enum
typedef
field
macro
include
```

C has no native class or method concept. A C adapter should not be required to emit `class` to satisfy the architecture. It may emit `struct`, `function`, `field`, `macro`, and `include`, while a future normalized layer could map some of those into `type_definition`, `callable_definition`, `field`, and `dependency` concepts.

### Java

Java commonly exposes:

```text
package
class
interface
enum
record
method
field
constructor
import
module
```

Java maps well to class, method, interface, field, and import vocabulary, but its top-level callable model differs from languages with free functions. Architecture should not make top-level `function` a required universal category.

### TypeScript

TypeScript commonly exposes:

```text
module
namespace
class
interface
type
function
method
field
import
export
```

TypeScript combines JavaScript runtime constructs with static type-only constructs. Some definitions exist only at type-checking time. A TypeScript adapter may need to preserve whether a symbol is a runtime artifact, a type artifact, or both. That distinction is adapter-specific until a concrete cross-language need justifies a normalized runtime/type ontology.

### Shared Concepts vs Language-Specific Concepts

Shared repository concepts include:

- artifact identity;
- file or source location;
- definition of a named thing;
- containment or structural association;
- dependency or reference to another source/module/package/header/crate;
- type-like definition;
- callable-like definition;
- field/member-like declaration;
- interface/protocol/contract-like declaration;
- implementation or conformance relationship.

Language-specific or language-shaped concepts include:

- Python `module` as a source file;
- Java `class` and package/module rules;
- Go receiver methods and package boundaries;
- Rust `trait`, `impl`, crate/module, and `use` distinctions;
- C `include`, macro, translation unit, and header conventions;
- TypeScript type-only aliases, interfaces, namespaces, imports, and exports.

The stable ontology is therefore not the exact spelling of each language construct. The stable ontology is the smaller set of observable repository relationships that many language constructs can instantiate.

## 5. Candidate Neutral Ontology

The following concepts are candidates for a future neutral ontology. This section evaluates them only; it does not require implementation changes.

| Candidate concept | Evaluation |
| --- | --- |
| `artifact` | Strong neutral concept. A repository artifact is an observed source-level thing with a kind, symbol, path, and evidence boundary. |
| `definition` | Strong neutral concept. Many languages define named things even when the kinds differ. |
| `containment` | Strong neutral relationship. A source artifact may be inside, declared under, owned by syntax, or directly associated with another artifact. This must remain evidence-backed and must not imply behavioral ownership. |
| `dependency` | Strong neutral relationship. Imports, includes, `use` statements, package references, and some manifest dependencies can all express dependency or name-availability edges. |
| `implementation` | Useful but more specialized. Java class implements interface, Rust type implements trait, Go type satisfies interface, and TypeScript class implements interface are related but not identical. This should wait for a concrete cross-language use case. |
| `field` | Mostly neutral as member data or declared attribute, but exact semantics vary across classes, structs, records, interfaces, and type-only declarations. |
| `interface` | Mixed. Java, Go, and TypeScript use the word, while Rust uses traits and Python uses protocols/ABCs/conventions. Neutral concept may be `interface_like_definition` or `protocol`. |
| `protocol` | Useful as a broad contract concept, but potentially too semantic unless backed by explicit language constructs such as Python `Protocol`, Rust traits, or Go interfaces. |
| `module_boundary` | Useful neutral concept for source/package visibility or grouping boundaries, but language mappings differ sharply. It should not replace adapter vocabulary without a real need. |
| `type_definition` | Strong candidate. Classes, structs, enums, records, aliases, interfaces, and traits may all be type definitions or type-like definitions, though runtime/type distinctions matter. |
| `callable_definition` | Strong candidate. Functions, methods, constructors, associated functions, and closures assigned to names may all be callable-like definitions depending on adapter evidence. |

A cautious future neutral layer could therefore start with:

```text
artifact
definition
containment
dependency
type_definition
callable_definition
```

More semantic concepts such as `implementation`, `interface`, and `protocol` should remain candidates rather than commitments until a concrete cross-language reconciliation question requires them.

## 6. Relationship To Existing Artifact Facts

Existing facts such as:

```text
artifact_kind="class"
artifact_kind="method"
artifact_kind="function"
```

should remain acceptable for now.

Reasons:

- they are already useful for Python repository observation;
- they support the current existence and structure claim frontier;
- replacing them would risk a schema or behavior change without a proven need;
- the architecture already has a stable downstream boundary in `RepositoryArtifactFact`;
- adapter vocabulary can coexist with later normalized concepts;
- premature normalization could erase useful source-language detail.

The important distinction is:

```text
Accepting adapter vocabulary is not the same as declaring it universal.
```

Therefore, no implementation change is recommended here. The current artifact kinds should remain valid evidence labels. Future documentation or implementation may add normalized concepts beside them only if cross-language use makes that necessary.

## 7. Containment Finding

`parent_symbol` should be interpreted as language-neutral containment or structural-association metadata, not merely Python method ownership.

For Python, `parent_symbol` may represent direct lexical containment:

```text
class Runtime:
    def handle_user_message(...): ...
```

For Go, a comparable relationship may come from receiver syntax:

```text
func (s *Server) ServeHTTP(...) { ... }
```

For Rust, a comparable relationship may come from an `impl` block:

```text
impl Server {
    fn serve_http(...) { ... }
}
```

The neutral meaning should be:

```text
The adapter has direct structural evidence that this artifact is contained by,
declared under, or structurally associated with the named parent artifact.
```

It should not mean:

```text
The parent owns behavior.
The parent owns architectural responsibility.
The adapter inferred ownership from naming similarity.
The runtime route is controlled by this symbol.
```

Conclusion:

```text
parent_symbol is acceptable language-neutral containment metadata.
It is not Python-only ontology, provided adapters emit it only from direct evidence.
```

## 8. Structure Reconciliation Impact

Structure Reconciliation should reason primarily over neutral relationships:

```text
definition
containment
dependency
```

It may use adapter vocabulary such as:

```text
class
method
function
import
```

as evidence labels, but it should avoid making those labels the whole ontology.

For example, the claim:

```text
Runtime defines method handle_user_message.
```

can currently be evaluated using facts shaped like:

```text
artifact_kind="class", symbol="Runtime"
artifact_kind="method", symbol="handle_user_message", parent_symbol="Runtime"
```

Architecturally, however, the stable reasoning pattern is:

```text
A definition named Runtime exists.
A callable definition named handle_user_message exists.
The callable definition is contained by or structurally associated with Runtime.
```

Recommendation:

```text
Structure Reconciliation should reason over definitions,
containment, and dependency relationships first.
It may use class/method/function/import terms as current adapter evidence,
but should not treat Python vocabulary as the universal structure ontology.
```

This preserves the evidence ladder from existence to structure: same-path existence is not enough to prove method containment, and containment evidence is not enough to prove behavioral ownership.

## 9. Future Evolution

This document evaluates future paths but does not recommend implementation.

### Option A: Keep RepositoryArtifactFact vocabulary as-is

Pros:

- simplest path;
- no schema churn;
- preserves current Python adapter behavior;
- keeps documentation aligned with current implementation;
- avoids speculative abstractions.

Cons:

- downstream rules may slowly couple to Python-shaped labels;
- non-Python adapters may need awkward mappings;
- cross-language comparisons may remain ad hoc.

### Option B: Introduce normalized ontology concepts later

Pros:

- gives Structure Reconciliation more stable concepts;
- allows `class`, `struct`, `trait`, and `interface` to map into broader concepts such as `type_definition`;
- allows `import`, `include`, and `use` to map into broader `dependency` relationships.

Cons:

- requires design, schema, migration, and tests;
- risks losing adapter detail if normalization replaces rather than supplements source terms;
- may be premature before real multi-language observation exists.

### Option C: Store both adapter vocabulary and normalized concepts

Pros:

- preserves source-language precision;
- gives reconciliation neutral concepts when needed;
- allows gradual adoption;
- avoids forcing all adapters into Python terms.

Cons:

- more complex records;
- requires clear precedence rules;
- introduces risk of disagreement between adapter kind and normalized kind;
- not justified until there is a concrete cross-language consumer.

Likely direction:

```text
Keep the current vocabulary now.
Allow future normalized concepts beside adapter vocabulary if a real
cross-language reconciliation need appears.
Do not introduce a normalized ontology speculatively.
```

## 10. Non-Goals

This reconciliation rejects:

- rewriting `RepositoryArtifactFact`;
- implementing multi-language observation;
- constructing a repository graph;
- adding LLM semantic code understanding;
- inferring ownership;
- inferring behavior;
- changing Repository Observation behavior;
- changing Runtime;
- integrating with Runtime;
- changing ToolExecutor;
- integrating with ToolExecutor;
- changing EventLedger;
- changing ProjectionStore;
- modifying production code;
- modifying tests.

## Explicit Questions Answered

### Did recent method-containment work accidentally create a Python ontology?

No, not by itself.

The recent method-containment work used Python AST extraction to produce better structural evidence for the first adapter. That work would become a Python ontology only if architecture or reconciliation treated Python labels as universal repository concepts.

The safe interpretation is:

```text
method is acceptable adapter vocabulary.
parent_symbol is language-neutral containment metadata.
RepositoryArtifactFact remains the stable boundary.
```

### What architectural guardrail prevents that?

The guardrail is:

```text
Repository Observation remains language-neutral acquisition.
Language adapters may emit language-specific artifact kinds.
RepositoryArtifactFact remains the stable downstream boundary.
Structure Reconciliation should reason primarily over definitions,
containment, and dependencies, not over Python syntax itself.
```

Additional guardrails:

- do not require non-Python adapters to emit Python terms;
- do not infer ownership or behavior from `parent_symbol`;
- do not move parsing into reconciliation;
- do not treat `artifact_kind` as a closed universal enum unless a future normalized ontology explicitly defines it;
- preserve adapter vocabulary when it is useful evidence;
- introduce normalized concepts only when a concrete cross-language need appears.

## Final Finding

RepositoryArtifactFact remains the stable architectural boundary between Repository Observation and downstream reconciliation.

Current artifact kinds such as `class`, `method`, `function`, `module`, and `import` remain acceptable adapter vocabulary. They are useful and should not be removed merely because they are not universal.

The stable repository ontology should currently be understood at the relationship level:

```text
artifact
definition
containment
dependency
```

Potential future normalized concepts such as `type_definition`, `callable_definition`, `field`, `interface`, `protocol`, `implementation`, and `module_boundary` may be useful later, but should not be introduced until real cross-language observation or reconciliation needs make them necessary.

Structure Reconciliation should therefore reason primarily about evidence-backed definitions, containment, and dependency relationships, while allowing current adapter vocabulary to remain the concrete evidence emitted by Repository Observation.

## Documentation-Only Status

This is architecture research only.

It changes documentation only.

It does not change production code.

It does not change tests.

It does not change Repository Observation behavior.

It does not change Runtime.

It does not change ToolExecutor.

It does not change EventLedger.

It does not change ProjectionStore.
