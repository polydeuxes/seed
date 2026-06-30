# Pressure Audit Responsibility Characterization

## Executive answer

Pressure Audit is not already fully mature as a decomposed implementation family. It is a small, read-only diagnostic, but its implementation still carries one strong implementation-local compression:

```text
pressure category assessment
```

That boundary is stronger than a generic `Pressure Evidence`, `Pressure Reason`, or `Pressure Recommendation` recovery. The implementation evidence shows five category-specific builders in `seed_runtime/pressure_audit.py`; each builder performs the same bundled sequence for one pressure category:

1. obtains or filters source audit evidence;
2. assigns the category label;
3. computes the score;
4. assembles the evidence payload;
5. writes the pressure reason;
6. creates the recommended inspection command;
7. returns a `PressureItem`.

The highest-confidence recoverable boundary is therefore:

```text
PressureCategoryAssessment
```

or equivalently:

```text
category-local pressure assessment builder
```

This is implementation-local to Pressure Audit. It does not justify a generic Pressure Evidence family, Pressure Visibility redesign, classification framework, schema change, runtime redesign, or behavior change.

Confidence: **medium-high** that one implementation-local category-assessment boundary is recoverable while preserving existing output compatibility.

## Implementation reviewed

Primary implementation reviewed:

- `seed_runtime/pressure_audit.py`
- `tests/test_pressure_audit.py`

Required pressure reports reviewed for scope and counterexamples:

- `pressure_evidence_characterization.md`
- `architectural_pressure_methodology_characterization.md`
- `pressure_visibility_competency_frontier.md`
- `pressure_visibility_evidence_classification_boundary_investigation.md`
- `docs/pressure_audit_design_audit.md`
- `docs/repository_pressure_inventory.md`
- `docs/surviving_pressure_after_decomposition_observation.md`

Commands used:

```bash
pwd && rg --files -g 'AGENTS.md' -g 'pressure*' -g '*pressure*' -g 'completion*' -g '*slice*' | head -200
cat AGENTS.md && sed -n '1,240p' seed_runtime/pressure_audit.py && sed -n '1,240p' tests/test_pressure_audit.py
sed -n '1,220p' pressure_evidence_characterization.md
sed -n '1,220p' architectural_pressure_methodology_characterization.md
sed -n '1,180p' pressure_visibility_competency_frontier.md
for f in pressure_visibility_evidence_classification_boundary_investigation.md docs/pressure_audit_design_audit.md docs/repository_pressure_inventory.md docs/surviving_pressure_after_decomposition_observation.md; do echo ===$f===; sed -n '1,140p' $f; done
rg -n "pressure_audit|PressureItem|format_pressure_audit|recommended_command|Reason|Score|category|evidence" seed_runtime/pressure_audit.py tests/test_pressure_audit.py pressure_evidence_characterization.md architectural_pressure_methodology_characterization.md pressure_visibility_competency_frontier.md pressure_visibility_evidence_classification_boundary_investigation.md docs/pressure_audit_design_audit.md | head -200
```

## Current ownership

### Stable output owner: `PressureItem`

`PressureItem` owns the pressure audit item shape. It stores:

- `category`;
- `score`;
- `evidence`;
- `reason`;
- `recommended_command`.

Its `to_json_dict()` method preserves those fields directly in JSON output. This is an output-shape owner, not an independent evidence, reason, recommendation, ranking, or category owner.

### Stable audit aggregate owner: `PressureAudit`

`PressureAudit` owns the tuple of pressure items and converts the aggregate to JSON. It does not decide category meaning, build evidence, score pressures, or render text.

### Stable orchestration/ranking owner: `build_pressure_audit()`

`build_pressure_audit()` owns the pressure-audit orchestration. It selects the repository root, invokes the current category builders, filters empty/non-positive items, and sorts the surviving items by descending score and then category name.

This is an independent implementation boundary for audit assembly and ranking. The ranking behavior is centralized here rather than duplicated in category builders.

### Stable presentation owner: `format_pressure_audit()`

`format_pressure_audit()` owns text presentation. It renders the title, empty-state message, category heading, score, evidence display, reason, recommended inspection, and summary. It uses `_display_evidence()` for display conversion of dicts and sequences.

This is already separated from the category builders and JSON conversion.

### Compressed category-specific builders

Five local builder functions own the category-specific pressure assessment work:

- `_diagnostic_shape_pressure(root)`;
- `_ownership_pressure(state)`;
- `_capability_pressure(state)`;
- `_orphaned_predicate_pressure(root)`;
- `_fragile_predicate_pressure(root)`.

Each builder returns either `None` or a fully assembled `PressureItem`. That means each builder currently owns the source evidence query/filter, category assignment, score calculation, evidence shape, reason text, and recommended command for its category.

## Recovery questions answered

### Where is observable evidence produced?

Observable evidence is assembled inside each category-specific builder, not by a shared evidence owner:

- Diagnostic Shape evidence is assembled from diagnostic shape summary counts: mismatches, warnings, and unknowns.
- Ownership Attribution evidence is assembled from ownership discrepancy rows filtered to conflicts, then summarized as service ambiguities, storage ambiguities, conflict counts, and dominant conflict.
- Capability evidence is assembled from capability need entries as need frequency, affected subjects, and affected diagnostics.
- Orphaned Predicate evidence is assembled from consumer-audit items filtered to orphaned observation predicates.
- Fragile Predicate evidence is assembled from consumer-audit items filtered to single-consumer observation predicates.

The evidence is observable and structured, but there is no independent Pressure Audit evidence builder or evidence class beyond the `PressureItem.evidence` field.

### Where is pressure reasoning performed?

Pressure reasoning is performed locally in each category-specific builder through the `reason=` string passed to `PressureItem`. The reason text interprets the evidence as pressure-bearing for that category. There is no separate reason owner or reason factory.

### Where are scores assigned?

Scores are assigned inside each category-specific builder:

- Diagnostic Shape score is the sum of mismatches, warnings, and unknowns.
- Ownership Attribution score is the number of conflicting ownership discrepancy rows.
- Capability score is the total number of subject occurrences across capability need entries.
- Orphaned Predicates score is the number of orphaned predicate items.
- Fragile Predicates score is the number of single-consumer predicate items.

Ranking is separate: `build_pressure_audit()` sorts the returned items after score assignment.

### Where are recommendations created?

Recommendations are created inside each category-specific builder as `recommended_command=`. The recommendation is not independently owned; it is packaged with the same builder that creates evidence, score, reason, and category.

### Where are categories assigned?

Categories are assigned inside each category-specific builder as `category=`. There is no category registry or category specification object in Pressure Audit.

### Where is presentation assembled?

Human-readable presentation is assembled in `format_pressure_audit()`. JSON presentation is assembled by `PressureItem.to_json_dict()`, `PressureAudit.to_json_dict()`, and `pressure_audit_json()`. The text formatter is already separated from category-specific evidence/scoring/reason/recommendation construction.

## Responsibilities with independent implementation boundaries

The following responsibilities already have implementation boundaries inside Pressure Audit:

| Responsibility | Current boundary | Evidence |
| --- | --- | --- |
| Item output shape | `PressureItem` | Dataclass fields and JSON conversion. |
| Audit aggregate output shape | `PressureAudit` | Tuple of pressure items and aggregate JSON conversion. |
| Audit orchestration | `build_pressure_audit()` | Invokes category builders, filters empty items, sorts by score/category. |
| Ranking | `build_pressure_audit()` | Sorts by descending score and category name after item construction. |
| Text presentation | `format_pressure_audit()` plus `_display_evidence()` | Renders title, empty state, item sections, evidence display, reason, recommendation, and summary. |
| JSON output conversion | `pressure_audit_json()`, `PressureAudit.to_json_dict()`, `PressureItem.to_json_dict()` | Preserves output fields for JSON consumers. |

These boundaries are small but real. They reduce the case for recovering Presentation, Ranking, or JSON shape as the next boundary.

## Compressed responsibilities

The strongest remaining compression is in each category-specific pressure builder.

For one category, a builder currently combines:

```text
source audit consumption/filtering
+ evidence payload assembly
+ score assignment
+ category label assignment
+ reason construction
+ recommended inspection command construction
+ PressureItem construction
```

This pattern repeats across all five category builders. The repetition is implementation-local and compatibility-preserving: the public output can remain a `PressureItem` while the category assessment data or builder result becomes a local owner.

The compression is not that Evidence and Reason require generic independent owners. The stronger evidence is that category assessment as a whole is the repeated owner that packages evidence, score, reason, category, and recommendation for each local category.

## Counterexamples searched

### Evidence and Reason already independently owned

Counterexample not found in Pressure Audit implementation.

The implementation separates `evidence` and `reason` as fields on `PressureItem`, but field separation is not an independent implementation owner. The category builders still create both fields together.

### Recommendation already independent

Counterexample not found.

`recommended_command` is a field on `PressureItem`, but each command string is created inside the same category builder that creates category, score, evidence, and reason.

### Presentation already separated

Counterexample found and supported.

Text presentation is centralized in `format_pressure_audit()` and `_display_evidence()`, while JSON conversion is owned by `to_json_dict()` methods and `pressure_audit_json()`. Because presentation is already separated, it is not the strongest remaining recovery boundary.

### Ranking already separated

Counterexample found and supported.

Ranking is centralized in `build_pressure_audit()` after the builders return items. Category builders assign scores, but they do not sort or choose final order. Because ranking is already separated, it is not the strongest remaining recovery boundary.

### No meaningful compression remaining inside Pressure Audit

Counterexample rejected.

Meaningful compression remains because five category builders repeatedly package evidence, score, reason, recommendation, and category into one `PressureItem`. This is not large architectural pressure, but it is a concrete implementation-local compression.

## Supported conclusions

1. Pressure Audit is a read-only operational pressure audit over existing visibility surfaces.
2. `PressureItem` is an output shape, not proof of separate Evidence, Reason, Recommendation, Category, or Ranking owners.
3. Presentation is already independently owned well enough for the current implementation.
4. Ranking is already independently owned by the audit builder/sort step.
5. Evidence, reason, score, recommendation, and category are repeatedly co-created inside the category-specific builders.
6. The strongest remaining compression is category-local pressure assessment, not generic Pressure Evidence.
7. Exactly one implementation-local recovery is justified if the recovery is bounded to Pressure Audit and preserves existing JSON/text behavior.

## Unsupported conclusions

The following conclusions are not supported by the implementation evidence reviewed:

- Recover a generic `Pressure Evidence` ownership family.
- Redesign Pressure Visibility.
- Introduce generic classification, schema changes, runtime redesign, or behavior changes.
- Treat `PressureItem.evidence` as an already independent evidence owner.
- Treat `PressureItem.reason` as an already independent reason owner.
- Treat `recommended_command` as an already independent recommendation owner.
- Recover Presentation as the highest-confidence remaining boundary.
- Recover Ranking as the highest-confidence remaining boundary.

## Recommendation on exactly one implementation-local recovery

Yes. There is sufficient implementation evidence to justify recovering exactly one implementation-local ownership boundary:

```text
PressureCategoryAssessment
```

Scope:

```text
Inside seed_runtime/pressure_audit.py only.
```

Boundary responsibility:

```text
Represent one category's local pressure assessment: category label, score, evidence payload, reason, and recommended inspection command, produced from one existing source-audit query/filter.
```

Compatibility expectation:

```text
Existing PressureItem JSON and text output should remain unchanged.
```

Why this boundary, and not another:

- It matches the repeated implementation pattern across all current category builders.
- It stays inside Pressure Audit.
- It avoids generic Pressure Evidence or Pressure Visibility claims.
- It preserves the existing `PressureItem` output contract.
- It does not require schema changes, new diagnostics, runtime redesign, or behavior changes.

## Confidence

Confidence is **medium-high**.

High-confidence evidence:

- Category builders repeatedly package the same set of concerns.
- Ranking and presentation already have separate local owners.
- Prior pressure reports explicitly warn that `PressureItem.evidence` is not enough to recover a generic Pressure Evidence owner.

Confidence limits:

- Pressure Audit is small, so the recovery should remain small.
- The implementation does not yet prove a need for multiple new classes or a registry.
- The boundary should be recovered only as a local compatibility-preserving refactor if future code work is requested.

## Final answer to acceptance question

Pressure Audit is partially mature but not fully decomposed.

It carries one remaining implementation-local compressed responsibility:

```text
category-local pressure assessment
```

The single highest-confidence boundary is:

```text
PressureCategoryAssessment
```

This conclusion is implementation-local to `seed_runtime/pressure_audit.py` and does not authorize any broader pressure methodology, Pressure Visibility, generic evidence, classification, schema, or runtime redesign.
