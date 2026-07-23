# Operational Measurement, Baseline, and Preservation Amendment 001

## Status

Canonical amendment record. This record documents the cross-examination that amended the Book; it is not independent authority apart from the clauses amended below.

## Central Finding

When Seed observes its own operation, Seed need not preserve every operational measurement. Seed must preserve sufficient evidence or compressed standing to retain its materially sufficient understanding of operational reality. The operator is not the constitutional subject: diagnostic display, external capture, or omission of capture does not decide Seed preservation.

## Canonical clauses examined

- `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `06-state-and-projection/projection-and-current-state.md`
- `07-operational-realization/execution-and-recording.md`
- `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `08-authority-communication-and-stopping/stopping-and-completion.md`
- `concordance.md`
- `unresolved.md`

## Repository witnesses examined

- `book_of_seed/operational_timing_and_preservation_recovery_001.md`
- `seed_runtime/execution_status.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/observations.py`
- `scripts/seed_local.py`
- `tests/test_execution_status.py`
- `tests/test_runtime_self_observation.py`
- `tests/test_projection_store.py`
- `tests/test_fact_index.py`

## PR 1894 findings accepted

PR 1894 correctly found current implementation testimony for individual invocation timing measurements, cache-status testimony, projection and ingestion phase measurements, ordinary runtime/resource observations, transient execution-status visibility, and rebuildable projection/read-model/index snapshots.

PR 1894 also correctly found no retained timing series, operational timing baseline, expected-duration standing, tolerance or comparison authority, deviation or regression testimony, baseline-transition testimony, or Seed consumer that uses timing evidence to constrain later movement.

## PR 1894 findings qualified or corrected

`ExecutionStatus` is not operational timing testimony. `ProgressCadence` uses a monotonic clock to decide whether to emit progress, but that cadence calculation is not an operational-duration artifact whose loss requires preservation. Transient status visibility does not automatically become retained knowledge.

PR 1894's preservation-loss pressure is accepted only as implementation testimony: current transient timings would be lost after process exit. That non-rebuildability does not by itself make every sample preservation-worthy.

## Recovered constitutional distinctions

Seed must distinguish performing an operation, measuring an operation, preserving operation testimony, summarizing ordinary operational behavior, comparing a measurement, recognizing a material deviation, establishing changed ordinary behavior, and using operational understanding in later movement.

## Operational measurement standing

An operational measurement is testimony that a particular bounded operation instance, under particular known conditions, was measured by a declared method and exhibited particular operational behavior. Possible dimensions include operation identity, operation-instance scope, measured phase, duration or resource behavior, method or clock, input scale, cache condition, environment or authority context, completion condition, and observation time. No implementation must possess every dimension.

An operational measurement does not by itself establish ordinary behavior, expected future duration, capability availability, operation correctness, operation failure, material degradation, or permission to act.

## Operational baseline standing

An operational baseline is retained, scoped, evidence-supported understanding of ordinary operational behavior under declared conditions. It is not necessarily a database table, raw timing history, average, threshold, or runtime artifact. It is not a predicted future duration.

A baseline must preserve enough context to avoid comparing constitutionally different subjects: cache hit and cache miss, full State rebuild and incremental replay, fact-view inventory construction and subject/predicate selection, small and large input, or different environment and authority conditions.

## Tolerance/comparison authority

A tolerance is not merely a number. A comparison boundary requires bounded authority for the baseline being applied, the operation and conditions covered, the purpose of comparison, the permitted variation, and the method by which the boundary was established. The Book does not decide whether future tolerance stands inside baseline standing, as a consumer-local comparison rule, or as a separate warrant; it requires preserved authority and purpose whichever implementation form is later chosen.

Difference from one prior sample is not material deviation.

## Deviation testimony

A measurement outside a comparison boundary is distinct from an established failure, lost capability, changed operational regime, cause, or consequence. Material deviation testimony must preserve the measured operation, applicable baseline or comparison standing, relevant context, observed difference, authority and purpose of comparison, and remaining uncertainty.

## Baseline transition

A baseline transition is evidence-supported establishment that ordinary operational behavior materially changed from one bounded regime to another. One unusual sample is insufficient. Repeated samples are not automatically sufficient merely by count; establishment remains bounded by scope, conditions, comparison method, evidence sufficiency, conflict awareness, and temporal standing.

Once changed ordinary behavior is lawfully established, Seed may preserve the prior baseline, transition standing, new baseline, and sufficient supporting evidence without permanently retaining every contributing raw measurement.

## Preservation and discard rule

Seed need not preserve every operational measurement. Seed must preserve sufficient evidence or compressed standing to retain its materially sufficient understanding of operational reality.

A measurement within an established tolerance may be discarded when its loss does not alter or erase that understanding. A material deviation must preserve sufficient measurement and comparison context to retain the challenge to the prior understanding. Every discarded sample removes hypothetical future analytical possibility, but that alone is not sufficient preservation warrant.

The inability to rebuild a raw measurement does not automatically require preservation. Preservation is required when discarding the artifact would erase material evidence or understanding of reality that is not otherwise retained.

## Rebuildability analysis

A rebuildable derived artifact need not be preserved when the understanding it carries can be faithfully rebuilt from retained evidence. A non-rebuildable raw testimony artifact is not automatically preservation-worthy. Preserved compressed understanding can lawfully stand in place of every raw sample when it retains the material understanding needed by its bounded consumers.

Current examples: a projection snapshot is generally rebuildable from ledger-supported evidence; a summary snapshot is generally rebuildable from projected State; a fact-index snapshot is generally rebuildable from projected State. The elapsed duration of one invocation is not reconstructable after process exit, and cache condition at a historical invocation is not necessarily reconstructable from current cache state. Rerunning the operation is not reconstructing the prior operation instance.

## Seed-consumption boundary

Operational understanding could later constrain budget sufficiency, stopping, route selection, capability reachability, degradation inquiry, cache strategy, or bounded refusal, but only through bounded standing, authority, sufficiency, admissibility, and consumer responsibility. This amendment does not canonize a selector, threshold, automatic action, or implementation consumer.

Diagnostic rendering is not Seed-consumable knowledge by identity. Operator capture is not Seed preservation; operator omission is not permission for Seed to forget; Seed preservation is not obligation to expose every sample externally.

## Clauses amended

- `07-operational-realization/execution-and-recording.md` now defines operational measurement, baseline, comparison, deviation, transition, and measurement preservation boundaries.
- `06-state-and-projection/projection-and-current-state.md` now distinguishes rebuildable derived artifacts, reconstructed current condition, and irrecoverable historical invocation testimony.
- `05-evidence-and-knowledge/recording-and-knowledge-extraction.md` now separates diagnostic rendering and operator capture from Seed preservation.
- `concordance.md` now indexes operational measurement, operational baseline, material deviation, baseline transition, and rebuildability.

## Clauses intentionally preserved

Artifact shape still does not establish standing. Projection still does not become source truth or constitutional law. Diagnostic findings remain diagnostic-scope unless separately promoted. Execution and recording remain separate. Transient status visibility remains visibility, not retained knowledge. Operational evidence does not independently authorize movement.

## What remains absent in implementation

No operational baseline, tolerance comparison, deviation artifact, baseline-transition artifact, or timing-based movement consumer is currently implemented, according to current repository testimony.

## What remains Unknown

It remains Unknown which future operational consumers, if any, will require retained operational baselines; which comparison authority form would be warranted for a particular operation; which raw measurements would be materially necessary for a future baseline; and which implementation surface should preserve deviation or transition testimony if such a surface is later authorized.
