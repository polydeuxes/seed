# Structure Observation Slice 002

## Selected architectural boundary

Recover exactly one implementation-local boundary:

```text
Structure Observation
        !=
Repository Artifact Observation Adapter
```

The selected adapter is the Python repository-artifact observation implementation in `seed_runtime/knowledge/repository_observation.py`. Relationship observation remains untouched.

## Implementation evidence

- `seed_runtime/structure_observation.py` already defines `Structure Observation` as a substrate-independent owner for read-only structural extraction, evidence preservation, non-interpretation, and substrate boundaries.
- `seed_runtime/knowledge/repository_observation.py` already extracted repository artifact facts from caller-provided Python source text, used Python `ast.parse`, emitted module/file facts even when parsing failed, and emitted class, function, async function, method, and import artifact records when parsing succeeded.
- `RepositoryArtifactFact` remains the record emitted by repository artifact observation for downstream reconciliation.
- Existing tests already proved that repository artifact observation remains separate from documentation claims and supports existence/structure reconciliation through `RepositoryArtifactFact` records.

## Before

Repository artifact observation implemented the shared structure-observation pattern implicitly:

- read-only operation over caller-provided text;
- structural extraction;
- evidence-preserving `RepositoryArtifactFact` construction;
- no file reads, repository scans, imports, LLM calls, reconciliation, runtime/tool integration, event-ledger writes, repository mutation, or cluster mutation.

However, the implementation-local adapter boundary was not named explicitly. Python parsing and repository-artifact record construction lived directly inside the public extractor function.

## After

`RepositoryArtifactObservationAdapterBoundary` now records the implementation-local adapter boundary beneath `Structure Observation`, and `RepositoryArtifactObservationAdapter.extract()` owns the existing Python repository-artifact extraction flow.

The existing public `extract_repository_artifact_facts(source_path, text)` function remains in place and delegates to the adapter without changing returned facts.

## Ownership made explicit

### 1. What responsibility was previously implicit?

Repository artifact observation was previously the implicit Python repository-artifact substrate adapter for Structure Observation. It owned Python parsing, module observation, class observation, function observation, method observation, import observation, and `RepositoryArtifactFact` construction, but that ownership was not named as an adapter boundary.

### 2. Which recovered architectural boundary became explicit?

The explicit recovered boundary is:

```text
Structure Observation != Repository Artifact Observation Adapter
```

### 3. What remains owned by Structure Observation?

Structure Observation continues to own only substrate-independent observation behavior:

- read-only observation;
- structural extraction;
- evidence preservation;
- non-interpretation;
- substrate boundary;
- no substrate parsing;
- no grammar interpretation;
- no responsibility recovery;
- no lexicon stabilization;
- no event-ledger writes;
- no repository mutation;
- no cluster mutation.

### 4. What is now explicitly owned by the Repository Artifact Observation adapter?

The Repository Artifact Observation adapter now explicitly owns repository-artifact-specific behavior:

- Python parsing of caller-provided source text;
- module/file observation;
- class observation;
- top-level function and async-function observation;
- direct method and async-method observation;
- top-level import observation;
- `RepositoryArtifactFact` record construction.

### 5. Did any public compatibility boundary change?

No.

## Compatibility preserved

No public rename, CLI change, JSON change, schema change, event change, ledger change, adapter registry, plugin system, grammar implementation, responsibility recovery, lexicon behavior, or relationship-observation migration was introduced.

The public `extract_repository_artifact_facts(source_path, text)` function remains available and preserves the same returned fact sequence and `RepositoryArtifactFact` shapes for the tested source fixture.

## Files changed

- `seed_runtime/knowledge/repository_observation.py`
  - Added `RepositoryArtifactObservationAdapterBoundary`.
  - Added `REPOSITORY_ARTIFACT_OBSERVATION_ADAPTER_BOUNDARY`.
  - Added `RepositoryArtifactObservationAdapter`.
  - Changed `extract_repository_artifact_facts()` to delegate to the adapter while preserving behavior.
- `tests/test_structure_observation.py`
  - Added tests proving repository artifact observation is explicitly beneath `Structure Observation`.
  - Added a compatibility test proving the public extractor delegates to the adapter without changing emitted artifact shape.
- `structure_observation_slice_002.md`
  - Added this slice report.

## LOC changed

At report time, before adding this report to the final diff, implementation and test changes were:

```text
2 files changed, 129 insertions(+), 28 deletions(-)
```

## Tests executed

```text
pytest -q tests/test_structure_observation.py tests/test_self_model_acquisition_pipeline.py
pytest -q tests/test_structure_observation.py tests/test_self_model_acquisition_pipeline.py tests/test_existence_claim_reconciliation.py tests/test_structure_claim_reconciliation.py
```

Both test commands passed.

## Remaining substrate adapters

- Documentation Structure adapter: Markdown documentation structure observation.
- Relationship Observation adapters: relationship extraction remains independent and untouched by this slice.
- Repository-state observation remains separate from repository artifact fact extraction.

## Remaining implementation gaps

- Relationship Observation has not been recovered beneath Structure Observation in this slice.
- No adapter registry exists, intentionally.
- No plugin architecture exists, intentionally.
- No public `Structure Observation` compatibility surface was added.
- No grammar, responsibility-recovery, or lexicon behavior was introduced.
