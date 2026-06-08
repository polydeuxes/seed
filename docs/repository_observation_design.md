# Repository Observation Design

## Purpose

This document defines the smallest safe design for Repository Observation v0.

It answers:

```text
How do repository artifacts become
Observation → Evidence → Fact → Projection
without becoming static analysis or architecture reconciliation?
```

This is documentation-only.

It does not implement repository observation.

## Design Goal

Repository Observation should be a narrow Knowledge Acquisition slice.

Its responsibility is to observe artifact structure and produce evidence-backed facts.

Desired lifecycle:

```text
Repository Artifact
        ↓
Repository Observation
        ↓
Observation
        ↓
Evidence
        ↓
Fact
        ↓
Projection
        ↓
Explanation
```

The design goal is reuse of the existing knowledge lifecycle, not creation of a new repository subsystem.

## Primary Constraint

Repository Observation must not create:

```text
RepositoryEngine
CodebaseUnderstandingEngine
StaticAnalysisEngine
ArchitectureEngine
RepositoryProjectionStore
CodeFactStore
```

It should reuse:

```text
Observation
Evidence
Fact
Projection
Explanation
```

Repository facts are ordinary projected knowledge with repository-artifact provenance.

## Ownership

Repository Observation belongs to:

```text
Knowledge Acquisition
```

It does not belong to:

```text
Runtime
ToolExecutor
ProjectionStore
Knowledge Integrity
Knowledge Selection
Response
Repository Reconciliation
```

Repository Observation acquires facts.

It does not select meaning, judge alignment, or communicate architectural conclusions.

## Source Boundary

Repository Observation v0 should operate on a local read-only repository tree or equivalent file-content snapshot.

It should not require:

```text
network calls
GitHub API calls at runtime
shell execution
source imports
test execution
type checking
language server integration
dependency installation
```

Reading file names and file contents is allowed.

Parsing source text with safe parsers is allowed.

Executing or importing source is not allowed.

## V0 Path Allowlist

For Seed itself, the first design should use an allowlist:

```text
README.md
docs/
seed_runtime/
scripts/
tests/
```

This keeps Repository Observation bounded and avoids accidental full-repository indexing.

## Exclusions

Repository Observation v0 should ignore:

```text
.git
.pytest_cache
.mypy_cache
__pycache__
venv
.venv
coverage output
build output
local database files
editor metadata
binary artifacts
```

## Observation Shape

Repository Observation should produce ordinary observations.

Example path observation:

```text
Observation
  source_type=repository
  extraction_kind=file_path
  subject=repository
  predicate=contains_path
  object=seed_runtime/runtime.py
```

Example class observation:

```text
Observation
  source_type=repository
  extraction_kind=python_ast_class
  subject=seed_runtime.runtime
  predicate=defines_class
  object=Runtime
```

Example import observation:

```text
Observation
  source_type=repository
  extraction_kind=python_ast_import
  subject=seed_runtime.runtime
  predicate=imports_module
  object=seed_runtime.events
```

These observations describe artifacts.

They do not describe architectural intent.

## Evidence Shape

Every repository observation should produce evidence.

Required evidence metadata:

```text
repository_path
file_path
line_range when available
extraction_kind
text_span or structural source
```

Examples:

```text
file_path evidence comes from directory traversal.
python_ast_class evidence comes from an AST ClassDef node.
python_ast_function evidence comes from an AST FunctionDef or AsyncFunctionDef node.
python_ast_import evidence comes from an AST Import or ImportFrom node.
```

Evidence should let explanation surfaces answer:

```text
Why does Seed believe this class exists?
```

without executing source code.

## Extraction Strategy

Repository Observation v0 should use deterministic extraction.

Priority extraction types:

```text
1. Directory entries
2. File paths
3. Filename patterns
4. Python AST module parse
5. Python AST class definitions
6. Python AST function definitions
7. Python AST import statements
8. Simple structured-file keys when safe
```

V0 should avoid:

```text
semantic summaries
LLM interpretation
control-flow analysis
data-flow analysis
type inference
call-graph construction
architecture scoring
```

## Python AST Boundary

Python AST parsing is acceptable because it observes syntax structure without executing code.

Allowed AST observations:

```text
module defines class
module defines function
module imports module
class defines method
function line range
class line range
```

Disallowed AST interpretations:

```text
function purpose
class responsibility
runtime ownership
policy ownership
execution ownership
whether behavior is correct
whether code violates documentation
```

## Artifact Kind Classification

Path classification should be deterministic and conservative.

Examples:

```text
*.md -> documentation_file
scripts/*.py -> script_file
tests/test_*.py -> test_file
seed_runtime/**/*.py -> source_file
*/__init__.py -> package_marker
*.json under catalog-like directories -> catalog_file
*.toml, *.yaml, *.yml -> configuration_file
```

Weak classifications must be explicitly marked weak.

## Predicate Strategy

Repository Observation v0 should prefer a small structural vocabulary.

Suggested predicates:

```text
contains_path
has_kind
under_directory
defines_module
defines_class
defines_function
defines_method
imports_module
appears_related_to
```

`appears_related_to` should be low-confidence and used only for explicit filename or path-pattern relationships.

## Fact Semantics

Repository-derived facts are artifact facts.

They should be interpreted as:

```text
The repository contains evidence that artifact X exists.
```

not:

```text
Artifact X satisfies documented architecture.
```

For example:

```text
seed_runtime/runtime.py defines class Runtime.
```

is a repository fact.

```text
Runtime owns orchestration.
```

is not a Repository Observation fact.

## Confidence

Repository Observation should distinguish direct and weak evidence.

High-confidence facts:

```text
file exists
directory exists
AST class exists
AST function exists
AST import exists
```

Lower-confidence facts:

```text
test appears related to source concept
catalog appears related to vocabulary
script appears to expose CLI entrypoint
```

Confidence should be metadata and should remain visible to explanation and integrity surfaces.

## Projection Requirements

Projected repository facts should preserve:

```text
artifact subject
predicate
object or value
artifact kind
source path
evidence reference
extraction kind
confidence
```

Repository facts should not overwrite documentation facts.

Repository facts should not be automatically compared to documentation facts.

Repository facts should be available to later Repository Reconciliation.

## Query Expectations

Repository Observation v0 should support questions like:

```text
Which paths exist under seed_runtime?
Which modules define Runtime?
Which modules define ProjectionStore?
Which files are tests?
Which files are documentation?
Which modules import seed_runtime.runtime?
Which scripts exist?
Which catalog files exist?
```

It should not answer:

```text
Does Runtime own selection?
Does code match the README?
Which module should be refactored?
Is this architecture correct?
```

## Relationship To Documentation Observation

Documentation Observation observes claims.

Repository Observation observes artifacts.

They are separate acquisition slices.

Example:

```text
Documentation fact:
README claims Seed is not a workflow engine.

Repository fact:
seed_runtime/runtime.py defines class Runtime.
```

Neither fact alone determines architectural alignment.

## Relationship To Repository Reconciliation

Repository Reconciliation will later compare:

```text
documentation facts
repository facts
```

Repository Observation should not perform that comparison.

It should only produce facts that reconciliation can consume later.

## Runtime Impact

None.

Repository Observation should not require Runtime changes.

It should not enter Runtime.

It should not route decisions.

It should not execute tools.

## ToolExecutor Impact

None.

Repository Observation must not use ToolExecutor.

Observing a repository is not registered-operation execution.

## EventLedger Impact

None to ownership.

Repository observations should enter through normal observation/event patterns if implemented.

EventLedger should not gain repository-specific ownership.

## ProjectionStore Impact

None to ownership.

Repository facts should project through existing projection mechanisms.

ProjectionStore should not become repository-specific.

## Integrity Impact

None to ownership.

Knowledge Integrity can later characterize repository facts as supported, stale, conflicting, or weakly supported.

Repository Observation does not own integrity.

## Selection Impact

None to ownership.

Knowledge Selection can later choose repository facts for context.

Repository Observation does not own selection.

## Response Impact

None to ownership.

Response can communicate repository facts.

Repository Observation does not own response formatting.

## Tests To Consider Later

If implemented, tests should be characterization tests over a tiny fixture repository.

They should verify:

```text
path facts are emitted
kind facts are emitted
class facts are emitted
function facts are emitted
import facts are emitted
evidence metadata is attached
source code is not executed
modules are not imported
Runtime is not touched
ToolExecutor is not touched
```

Tests should not require broad repository indexing.

## Success Criteria

Repository Observation v0 succeeds if:

```text
Given a small allowlist of repository paths,
Seed can project evidence-backed artifact facts
about paths, modules, classes, functions, imports, tests, scripts, and catalogs
without executing code,
without importing modules,
and without comparing those facts to documentation claims.
```

## Failure Criteria

The design fails if implementation requires:

```text
RepositoryEngine
StaticAnalysisEngine
CodebaseUnderstandingEngine
Runtime changes
ToolExecutor changes
ProjectionStore ownership changes
EventLedger ownership changes
LLM-required interpretation
semantic summarization
architecture scoring
automatic doc/code reconciliation
```

## Conclusion

Repository Observation v0 should remain small because its facts are small.

It observes artifacts.

It does not understand architecture.

It creates the evidence-backed structural substrate that Repository Reconciliation can use later.