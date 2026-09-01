# Grammar Observation Slice 001

## Selected architectural boundary

Recovered exactly one implementation-local boundary:

```text
Grammar Observation != Responsibility Recovery
```

Grammar Observation is now represented as a read-only, internal owner that consumes only `ObservationAgreementRecord` instances and emits implementation-local `GrammarObservationRecord` instances for recurring relation shapes.

## Implementation evidence

- `ObservationAgreementRecord` already exposes the durable evidence contract Grammar Observation can consume: `candidate_agreement`, `participating_observation_streams`, `supporting_evidence`, `provenance`, and `non_promotion_boundary`.
- `observation_agreement.py` explicitly refuses grammar ownership, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, event writes, ledger writes, repository mutation, runtime mutation, and cluster mutation.
- `grammar_observation.py` now defines the adjacent internal owner with the narrow input type `Sequence[ObservationAgreementRecord]`.
- `GrammarObservationRecord` preserves only `observed_relation_shape`, `supporting_agreements`, `provenance`, `recurrence_evidence`, and `non_promotion_boundary`.
- Tests prove Grammar Observation emits only when a relation shape recurs across at least two agreement records.
- Tests prove Grammar Observation preserves recurrence evidence and does not promote responsibility, family, lexicon, semantic interpretation, or architectural truth.

## Before

Observation Agreement had recovered the smallest stable agreement contract, but the adjacent Grammar Observation responsibility was still implicit. Recurring relation-shape recognition could be read as pressure inside Observation Agreement even though Observation Agreement explicitly did not own grammar.

## After

Grammar Observation is explicit as an internal implementation-local owner:

- consumes only `ObservationAgreementRecord` values;
- observes recurring syntactic relation shapes;
- preserves supporting agreement records;
- preserves provenance from the agreements;
- preserves recurrence evidence as the candidate agreement strings that recurred by shape;
- emits `GrammarObservationRecord` values;
- rejects promotion to architectural truth.

## Ownership made explicit

### Grammar Observation now owns

- consuming Observation Agreement records;
- observing recurring relation shapes;
- preserving supporting evidence through supporting agreements;
- preserving provenance;
- preserving recurrence evidence;
- emitting grammar observations;
- maintaining a non-promotion boundary.

### Observation Agreement still owns

- consuming supplied lower-level observation records;
- preserving candidate agreement;
- preserving participating observation streams;
- preserving supporting evidence;
- preserving provenance;
- preserving observation independence;
- emitting candidate agreement records.

### Responsibility Recovery remains reserved

Responsibility Recovery remains unrecovered in this slice. Grammar Observation explicitly refuses responsibility recovery and does not infer implementation responsibility from observed relation shapes.

### Additional explicit refusals

Grammar Observation refuses ownership of:

- family recovery;
- lexicon stabilization;
- semantic interpretation;
- architectural truth;
- capability promotion;
- runtime mutation;
- event writes;
- ledger writes;
- repository mutation;
- cluster mutation.

## Compatibility preserved

No compatibility boundary changed.

The slice is internal only. It does not add or modify CLI flags, JSON output, schemas, diagnostic inventory entries, diagnostic shape-audit entries, events, ledger behavior, runtime behavior, or compatibility objects.

## Files changed

- Added `seed_runtime/knowledge/grammar_observation.py`.
- Added `tests/test_grammar_observation.py`.
- Added `grammar_observation_slice_001.md`.

## LOC changed

Current added local line counts:

```text
109 seed_runtime/knowledge/grammar_observation.py
 95 tests/test_grammar_observation.py
146 grammar_observation_slice_001.md
350 total
```

## Tests executed

```text
pytest -q tests/test_observation_agreement.py tests/test_grammar_observation.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result: both passed.

## Questions answered with implementation evidence

### 1. What responsibility was previously implicit?

Recurring relation-shape observation was implicit next to Observation Agreement. Observation Agreement preserved candidate agreement strings and explicitly refused grammar ownership, but no implementation-local owner consumed those agreement records to observe recurring grammar shapes.

### 2. Which recovered architectural boundary became explicit?

```text
Grammar Observation != Responsibility Recovery
```

Grammar Observation is now explicit as a narrow read-only consumer of Observation Agreement records, while responsibility recovery remains outside this slice.

### 3. What does Grammar Observation now own?

Grammar Observation owns only consuming `ObservationAgreementRecord` values, observing recurring relation shapes, preserving supporting agreements, preserving provenance, preserving recurrence evidence, emitting grammar observations, and maintaining a non-promotion boundary.

### 4. What remains owned by Observation Agreement?

Observation Agreement remains the owner of consuming lower-level observation records, preserving candidate agreements, preserving participating observation streams, preserving supporting evidence, preserving provenance, preserving observation independence, and emitting candidate agreement records.

### 5. What remains reserved for Responsibility Recovery?

Responsibility Recovery remains reserved for any future implementation that recovers responsibility ownership. This slice does not infer, stabilize, emit, or promote responsibility.

### 6. Did any compatibility boundary change?

No.

## Remaining implementation gaps

- Responsibility Recovery is still intentionally unrecovered.
- Family Recovery is still intentionally unrecovered.
- Lexicon stabilization is still intentionally unrecovered.
- Grammar Observation remains internal and unregistered; this is intentional because the acceptance criteria required no public compatibility-surface change.
- The relation-shape detector is intentionally small and syntactic. It recognizes only recurring known operator shapes and does not parse Markdown, Python, repositories, runtime state, or semantic meaning.
