# Repository Observation v0 Implementation Characterization

## Purpose

This document characterizes the smallest useful implementation slice for Repository Observation v0.

It intentionally moves from architectural description toward implementation constraints without changing runtime behavior.

The goal is to define a tiny, deterministic artifact extraction slice.

## Implementation Slice

Repository Observation v0 should extract structural repository facts from only:

```text
seed_runtime/
tests/
```

No documentation parsing.

No claim extraction.

No repository reconciliation.

No architecture interpretation.

## Why This Slice

These paths are enough to prove the path:

```text
Repository Artifact
        ↓
Artifact Fact
        ↓
Evidence metadata
```

They contain enough source and test structure to characterize:

* file existence;
* module existence;
* class definitions;
* function definitions;
* imports;
* test files.

## Non-Goals

This slice must not implement:

* Documentation Observation;
* Repository Reconciliation;
* Claim Support projection;
* self-model projection;
* runtime behavior;
* ToolExecutor integration;
* EventLedger ownership changes;
* ProjectionStore ownership changes;
* LLM interpretation;
* semantic code summarization;
* test execution;
* module importing.

## Input Boundary

Inputs are a read-only repository tree.

Allowed root paths:

```text
seed_runtime/
tests/
```

The extractor should fail closed if asked to scan outside this allowlist unless the allowlist is explicitly expanded.

## Extraction Boundary

Allowed extraction structures:

```text
directory entries
file paths
Python AST class definitions
Python AST function definitions
Python AST import statements
filename patterns for tests
```

Disallowed extraction behavior:

```text
source execution
module importing
type checking
call graph construction
control-flow analysis
data-flow analysis
semantic summaries
architecture conclusions
```

## Artifact Families In Scope

V0 artifact families:

```text
path_exists
path_has_kind
module_exists
module_defines_class
module_defines_function
module_imports_module
test_file_exists
```

V0 should prefer fewer high-confidence artifact facts over many weak pattern facts.

## Expected Facts From seed_runtime/

Minimum expected extraction should include structural facts such as:

```text
seed_runtime exists.
seed_runtime/runtime.py exists.
seed_runtime/runtime.py is a source file.
seed_runtime/runtime.py defines module seed_runtime.runtime.
```

If present in the repository, expected artifact facts include:

```text
Runtime class exists.
ToolExecutor class exists.
ProjectionStore protocol or class exists.
EventLedger class exists.
ContextComposer class exists.
PredicateCatalog class exists.
RelationshipCatalog class exists.
EntityTypeCatalog class exists.
InferenceCatalog class exists.
CapabilityCatalog class exists.
```

The extractor should only emit facts backed by observed files and AST nodes.

## Expected Facts From tests/

Minimum expected extraction should include structural facts such as:

```text
tests exists.
tests contains Python test files.
tests/test_*.py files are test files.
```

If present in the repository, expected artifact facts include:

```text
ProjectionStore tests exist.
Runtime tests exist.
Catalog tests exist.
Context composition tests exist.
```

Weak relationship facts such as:

```text
test_projection_store appears related to ProjectionStore.
```

must be explicitly marked weak and should not be required in v0.

## Python AST Requirements

AST parsing is allowed because it observes syntax without executing code.

Allowed AST node observations:

```text
ClassDef
FunctionDef
AsyncFunctionDef
Import
ImportFrom
```

Each AST-derived fact should include:

```text
file path
module name
symbol name
line range
extraction kind
```

## Import Normalization

Import facts should remain structural.

Examples:

```text
seed_runtime.runtime imports seed_runtime.events.
seed_runtime.runtime imports seed_runtime.registry.
```

Do not infer ownership or dependency semantics from imports in v0.

## Kind Classification

Path kind classification should be deterministic.

Examples:

```text
seed_runtime/**/*.py -> source_file
tests/test_*.py -> test_file
*/__init__.py -> package_marker
```

A package may be observed when a directory contains `__init__.py`.

## Evidence Metadata

Every extracted artifact fact should preserve:

```text
path
artifact_kind
line_range when available
extraction_kind
raw_symbol or raw_import when available
normalized_fact
```

Recommended extraction kinds:

```text
directory_entry
file_path
filename_pattern
python_ast_class
python_ast_function
python_ast_import
```

## Output Shape

A future implementation can expose extracted artifacts as plain records before integrating with state projection.

Conceptual record:

```text
RepositoryArtifactFact
  path
  artifact_kind
  module
  symbol
  predicate
  object
  line_range
  extraction_kind
```

This record is an implementation convenience, not a new architectural store.

## Tests To Add Later

If implemented, tests should use tiny fixture repositories.

Test categories:

```text
extracts path facts
classifies source files
classifies test files
extracts Python classes
extracts Python functions
extracts Python imports
preserves evidence metadata
does not import modules
does not execute source
does not scan outside allowlist
```

Tests should not touch Runtime, ToolExecutor, EventLedger, ProjectionStore, or live repository state.

## Success Criteria

Repository Observation v0 succeeds when:

```text
Given a small allowlist of seed_runtime/ and tests/,
Seed can deterministically extract structural artifact facts
with source evidence metadata.
```

## Failure Criteria

The slice fails if implementation requires:

```text
source execution
module importing
LLM interpretation
semantic code summarization
architecture conclusions
claim support projection
repository reconciliation
```

## Recommended Next Step

Implement only a fixture-level extractor or CLI/dev helper that demonstrates deterministic artifact extraction from the two allowlisted paths.

Do not connect it to Runtime.

Do not connect it to ToolExecutor.

Do not project Claim Support yet.

Do not compare artifacts to documentation claims yet.

## Conclusion

Repository Observation v0 should be tiny.

It should prove that repository artifacts can be acquired as structured, evidence-backed records.

Only after that works should Seed consider repository reconciliation implementation.