# Repository Observation Frontier

## Purpose

This document defines the next frontier after Documentation Observation.

It preserves the architectural distinction between:

```text
Documentation Observation
        ↓
Repository Observation
        ↓
Repository Reconciliation
```

Documentation Observation asks:

```text
What does the repository say it is meant to be?
```

Repository Observation asks:

```text
What does the repository actually contain?
```

Repository Reconciliation later asks:

```text
Do documentation claims and repository artifacts agree?
```

This document covers Repository Observation only.

## Problem

Seed can only reason about a codebase if it first has evidence-backed projected knowledge about the codebase.

A repository contains many observable artifacts:

* files
* directories
* packages
* modules
* imports
* classes
* functions
* tests
* schemas
* catalogs
* scripts
* configuration files
* documentation files
* dependency declarations
* CI definitions

A human can inspect those artifacts and build a mental image of the repository's actual shape.

Seed does not yet have a narrow observation slice that turns repository artifacts into evidence-backed projected facts.

Without Repository Observation, Seed cannot safely answer questions such as:

```text
Which modules exist?
Which package owns this file?
Which files define Runtime-adjacent behavior?
Which tests characterize ProjectionStore?
Does this repository contain a ToolExecutor implementation?
Does this repository contain a generated toolkit path?
```

Those questions require repository facts, not documentation claims.

## Core Distinction

Repository Observation does not interpret intent.

It observes artifacts.

The safe v0 distinction is:

```text
Repository contains file X.
File X is under package or directory Y.
File X imports module Z.
File X defines class C.
File X defines function F.
File X contains test T.
```

Those are artifact facts.

They are not architectural reconciliation facts.

Repository Observation should not say:

```text
The code violates the docs.
The architecture is wrong.
Runtime owns selection.
This module should be refactored.
```

Those require reconciliation or human judgment.

## Why Repository Observation Is A Knowledge Acquisition Slice

Repository Observation fits the existing lifecycle:

```text
Repository Artifact
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

The repository is the observed world.

The artifacts are evidence.

The projected facts describe what exists.

## What V0 Should Observe

Repository Observation v0 should start narrow.

Initial artifact families:

* repository root files
* top-level directories
* Python packages
* Python modules
* Python imports
* Python classes
* Python functions
* test files
* documentation files
* script files
* catalog files
* configuration files

V0 should prefer structural facts over semantic interpretation.

## Initial Fact Families

Suggested fact families:

| Fact family | Meaning |
| --- | --- |
| `repository_contains_path` | A file or directory exists in the repository. |
| `path_has_kind` | A path is a module, package, test, doc, script, config, catalog, or source file. |
| `path_under_directory` | A file or directory belongs under another directory. |
| `module_defines_class` | A Python module defines a class. |
| `module_defines_function` | A Python module defines a function. |
| `module_imports_module` | A Python module imports another module. |
| `test_file_targets_path` | A test file appears to target a source path or concept by name. |
| `catalog_file_defines_vocab` | A catalog file appears to define structured vocabulary. |
| `script_exposes_entrypoint` | A script exposes a CLI or runnable entrypoint. |

These facts describe repository structure.

They do not prove architecture.

## Initial Subjects

Repository Observation v0 can use subjects such as:

* repository
* path
* directory
* file
* package
* module
* class
* function
* test file
* catalog file
* script

Example facts:

```text
repository contains path seed_runtime/runtime.py
seed_runtime/runtime.py has kind source_file
seed_runtime/runtime.py defines class Runtime
seed_runtime/runtime.py imports seed_runtime.events
repository contains path tests/test_projection_store.py
tests/test_projection_store.py has kind test_file
```

## Evidence Requirements

Every repository fact should retain evidence.

Required evidence metadata:

* repository path
* file path
* line range when available
* extraction kind
* observed text span or structural source

Recommended extraction kinds:

* `directory_entry`
* `file_path`
* `python_ast_class`
* `python_ast_function`
* `python_ast_import`
* `filename_pattern`
* `json_key`
* `yaml_key`
* `toml_key`
* `markdown_heading`

## What V0 Should Answer

Repository Observation v0 should support narrow artifact questions:

* What files exist under `seed_runtime/`?
* Which modules define classes named `Runtime`, `ToolExecutor`, or `ProjectionStore`?
* Which files are tests?
* Which files are documentation?
* Which files are catalogs?
* Which modules import `seed_runtime.runtime`?
* Which scripts expose local CLI entrypoints?
* Which files look like package, dependency, or tool configuration?

These are observation questions.

They do not require reconciliation.

## What V0 Must Not Do

Repository Observation v0 must not create:

* `RepositoryEngine`
* `CodebaseUnderstandingEngine`
* `StaticAnalysisEngine`
* hidden code understanding store
* automatic architecture evaluation
* automatic doc/code comparison
* automatic refactoring recommendations
* broad semantic code summarization
* LLM-required interpretation
* runtime behavior
* provider execution
* shell execution
* ToolExecutor integration
* repository mutation

Repository Observation must not decide whether code is good.

Repository Observation must not decide whether code matches documentation.

Repository Observation must not infer ownership from naming alone unless the fact is explicitly scoped as a weak observation.

## Relationship To Documentation Observation

Documentation Observation and Repository Observation are peer acquisition slices.

Documentation Observation produces facts about documentation claims.

Repository Observation produces facts about repository artifacts.

They should remain separate:

```text
Documentation facts ≠ Repository facts
```

A documentation fact may say:

```text
README claims ProjectionStore owns cached projected state.
```

A repository fact may say:

```text
seed_runtime/projection_store/sqlite.py defines class SQLiteProjectionStore.
```

Neither fact alone proves alignment.

## Relationship To Repository Reconciliation

Repository Reconciliation will later compare documentation facts and repository facts.

Examples:

```text
Documentation claims ToolExecutor owns execution.
Repository contains ToolExecutor class.
Repository contains Runtime route that calls ToolExecutor.
```

Reconciliation asks whether those facts align, drift, or require human review.

Repository Observation must not perform that comparison.

## Authority And Confidence

Repository Observation should distinguish direct structural evidence from weak pattern evidence.

High-confidence examples:

* file exists
* directory exists
* Python AST defines class
* Python AST defines function
* Python AST imports module

Lower-confidence examples:

* test appears to target source file by filename similarity
* catalog appears to define vocabulary by filename or keys
* script appears to expose CLI entrypoint

Confidence should be explicit metadata, not hidden behavior.

## Source Boundary

Repository Observation v0 should be local and read-only.

It should observe a checked-out repository tree or an equivalent file listing/content source.

It should not require:

* network calls
* GitHub API calls at runtime
* shell execution
* dependency installation
* language server integration
* type checking
* test execution
* importing repository modules

Parsing Python source with a safe parser is acceptable.

Executing Python source is not.

## Suggested V0 Allowlist

For Seed itself, the first repository observation pass should likely start with:

```text
README.md
docs/
seed_runtime/
scripts/
tests/
```

It should avoid broad generated artifacts, caches, virtual environments, local databases, and build output.

## Rejection Criteria

Do not implement Repository Observation if the work requires:

* Runtime changes
* ToolExecutor changes
* EventLedger ownership changes
* ProjectionStore ownership changes
* provider execution
* shell execution
* source importing
* test execution
* broad semantic summarization
* central repository engine
* hidden architecture scoring
* automatic doc/code reconciliation

Do not continue design if the proposed v0 cannot be reduced to explicit artifact facts with evidence.

## Recommended Next Step

Before implementation, add a characterization document defining the exact repository facts v0 should extract from Seed's own repository structure.

The characterization should answer:

* which paths are in the v0 allowlist;
* which file kinds are recognized;
* which Python AST nodes are observed;
* which facts are expected for known files;
* which evidence metadata is required;
* which questions v0 can answer;
* which questions require Repository Reconciliation instead.

The safest first success criterion is:

```text
Given a small allowlist of repository paths,
Seed can project evidence-backed repository artifact facts
without executing code,
without importing modules,
and without comparing those facts to documentation claims.
```

## Conclusion

Repository Observation is the next Knowledge Acquisition slice after Documentation Observation.

Its responsibility is not to understand a codebase in one leap.

Its responsibility is to observe the codebase's artifacts and project evidence-backed structural knowledge.

Once that exists, Repository Reconciliation can compare what the repository claims against what the repository contains.
