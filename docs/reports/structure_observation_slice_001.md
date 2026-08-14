# Structure Observation Slice 001

## Selected architectural boundary

Recover exactly one implementation-local owner: **Structure Observation**.

The recovered boundary is internal and substrate-independent. It names the shared responsibility already repeated across existing adapters: read-only structural extraction with evidence preservation and explicit non-interpretation.

## Implementation evidence

- `seed_runtime/documentation_structure.py` already exposed a read-only documentation boundary: no prose interpretation, no grammar interpretation, no responsibility recovery, no lexicon stabilization, no claim extraction, no authority inference, no shape inference, no event-ledger writes, and no repository mutation.
- `seed_runtime/knowledge/repository_observation.py` extracts Python repository artifact facts only from caller-provided source text and explicitly avoids reading files, importing modules, reconciling claims, or inferring architecture/ownership.
- `seed_runtime/knowledge/relationship_observation.py` emits relationship evidence from explicit documentation metadata and Python syntax adapters while explicitly avoiding prose/concept inference, graph reconciliation, runtime integration, or ownership claims.
- `seed_runtime/repository_observation.py` observes repository state read-only and preserves operational status evidence without event-ledger writes or cluster mutation.
- Existing diagnostic inventory and shape-audit surfaces keep the public `documentation_structure` compatibility vocabulary unchanged.

## Before

Structure observation was implicit in each adapter. Documentation Structure carried a boundary that mixed the common read-only structural observation contract with Markdown-specific public vocabulary.

Repository/code observation and relationship observation independently repeated the same pattern over Python source text, repository state, and relationship records without an implementation-local common owner.

## After

`seed_runtime/structure_observation.py` defines the internal **Structure Observation** owner and its substrate-independent boundary.

`seed_runtime/documentation_structure.py` now derives its existing public `BOUNDARY` shape from that internal owner while preserving the same public keys and values.

## Ownership made explicit

### 1. What responsibility was previously implicit?

The previously implicit responsibility was read-only, substrate-independent structural observation: structural extraction, evidence preservation, and non-interpretation across documentation, repository/code, relationship, and repository-state adapters.

### 2. Which recovered architectural boundary became explicit?

The explicit recovered boundary is **Structure Observation != Documentation Structure Adapter**.

### 3. What does the new Structure Observation owner own?

Structure Observation owns only substrate-independent concepts:

- read-only observation
- structural extraction
- evidence preservation
- non-interpretation
- the substrate-adapter boundary
- refusal to own substrate parsing, grammar, responsibility recovery, lexicon stabilization, event-ledger writes, repository mutation, or cluster mutation

### 4. What remains owned by the Documentation Structure adapter?

Documentation Structure continues to own Markdown/documentation behavior and compatibility surfaces, including Markdown file selection, headings, sections, links, code fences, front matter, architectural relation observations, recurrence/drilldown/membership reports, formatting, JSON rendering, and the public `documentation_structure` diagnostic vocabulary.

### 5. What remains owned by repository/code observation?

Repository/code observation remains a separate substrate adapter. Python artifact extraction remains in `seed_runtime/knowledge/repository_observation.py`; relationship extraction remains in `seed_runtime/knowledge/relationship_observation.py`; git repository-state observation remains in `seed_runtime/repository_observation.py`.

### 6. Did any public compatibility boundary change?

No.

## Compatibility preserved

No public rename, CLI rename, JSON rename, schema change, event change, ledger change, grammar behavior, responsibility recovery, lexicon behavior, repository-wide adapter framework, plugin registry, or new runtime surface was introduced.

The existing Documentation Structure boundary dictionary remains byte-for-byte equivalent in shape and values at runtime.

## Files changed

- `seed_runtime/structure_observation.py`
- `seed_runtime/documentation_structure.py`
- `tests/test_structure_observation.py`
- `structure_observation_slice_001.md`

## LOC changed

Measured with `git diff --stat` after this slice:

- `seed_runtime/documentation_structure.py`: 3 insertions, 9 deletions
- `seed_runtime/structure_observation.py`: 53 insertions
- `tests/test_structure_observation.py`: 43 insertions
- `structure_observation_slice_001.md`: 102 insertions

## Tests executed

- `pytest -q tests/test_structure_observation.py tests/test_documentation_structure.py tests/test_repository_observation.py tests/test_self_model_acquisition_pipeline.py`

Result: passed.

## Remaining substrate adapters

- Documentation Structure adapter: Markdown documentation structure observation.
- Repository artifact adapter: Python source artifact observation.
- Relationship Observation adapters: authored documentation metadata relationships and Python import/definition relationships.
- Repository state adapter: git repository-state observation.

## Remaining implementation gaps

- No public `Structure Observation` surface exists yet.
- No repository-wide adapter framework exists.
- No grammar, responsibility recovery, or lexicon behavior exists in the recovered owner.
- Additional adapters can continue to depend on the internal boundary when implementation evidence justifies doing so, but this slice intentionally stops after recovering one implementation-local owner.
