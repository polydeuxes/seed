# Pressure Audit Smallest Owner Investigation

## Executive answer

`PressureCategoryAssessment` is not proven to be the smallest recoverable implementation owner by the current implementation. The smallest repeated implementation sequence inside every current category builder is:

```text
read an existing audit surface
→ derive a category-local positive score
→ stop when score is non-positive
→ assemble category-local evidence
→ attach category/reason/recommended command labels
→ return a PressureItem
```

The first common stopping point is after the category-local audit result has been reduced to a positive score and evidence payload, but before the final `PressureItem` is constructed. At that point the recurring artifact is not currently named in code, but it is visible as the repeated local variables and literals that feed the `PressureItem` constructor: `score`, `evidence`, `reason`, `recommended_command`, and `category`.

However, the implementation evidence is not strong enough to justify recovering a slice now. The repeated owner is smaller than a whole category assessment, but it is still only implicit: no intermediate type, helper, or test assertion currently names or consumes it independently. The current proposed boundary should therefore be treated as not demonstrably minimal, but also not ready for ownership recovery without further implementation pressure.

## Implementation reviewed

Only the requested files were reviewed:

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`

No new diagnostic, audit, probe, CLI flag, recordable output, or runtime behavior was added. This report is an investigation artifact only.

## Current pressure audit structure

`PressureItem` is the emitted row shape for a pressure category. It carries five fields: `category`, `score`, `evidence`, `reason`, and `recommended_command`.

`build_pressure_audit` calls five private category builders, filters out `None` and non-positive scores, then sorts by descending score and category name:

```text
_diagnostic_shape_pressure(root)
_ownership_pressure(state)
_capability_pressure(state)
_orphaned_predicate_pressure(root)
_fragile_predicate_pressure(root)
```

The category builders are the implementation corridor under review.

## Repeated builder sequence

### Diagnostic Shape

Implementation sequence:

1. Selects a repo root variant for the diagnostic shape audit.
2. Calls `build_diagnostic_shape_audit` and summarizes it.
3. Computes `score` from `mismatches + warnings + unknown`.
4. Returns `None` if `score <= 0`.
5. Builds evidence from `mismatches`, `warnings`, and `unknowns`.
6. Constructs `PressureItem` with category, score, evidence, reason, and recommended command.

Category-specific work:

- repo-root fallback logic;
- diagnostic shape summary construction;
- score formula using summary counts;
- evidence keys tied to shape-audit summary fields.

Repeated work:

- derive score;
- suppress non-positive pressure;
- assemble evidence;
- attach static category label, reason, and command;
- return `PressureItem`.

### Ownership Attribution

Implementation sequence:

1. Calls `build_ownership_discrepancies(state)`.
2. Filters rows to those with `row.conflict`.
3. Builds `conflict_counts` and `kind_counts` counters.
4. Computes `score = len(rows)`.
5. Returns `None` if `score <= 0`.
6. Derives `dominant` conflict.
7. Constructs `PressureItem` with category, score, evidence, reason, and recommended command.

Category-specific work:

- conflict filtering;
- conflict and kind counters;
- dominant conflict selection;
- ownership-specific evidence names.

Repeated work:

- derive score;
- suppress non-positive pressure;
- assemble evidence;
- attach static category label, reason, and command;
- return `PressureItem`.

### Capability

Implementation sequence:

1. Calls `build_capability_needs(state)`.
2. Computes `score` as total subject occurrences across entries.
3. Returns `None` if `score <= 0`.
4. Reads `top = entries[0]` after the positive-score guard.
5. Builds evidence from capability frequencies, affected subjects, and affected diagnostics.
6. Constructs `PressureItem` with category, score, evidence, reason, and recommended command.

Category-specific work:

- total-subject-occurrence score formula;
- first-entry top-need selection;
- set comprehensions over subjects and diagnostics;
- capability-specific evidence names.

Repeated work:

- derive score;
- suppress non-positive pressure;
- assemble evidence;
- attach static category label, reason, and command;
- return `PressureItem`.

### Orphaned Predicates

Implementation sequence:

1. Calls `build_consumer_audit(root).items`.
2. Filters to `observation_predicate` items where `item.orphaned` is true.
3. Returns `None` if no items remain.
4. Uses `len(items)` as the score.
5. Builds evidence from orphan count and predicate names.
6. Constructs `PressureItem` with category, score, evidence, reason, and recommended command.

Category-specific work:

- orphaned predicate filter;
- orphan-specific evidence key.

Repeated work:

- derive score from matching items;
- suppress non-positive/empty pressure;
- assemble evidence;
- attach static category label, reason, and command;
- return `PressureItem`.

### Fragile Predicates

Implementation sequence:

1. Calls `build_consumer_audit(root).items`.
2. Filters to `observation_predicate` items where `item.consumer_count == 1`.
3. Returns `None` if no items remain.
4. Uses `len(items)` as the score.
5. Builds evidence from single-consumer count and predicate names.
6. Constructs `PressureItem` with category, score, evidence, reason, and recommended command.

Category-specific work:

- single-consumer predicate filter;
- fragile-specific evidence key.

Repeated work:

- derive score from matching items;
- suppress non-positive/empty pressure;
- assemble evidence;
- attach static category label, reason, and command;
- return `PressureItem`.

## Recurring implementation work

The identical work across all category builders is not the source query or the evidence payload. It is the pressure-row assembly contract:

```text
produce a numeric pressure score
skip when no pressure exists
produce an evidence mapping
attach human-facing reason
attach inspection command
emit PressureItem
```

The pressure audit aggregator repeats the same expectation at the outer layer by discarding `None` and non-positive `PressureItem` values before sorting. This means positivity is checked both inside category builders and again by the aggregator.

The tests also preserve this repeated row contract rather than a category-assessment type. They assert rendered category, score, evidence, and recommended command for an ownership pressure; assert each category's evidence fields; assert all emitted recommended commands start with `seed --`; and assert the empty-state path produces zero pressures and no ledger events.

## Parameterized work

The following work is merely parameterized across builders:

- category label: `Diagnostic Shape`, `Ownership Attribution`, `Capability`, `Orphaned Predicates`, `Fragile Predicates`;
- recommended command: each builder supplies a static `seed --...` command;
- reason text: each builder supplies a category-specific sentence, sometimes interpolating score or top capability;
- evidence key names: each builder names its payload keys;
- positive-pressure guard: all builders skip empty pressure, although two express it as `score <= 0` and two express it as `if not items` before using `len(items)`.

The parameterization is implementation-local. It does not imply a generic evidence framework or schema change.

## Work that actually differs between categories

The category-specific work is the source-local reduction from an existing audit surface into pressure inputs:

- Diagnostic Shape reduces shape-audit summary mismatch/warning/unknown counts.
- Ownership Attribution reduces conflict-bearing ownership discrepancy rows, counters, and dominant conflict.
- Capability reduces capability-need entries into subject occurrence counts and affected sets.
- Orphaned Predicates reduces consumer-audit items by orphaned observation predicates.
- Fragile Predicates reduces consumer-audit items by single-consumer observation predicates.

These differences are substantial enough that the source query/filter and local transformation should not be treated as identical work.

## First recurring implementation stopping point

A builder could naturally stop after it has created the data needed to construct a pressure row but before instantiating `PressureItem`:

```text
category-local source reduction
→ score/evidence/reason/command/category bundle
STOP
→ PressureItem construction
```

The artifact at that stop would be an implementation-local pressure row candidate or pressure item input bundle. The current code does not name this artifact; it is visible only as the repeated constructor arguments.

This is smaller than `PressureCategoryAssessment` because it excludes the category-specific source query/filter and local transformation. It is also earlier than `PressureItem` because the recurring result is visible as constructor inputs before the dataclass is instantiated.

## Counterexamples considered

### Counterexample: `PressureCategoryAssessment` is already smallest

Evidence supporting this counterexample:

- Every builder currently owns its source query/filter, score calculation, evidence payload, reason, command, and `PressureItem` construction in one function.
- Tests interact only with emitted pressure items and formatted/JSON output; no test names a smaller intermediate artifact.
- The implementation has no `PressureCategoryAssessment` class and no independent category-assessment result type to compare against.

Evidence weakening this counterexample:

- The source reduction differs by category, but the positive-pressure row assembly repeats in every builder.
- `PressureItem` construction uses the same field set every time.
- Positive-pressure filtering is repeated inside each builder and again in the aggregate builder.

Conclusion: `PressureCategoryAssessment` is not proven minimal, but the smaller owner is not yet first-class.

### Counterexample: `PressureItem` is naturally the first stable artifact

Evidence supporting this counterexample:

- `PressureItem` is the first named dataclass returned by category builders.
- `PressureAudit` stores a tuple of `PressureItem` objects.
- JSON and formatted output operate on `PressureItem` fields.
- Tests assert behavior through pressure items in JSON/rendered output, not through a pre-item candidate.

Evidence weakening this counterexample:

- Every builder assembles the same constructor input shape before `PressureItem` exists.
- A builder could stop after producing the score/evidence/reason/command/category bundle and before constructing the dataclass without changing the source reduction work.

Conclusion: `PressureItem` is the first stable named artifact, but not necessarily the first recurring implementation stopping point.

### Counterexample: no smaller recurring owner exists

Evidence supporting this counterexample:

- Source queries and local transformations differ significantly.
- Evidence payloads use category-specific keys and value derivations.
- Reason strings are category-specific.
- The current tests do not isolate shared row assembly.

Evidence weakening this counterexample:

- The score/evidence/reason/command/category constructor input shape recurs in every builder.
- The skip-empty-pressure pattern recurs in every builder.
- Recommended inspection is a required repeated field across all emitted pressures.

Conclusion: a smaller recurring owner exists conceptually in the implementation, but the repository has not yet made it independently owned.

## Supported conclusions

1. The smallest repeated implementation sequence is positive pressure row assembly: compute or receive a category-local score, skip non-positive pressure, assemble evidence, attach category/reason/command, and emit `PressureItem`.
2. Category label, reason text, recommended command, evidence keys, and positive-score threshold are parameterized.
3. The first recurring stopping point is before `PressureItem` construction, after category-local reduction has produced the constructor-input bundle.
4. `PressureCategoryAssessment` is not demonstrably the smallest stable owner because it would include category-specific source reductions that do not repeat.
5. The smaller implementation-local owner is an unnamed pressure item input/candidate bundle, not a broad evidence abstraction and not a redesign.
6. There is not sufficient implementation evidence to justify a slice now, because no code or test currently names, consumes, or preserves that pre-`PressureItem` artifact independently.

## Unsupported conclusions

The reviewed implementation does not support these conclusions:

- that a generic pressure evidence abstraction should be introduced;
- that pressure categories should be compared or normalized against each other;
- that runtime schema, diagnostic inventory, or CLI behavior should change;
- that ownership recovery should proceed immediately;
- that `PressureCategoryAssessment` exists as a current code artifact;
- that `PressureItem` is the only possible stable boundary.

## Confidence

Medium.

The repeated constructor-input sequence is visible across all five builders, and the category-specific reductions are also visible. Confidence is limited because the smaller owner is implicit only. The repository currently names `PressureItem` and `PressureAudit`, but it does not name or test a pre-item candidate artifact.

## Recommendation on whether the proposed boundary is already minimal

The current proposed `PressureCategoryAssessment` boundary should not be considered proven minimal. A smaller recurring implementation owner is compressed inside the builders: the positive pressure item candidate assembled from score, evidence, category label, reason, and recommended inspection command.

Do not recover that owner yet. The implementation demonstrates recurrence, but not enough independent ownership pressure. The appropriate answer for recovery readiness is:

```text
Insufficient implementation evidence.
```
