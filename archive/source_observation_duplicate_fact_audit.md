# Source Observation Duplicate Fact Audit

## Purpose

This audit investigates why repository source-observation facts such as `imports`
and `defines` appear duplicated in operator-facing output.

It is a documentation-only implementation audit.

It does not change code, schemas, projections, observations, facts, tests,
runtime behavior, source observation behavior, CLI behavior, or storage.

## Trigger

After repository self-observation expanded beyond imports to include definitions,
live operator output showed adjacent duplicate source facts:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views._entity_summary_row
seed_runtime.state_summary_views defines seed_runtime.state_summary_views._entity_summary_row
```

and similar duplicate `imports` rows.

The operator also observed that:

```text
seed --unsupported-facts
```

reported:

```text
(none)
```

Therefore the issue is not obviously unsupported source facts. The question is
which layer owns the duplication or duplicate-looking presentation.

## Central Finding

The most likely cause is repeated observation ingestion of stable repository
source relationships, not AST extraction emitting duplicates for a single source
file.

The source extractor emits one relationship per top-level AST definition and one
relationship per import alias. The observed adjacent duplicate rows are more
consistent with the same repository source observation being collected and
promoted more than once across observation runs.

The boundary finding is:

```text
repeated observation
        !=
new durable source relationship
```

Repository source relationships such as:

```text
module defines symbol
module imports symbol
```

are durable structural observations. Re-observing the same relationship should
accumulate provenance or support without making the default current-fact surface
look like the relationship exists twice.

## Evidence Reviewed

### Repository Source Observation Emits Imports And Definitions Together

`RepositorySourceObservationSource.collect()` scans allowlisted Python source
files and combines import and definition relationship facts:

```python
relationship_facts = [
    *extract_python_import_relationship_facts(source_path, text),
    *extract_python_definition_relationship_facts(source_path, text),
]
observations.extend(
    self._relationship_observation(relationship)
    for relationship in relationship_facts
)
```

Each relationship becomes an observation with:

```python
subject=relationship.subject
predicate=relationship.relationship_kind
value=relationship.object
metadata={... "source_path": relationship.path, ...}
dimensions={"path": relationship.path}
```

This means source observations are ordinary observations promoted through the
standard observation pipeline.

### Definition Extraction Is One Relationship Per Top-Level Definition

`extract_python_definition_relationship_facts()` parses a file once, iterates
only `tree.body`, and appends one relationship for each top-level function,
async function, or class definition:

```python
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        facts.append(_definition_relationship(source_path, subject, node))
```

The helper constructs one object name from the module subject and AST node name:

```python
symbol = f"{subject}.{node.name}"
```

This does not explain adjacent duplicate rows for the same symbol within a
single file unless the same file is processed more than once or the same
relationship is ingested more than once.

### Import Extraction Is One Relationship Per Import Alias

Import extraction iterates top-level import nodes and emits one relationship per
alias. Duplicate imports inside the same file could produce multiple facts, but
live output showed broad paired duplication across many imports and definitions,
which is more consistent with repeated repository observation runs than isolated
source code duplication.

### Observation Ingestion Always Creates New IDs

`ObservationIngestor.ingest_many()` converts each observation to new evidence and
a new fact when fact promotion is not suppressed:

```python
evidence = self.observation_to_evidence(observation, workspace_id)
fact = self.observation_to_fact(observation, evidence)
```

`observation_to_evidence()` assigns a new evidence id:

```python
id=new_id("evd_obs")
```

`observation_to_fact()` assigns a new fact id:

```python
id=new_id("fact_obs")
```

This is appropriate for append-only observation preservation, but repeated
collection of the same durable source relationship creates distinct facts unless
projection or rendering collapses them.

### Projection Supports Aggregate Compatible Facts

`_project_fact_supports()` groups facts by:

```python
(subject, predicate, dimensions, value_key)
```

For non-measurement predicates, it creates one aggregate support record with all
supporting fact ids.

That means the projection already has a conceptual support-rollup mechanism for
identical durable claims. The default raw current-facts surface may still render
representative facts or underlying facts in a way that makes repeated support
appear as duplicate relationships.

## Layer Assessment

### AST Extraction Layer

Likely not the primary owner.

The extraction code appears deterministic and bounded. It emits one `defines`
relationship per top-level declaration and one `imports` relationship per import
alias. It does not itself appear to intentionally duplicate each extracted
relationship.

### Repository Source Discovery Layer

Possible owner if the same physical file is discovered more than once.

The repository source discovery walks configured include roots and returns sorted
source paths. If include roots overlap, the same file could be observed more than
once in one run. Current default include roots are `("seed_runtime", "tests")`,
which should not overlap for the observed `seed_runtime.*` examples.

This should still be tested directly before ruling it out.

### Observation Ingestion Layer

Strong likely contributor.

Each collection run creates new observations, evidence, and fact ids for the same
stable source relationships. For durable structural source facts, repeated
observation should probably accumulate support without causing duplicate-looking
operator rows.

### Projection Layer

Possible mitigation point.

Projection already aggregates durable support groups. A source-navigation view
should probably present one source relationship with support count/provenance,
not one row per fact id.

### Rendering / Current-Facts Surface

Strong visible owner.

The duplicated rows are observed in `--current-facts`. Even if the ledger
properly preserves repeated observations, the current-facts surface should not
make stable durable relationships appear as if the source defines/imports the
same thing twice without qualification.

## Boundary Analysis

The bug is not simply "duplicate facts bad."

Append-only preservation may legitimately keep repeated observations. The
problem is that a default current relationship surface should distinguish:

```text
one relationship with multiple support observations
```

from:

```text
multiple distinct relationships
```

For source definitions and imports, adjacent duplicate rows hide the useful
navigation answer and reduce operator trust.

## Suspected Root Cause

The likely sequence is:

```text
repository source observed
        -> source relationship observations emitted
        -> each observation receives new evidence id
        -> each observation receives new fact id
        -> repeated repository observation emits same relationship again
        -> current-facts renders multiple fact instances
        -> operator sees duplicate imports/defines rows
```

This should be confirmed with a targeted test that runs repository observation
twice against the same source tree and inspects:

- ledger event count;
- observation count;
- evidence count;
- fact count;
- fact support grouping;
- `--current-facts` rendering.

## What Is Correct

- Repeated observations may be preserved in the append-only ledger.
- Evidence for each observation should remain auditable.
- Source facts should remain evidence-backed.
- `imports` remains dependency evidence only.
- `defines` remains ownership/declaration evidence only.
- Repeated source observation should not be silently deleted without preserving
  provenance.

## What Is Incorrect Or Suspect

- Default current-facts output appears to present repeated support as repeated
  relationships.
- Source observations do not yet have a source-navigation projection that rolls
  up identical durable source relationships.
- Queryability is degraded because duplicate rows amplify fact flood.
- It is unclear whether duplicates are in stored facts, projected current facts,
  or only rendering.

## Candidate Fix Directions

This audit does not implement changes. Candidate implementation directions are:

### 1. Add A Duplicate Diagnosis Test First

Create a focused test that observes a small repository fixture twice and asserts
which layer contains repetition.

The test should answer:

```text
Are duplicate source relationships duplicated in the ledger, projected state,
fact support groups, or rendered current-facts output?
```

### 2. Prefer Rollup In Source Navigation Surface

For source relationship navigation, present one row per stable relationship:

```text
seed_runtime.state_summary_views defines seed_runtime.state_summary_views.state_summary
    support: 2 observations
```

instead of two identical rows.

### 3. Avoid Deleting Provenance

Do not remove repeated observations merely to make output cleaner. If repeated
source observation matters historically, preserve it as support/provenance.

### 4. Consider Stable Source Observation IDs Only Carefully

Stable IDs could suppress duplicate observation events, but that would change
append-only observation behavior. It should not be the first fix unless the
architecture explicitly wants idempotent durable-source observation refresh.

### 5. Current-Facts Rendering Could Use Support Groups

If `--current-facts` is intended to show current durable claims rather than every
supporting fact instance, it should render aggregate support groups for durable
multi-observation claims.

That is broader than source observation and should be scoped carefully.

## Non-Goals

This audit does not recommend:

- deleting repeated observations;
- deleting evidence;
- changing append-only event semantics;
- changing source relationship extraction semantics;
- making imports/defines imply behavior;
- collapsing module identity and path identity;
- building call graph observation;
- implementing a new source query command;
- suppressing repository source observations entirely.

## Files Inspected

- `seed_runtime/observation_sources.py`
- `seed_runtime/knowledge/relationship_observation.py`
- `seed_runtime/observations.py`
- `seed_runtime/state.py`

## Invariants

```text
Repeated observation is not a new durable source relationship.
```

```text
Duplicate-looking source facts should be diagnosed before deletion or collapse.
```

```text
Preserved repeated evidence should roll up into explainable support when the
claim is identical.
```

```text
Source relationship navigation should present relationships, not raw fact-id
multiplicity.
```

```text
Cleaning output must not erase provenance.
```

## Conclusion

The duplicate source fact symptom is most likely caused by repeated observation
of stable repository source relationships flowing through the standard
append-only observation-to-evidence-to-fact path. That path correctly preserves
provenance, but the current operator-facing source/current-facts surface appears
to render repeated support as repeated relationships.

The next implementation step should not be a new source query command yet. It
should be a targeted duplicate diagnosis test that locates whether duplication is
stored, projected, or rendered, followed by the smallest fix that preserves
provenance while preventing identical durable source relationships from flooding
operator navigation surfaces.
