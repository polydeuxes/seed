# Observation Agreement Slice 001

## Selected architectural boundary

Recovered exactly one implementation-local boundary:

```text
Observation Agreement != Grammar Observation
```

`Observation Agreement` is now an internal, read-only owner for candidate agreement between independent already-observed records. It consumes only supplied observation records, preserves candidate agreement and provenance, preserves observation independence, emits candidate agreement records, and rejects promotion.

This slice does not recover Grammar Observation, Responsibility, family recovery, lexicon, semantic interpretation, or architectural truth.

## Implementation evidence

- `seed_runtime/structure_observation.py` already names Structure Observation as the read-only structural extraction boundary and rejects grammar ownership, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation.
- `seed_runtime/documentation_structure.py` already emits `DocumentationArchitecturalRelationRecord` records with `left_term`, `relation`, `right_term`, `source_path`, `line_number`, and `evidence`.
- `seed_runtime/knowledge/self_model_alignment.py` already defines `RepositoryArtifactFact` as a supplied repository artifact observation record.
- `seed_runtime/knowledge/relationship_observation.py` already defines `RelationshipFact` and states that import and definition relationships do not prove behavior, calls, boundaries, ownership, invocation, reachability, capability authority, or runtime ownership.
- `observation_agreement_classification_audit.md` previously identified `Observation Agreement` as read-only preservation of candidate agreement between independent observation streams without promotion to truth, grammar, responsibility, lexicon, semantics, or mutation.

## Before

Observation agreement existed only as an audit-level responsibility candidate. The repository had independent observation streams and records, but no implementation-local owner that explicitly preserved agreement among those supplied records while refusing promotion.

The implicit responsibility was:

```text
candidate agreement preservation across independent observation streams
```

Because it was implicit, the boundary between agreement and grammar/responsibility/lexicon/truth was documented but not implementation-local.

## After

Added `seed_runtime/knowledge/observation_agreement.py` with:

- `ObservationAgreementEvidence`
- `ObservationAgreementRecord`
- `OBSERVATION_AGREEMENT_BOUNDARY`
- `observe_observation_agreements(...)`

The implementation consumes only these supplied record families:

- `DocumentationArchitecturalRelationRecord`
- `RepositoryArtifactFact`
- `RelationshipFact`

It emits candidate agreement records only when two or more independent supplied streams preserve the same trimmed evidence text. This deliberately small rule avoids Markdown parsing, Python parsing, repository reading, runtime scanning, tool execution, semantic inference, vocabulary canonicalization, and truth promotion.

## Ownership made explicit

### 1. What responsibility was previously implicit?

Candidate agreement preservation across independent observation streams was previously implicit. The audits described agreement as downstream and comparative, but no implementation-local record owned candidate agreement, provenance, independence, and non-promotion together.

### 2. Which recovered architectural boundary became explicit?

`Observation Agreement != Grammar Observation` became explicit. The new boundary owns only candidate agreement records over supplied observations and explicitly refuses grammar ownership.

### 3. What does Observation Agreement now own?

Observation Agreement now owns:

- consuming supplied observation records;
- preserving candidate agreement;
- preserving provenance;
- preserving observation independence;
- emitting candidate agreement records;
- rejecting promotion.

It explicitly refuses ownership of:

- grammar;
- responsibility recovery;
- family recovery;
- lexicon;
- semantic interpretation;
- architectural truth;
- runtime mutation;
- event writes;
- ledger writes;
- repository mutation;
- cluster mutation.

### 4. What remains owned by Structure Observation?

Structure Observation continues to own read-only structural extraction and substrate adapter boundaries. Documentation Structure remains responsible for documentation structure records, including `DocumentationArchitecturalRelationRecord`. Repository Artifact Observation remains responsible for repository artifact observation records such as `RepositoryArtifactFact`.

### 5. What remains owned by Relationship Observation?

Relationship Observation continues to own relationship evidence construction and relationship-specific extraction invariants through `RelationshipFact`. It remains separate from behavior proof, ownership proof, reachability proof, runtime ownership, graph building, and runtime/tool integration.

### 6. What remains reserved for Grammar Observation?

Grammar Observation remains reserved for any future grammar-specific owner. This slice does not infer grammar, parse prose grammar, canonicalize relation tokens into grammar, or promote recurring agreement into grammar authority.

### 7. Did any compatibility boundary change?

No.

## Compatibility preserved

No public compatibility surface changed:

- no CLI changes;
- no JSON changes;
- no schema changes;
- no diagnostic inventory changes;
- no diagnostic shape-audit changes;
- no event changes;
- no ledger behavior changes;
- no runtime behavior changes;
- no compatibility object changes.

The new implementation is internal and read-only.

## Files changed

- `seed_runtime/knowledge/observation_agreement.py`
- `tests/test_observation_agreement.py`
- `observation_agreement_slice_001.md`

## LOC changed

At slice creation time:

```text
132 seed_runtime/knowledge/observation_agreement.py
110 tests/test_observation_agreement.py
156 observation_agreement_slice_001.md
398 total
```

## Tests executed

```text
pytest -q tests/test_observation_agreement.py
```

Result:

```text
3 passed
```

## Remaining implementation gaps

- No public CLI, JSON, schema, diagnostic inventory, or diagnostic shape-audit surface exists for Observation Agreement. This is intentional for this internal slice.
- The agreement rule is intentionally minimal and exact-evidence based. It does not attempt semantic matching, label normalization, grammar recovery, responsibility recovery, family recovery, or lexicon stabilization.
- Future Grammar Observation, if recovered, must be implemented separately and must not be inferred from this slice.

## Stop condition

The slice stops after recovering Observation Agreement as a bounded implementation-local owner. It does not continue into Grammar Observation.
