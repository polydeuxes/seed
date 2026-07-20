# Repository Observation Characterization

## Purpose

This document characterizes Repository Observation v0.

It defines the exact repository artifact facts Seed should be able to extract from its own repository before implementation begins.

This is documentation-only.

It does not justify runtime behavior, repository mutation, static-analysis engines, model interpretation, or repository reconciliation.

## Core Question

Repository Observation asks:

```text
What artifacts exist?
```

It does not ask:

```text
Why do they exist?
What architecture should exist?
Do they match documentation?
Are they correct?
```

Those questions belong elsewhere.

## Scope

Repository Observation v0 is limited to structural repository facts.

The repository itself is the observed world.

The observation target is:

```text
Repository
  ↓
Directories
  ↓
Files
  ↓
Modules
  ↓
Classes
  ↓
Functions
```

No semantic interpretation is required.

## V0 Repository Allowlist

Repository Observation v0 should remain intentionally small.

Suggested allowlist:

```text
README.md
/docs
/seed_runtime
/scripts
/tests
```

Excluded:

```text
.git
.pytest_cache
.mypy_cache
venv
.venv
build artifacts
coverage artifacts
database files
editor metadata
```

The goal is stable architectural observation rather than complete repository inventory.

## Initial Artifact Kinds

V0 should classify paths into:

```text
directory
source_file
package
module
test_file
documentation_file
script_file
catalog_file
configuration_file
```

Classification should be explicit and deterministic.

## Expected Repository Facts

The purpose of characterization is to define expected facts.

These are examples of the kinds of facts v0 should be capable of producing.

## Repository Root Facts

```text
Repository contains README.md.
Repository contains docs directory.
Repository contains seed_runtime directory.
Repository contains tests directory.
Repository contains scripts directory.
```

These are existence facts.

## Documentation Facts

```text
README.md is a documentation file.
docs/architectural_knowledge_map.md is a documentation file.
docs/documentation_observation_frontier.md is a documentation file.
docs/repository_observation_frontier.md is a documentation file.
```

Repository Observation does not care what the documents mean.

Only that they exist and belong to a file class.

## Runtime Package Facts

Repository Observation should be able to observe that runtime-related paths exist.

Examples:

```text
seed_runtime is a package.
seed_runtime/runtime.py is a source file.
seed_runtime/context is a directory.
seed_runtime/ledger is a directory.
seed_runtime/state is a directory.
seed_runtime/registry is a directory.
```

These are structural facts.

## Module Facts

Repository Observation should observe modules.

Examples:

```text
seed_runtime.runtime is a module.
seed_runtime.context is a module or package.
seed_runtime.state is a module or package.
seed_runtime.ledger is a module or package.
```

The observation should come from repository structure.

## Class Facts

Repository Observation should observe class definitions.

Examples:

```text
Runtime class exists.
ToolExecutor class exists.
ProjectionStore class exists.
ContextComposer class exists.
```

The observation should be:

```text
module_defines_class
```

not:

```text
class owns architecture concern
```

The latter requires interpretation.

## Function Facts

Repository Observation should observe function definitions.

Examples:

```text
Runtime._route exists.
ContextComposer methods exist.
Projection helper functions exist.
```

The fact should remain structural.

Repository Observation should not infer purpose.

## Import Facts

Repository Observation should observe imports.

Examples:

```text
module A imports module B.
module B imports module C.
```

These are dependency observations.

They are not ownership claims.

## Test Facts

Repository Observation should classify tests.

Examples:

```text
tests/test_projection_store.py is a test file.
tests/test_runtime.py is a test file.
```

Weak observations may exist:

```text
test_projection_store appears related to ProjectionStore.
```

But weak observations must remain explicitly weak.

## Script Facts

Repository Observation should identify runnable scripts.

Examples:

```text
scripts/seed_local.py is a script file.
```

Possible weak observation:

```text
seed_local.py appears to expose a CLI entrypoint.
```

This should not require execution.

## Catalog Facts

Repository Observation should identify catalog artifacts.

Examples:

```text
PredicateCatalog-related files exist.
RelationshipCatalog-related files exist.
InferenceCatalog-related files exist.
CapabilityCatalog-related files exist.
```

The observation should be structural.

Repository Observation should not interpret catalog meaning.

## Evidence Requirements

Every repository fact requires evidence.

Required metadata:

```text
path
artifact kind
line range when available
extraction kind
source text span when available
```

Examples:

```text
python_ast_class
python_ast_function
python_ast_import
directory_entry
file_path
```

## Fact Strength

Repository Observation should distinguish:

```text
Direct observation
```

from:

```text
Pattern-based observation
```

High confidence:

```text
File exists.
Directory exists.
Class exists.
Function exists.
Import exists.
```

Lower confidence:

```text
Test appears related to source file.
Script appears to expose CLI entrypoint.
Catalog appears related to vocabulary.
```

Confidence should remain visible metadata.

## Query Expectations

Repository Observation v0 should answer:

```text
Which runtime modules exist?
Which classes exist?
Which functions exist?
Which tests exist?
Which scripts exist?
Which catalog files exist?
Which modules import a given module?
```

Repository Observation v0 should not answer:

```text
Which component owns execution?
Which component owns selection?
Does implementation match documentation?
Which architecture is correct?
```

Those require Repository Reconciliation.

## Explicit Non-Goals

Repository Observation v0 is not:

```text
Static analysis
Architecture analysis
Repository reconciliation
Code quality review
Refactoring guidance
Design review
Execution analysis
Behavioral verification
Test execution
Type checking
```

It is observation only.

## Success Criteria

Repository Observation v0 succeeds if:

```text
Seed can project evidence-backed repository artifact facts
```

for:

```text
paths
modules
classes
functions
imports
tests
scripts
catalogs
```

without:

```text
executing code
importing modules
running tests
comparing documentation
performing architecture evaluation
```

## Failure Criteria

The design fails if implementation requires:

```text
RepositoryEngine
CodebaseUnderstandingEngine
semantic repository summaries
LLM-required interpretation
runtime ownership changes
ToolExecutor ownership changes
ProjectionStore ownership changes
EventLedger ownership changes
```

## Recommended Next Step

The next document should be:

```text
Repository Observation Design
```

That design should explain:

* how repository artifacts become observations;
* how AST extraction remains read-only;
* how evidence is attached;
* which existing observation/event structures are reused;
* why repository observation does not become static analysis.

## Conclusion

Repository Observation v0 is intentionally narrow.

Its responsibility is not understanding architecture.

Its responsibility is producing evidence-backed structural knowledge about repository artifacts.

Architecture understanding emerges later through reconciliation, not through observation.