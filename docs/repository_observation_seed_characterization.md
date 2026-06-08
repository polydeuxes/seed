# Repository Observation Seed Characterization

## Purpose

This document characterizes what Repository Observation would acquire from Seed's own repository if implemented.

It answers:

```text
What repository facts exist in Seed today?
```

This is the repository-side counterpart to:

```text
docs/documentation_observation_seed_characterization.md
```

That document characterizes documentation claims.

This document characterizes repository artifacts.

## Core Distinction

Documentation Observation produces:

```text
Claim knowledge
```

Repository Observation produces:

```text
Artifact knowledge
```

Repository Reconciliation later compares them.

Repository Observation should not perform that comparison.

## Initial Repository Scope

Repository Observation v0 should use a narrow allowlist.

Suggested Seed allowlist:

```text
README.md
/docs
/seed_runtime
/scripts
/tests
```

This is sufficient to characterize:

* documentation artifacts;
* runtime artifacts;
* catalog artifacts;
* projection artifacts;
* execution artifacts;
* test artifacts.

## Artifact Families

Repository Observation should initially acquire:

```text
paths
directories
packages
modules
classes
functions
imports
tests
scripts
catalogs
configuration artifacts
```

No semantic interpretation is required.

## Repository Root Facts

Expected repository facts:

```text
Repository contains README.md.
Repository contains docs directory.
Repository contains seed_runtime directory.
Repository contains tests directory.
Repository contains scripts directory.
```

These are existence facts.

## Documentation Artifact Facts

Expected facts:

```text
README.md is a documentation file.
docs/architectural_knowledge_map.md is a documentation file.
docs/architectural_status_and_next_frontier.md is a documentation file.
docs/knowledge_representation_map.md is a documentation file.
docs/knowledge_representation_reconciliation.md is a documentation file.
docs/documentation_observation_seed_characterization.md is a documentation file.
```

Repository Observation does not care what these documents claim.

Only that they exist and belong to a class.

## Runtime Artifact Facts

Expected facts:

```text
seed_runtime exists.
seed_runtime/runtime.py exists.
seed_runtime/context exists.
seed_runtime/state exists.
seed_runtime/ledger exists.
seed_runtime/catalogs exists.
```

Repository Observation should acquire these as structural facts.

## Ownership-Relevant Artifacts

Repository Observation should observe artifact existence for concepts frequently referenced by documentation.

Examples:

```text
Runtime exists.
ToolExecutor exists.
ProjectionStore exists.
EventLedger exists.
PredicateCatalog exists.
RelationshipCatalog exists.
EntityTypeCatalog exists.
InferenceCatalog exists.
CapabilityCatalog exists.
```

These are artifact facts.

They are not ownership conclusions.

## Class Facts

Expected class-level facts:

```text
Runtime class exists.
ToolExecutor class exists.
ProjectionStore class exists.
ContextComposer class exists.
```

Additional classes may exist.

Repository Observation should record what is present rather than what is expected.

## Function Facts

Expected function-level facts:

```text
Runtime._route exists.
Projection helper functions exist.
Context composition functions exist.
Catalog access functions exist.
```

Repository Observation should not infer purpose.

## Import Facts

Expected import observations:

```text
Runtime imports other runtime modules.
Runtime imports ToolExecutor.
Catalog-related modules import catalog definitions.
Projection-related modules import projection helpers.
```

The exact import graph is implementation evidence.

Repository Observation should preserve it.

## Test Artifact Facts

Expected test observations:

```text
ProjectionStore tests exist.
Runtime tests exist.
Catalog tests exist.
Context composition tests exist.
```

Repository Observation should classify tests.

Weak relationships may be recorded:

```text
test_projection_store appears related to ProjectionStore.
```

These should remain explicitly weak.

## Script Artifact Facts

Expected observations:

```text
Local CLI scripts exist.
Repository helper scripts exist.
```

Repository Observation should identify script files.

It should not execute them.

## Catalog Artifact Facts

Expected observations:

```text
PredicateCatalog artifacts exist.
RelationshipCatalog artifacts exist.
EntityTypeCatalog artifacts exist.
InferenceCatalog artifacts exist.
CapabilityCatalog artifacts exist.
```

Repository Observation should identify catalog artifacts.

It should not interpret catalog meaning.

## Representation-Layer Artifacts

Expected observations:

```text
FactSupport artifacts exist.
Evidence-related artifacts exist.
Projection-related artifacts exist.
Relationship-related artifacts exist.
Contradiction-related artifacts exist.
```

These observations are important because they provide repository-side support for representation-layer claims.

Repository Observation should still remain structural.

## Rejected Concept Artifact Checks

Repository Observation should be able to answer:

```text
Does ResponseEngine exist?
Does IntegrityEngine exist?
Does SelectionEngine exist?
Does CaveatEngine exist?
Does ClaimStore exist?
Does SupportStore exist?
```

Expected observations today:

```text
No matching artifacts observed.
```

These become useful inputs for Repository Reconciliation.

## Example Artifact Inventory

### ToolExecutor

Expected artifact facts:

```text
ToolExecutor class exists.
ToolExecutor module exists.
ToolExecutor tests may exist.
Runtime imports ToolExecutor.
```

Repository Observation should not conclude:

```text
ToolExecutor owns execution.
```

That is a reconciliation question.

## Example Artifact Inventory

### ProjectionStore

Expected artifact facts:

```text
ProjectionStore protocol exists.
InMemoryProjectionStore exists.
SQLiteProjectionStore exists.
Projection snapshot storage artifacts exist.
```

Repository Observation should not conclude:

```text
ProjectionStore owns cached projections.
```

That is a documentation claim.

## Example Artifact Inventory

### Runtime

Expected artifact facts:

```text
Runtime class exists.
Runtime._route exists.
Runtime imports other runtime modules.
```

Repository Observation should not conclude:

```text
Runtime owns orchestration.
Runtime violates architecture.
Runtime is correct.
```

Those require interpretation.

## Evidence Requirements

Every repository fact should retain:

```text
path
artifact kind
line range when available
extraction kind
source text span when available
```

Recommended extraction kinds:

```text
directory_entry
file_path
python_ast_class
python_ast_function
python_ast_import
filename_pattern
```

## Query Expectations

Repository Observation over Seed should answer:

```text
Which runtime modules exist?
Which catalog artifacts exist?
Which classes exist?
Which functions exist?
Which tests exist?
Which imports exist?
Do rejected concept artifacts exist?
```

It should not answer:

```text
Which architecture is correct?
Which ownership claim is true?
Does code match documentation?
What should be implemented next?
```

Those require Repository Reconciliation or human review.

## Repository Observation Output

Repository Observation should produce facts like:

```text
seed_runtime/runtime.py defines class Runtime.
seed_runtime/runtime.py imports ToolExecutor.
tests/test_projection_store.py is a test file.
README.md is a documentation file.
```

Not:

```text
Runtime owns execution.
ProjectionStore is correct.
Architecture is aligned.
```

Those are not repository facts.

## Relationship To Documentation Observation

Documentation Observation over Seed should acquire:

```text
claims
```

Repository Observation over Seed should acquire:

```text
artifacts
```

Together they create the inputs required by Repository Reconciliation.

## Completion Criteria

Seed-specific Repository Observation is characterized when it has:

* repository allowlist;
* artifact families;
* expected repository facts;
* example artifact inventories;
* evidence requirements;
* query expectations;
* documentation-observation relationship.

This document provides that characterization.

## Recommended Next Step

Once both Seed-specific characterizations exist:

```text
Documentation Observation Seed Characterization
Repository Observation Seed Characterization
```

create:

```text
Repository Reconciliation Seed Characterization
```

That document should compare actual Seed claims with actual Seed artifacts.

## Conclusion

Seed already contains a substantial body of observable repository artifacts.

Repository Observation should acquire those artifacts as evidence-backed structural knowledge.

It should not interpret them.

Interpretation belongs to Repository Reconciliation.