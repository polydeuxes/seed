# External Material Surface Feature Projection Slice 001

## Recovered responsibility

This slice recovers exactly one canonical responsibility:

> Project raw, evidence-preserving line-length features and deterministically composed region length sequences from an existing `ExternalMaterialStructuralProjection`.

The bounded question is:

> For each mechanically projected line and nonblank region, what exact raw length structure is visible without interpreting the text?

## Starting evidence verified

The repository already contains the completed road:

```text
bounded hash-identified exact text
→ ExternalMaterialStructuralProjection
→ stable line records
→ maximal nonblank contiguous regions
```

The structural projection preserves manifest/source/artifact identity, artifact hash, raw line text, stable line IDs, stable region IDs, one-based line numbers, zero-based half-open character coordinates, `character_count`, `has_line_terminator`, blank/nonblank state, and region line membership.

The latest topology audit concluded:

```text
C. Mechanical line/region projection exists,
but raw surface-feature projection is a genuinely missing responsibility.
```

and:

```text
2. Cross-substrate recurrence improves probe questions
but does not yet warrant comparison implementation.
```

## Producer

The producer is:

```text
project_external_material_surface_features(structural_projection)
```

It consumes exactly one existing `ExternalMaterialStructuralProjection` and does not reopen files, reacquire exact text, inspect manifests independently, fetch remote material, revalidate source authority, reinterpret material, or generate recurrence conclusions.

## Input artifact

The input artifact is the existing immutable structural projection:

```text
ExternalMaterialStructuralProjection
```

It remains the owner of exact text identity, line segmentation, region segmentation, and raw line preservation.

## Output artifact

The output artifact is:

```text
ExternalMaterialSurfaceFeatureProjection
```

It contains:

```text
manifest_id
source_id
artifact_id
artifact_hash
structural_projection_identity
feature_convention
feature_convention_notes
line_features
region_features
projection_unknowns
boundary_notes
read_only
writes_event_ledger
mutates_cluster
```

No standalone random projection ID is introduced.

## Consumer

The consumers added or updated are:

```text
seed --external-material-surface-features JSON_FILE
```

and the supervised grammar campaign for `selected_lesson_006.txt`.

Both consumers are read-only.

## Feature convention

The feature convention is:

```text
external_material_surface_feature_projection_v1
```

It states that line numbers remain one-based, character counts use Python string characters, raw line text is not copied into the artifact, content-character count excludes only the recorded line terminator, all other whitespace remains counted, region sequences preserve physical line order, and no normalization or interpretation occurs.

## Terminator-separation rule

For every structural line:

```text
raw_character_count = structural line character_count
content_character_count = raw_character_count - mechanical terminator length
line_terminator_character_count = raw_character_count - content_character_count
```

The terminator length is determined mechanically from the preserved structural line text and `has_line_terminator` behavior:

- `\r\n` counts as 2 characters.
- `\n` counts as 1 character.
- `\r` counts as 1 character.
- A line without a recorded terminator excludes 0 terminator characters.

No conversion from `\r\n` to `\n` or from `\r` to `\n` occurs.

## Line feature fields

Each line feature preserves:

```text
line_id
line_number
raw_character_count
content_character_count
line_terminator_character_count
is_blank
has_line_terminator
unknowns
```

Raw line text is not duplicated into the surface-feature artifact.

## Region composition rule

Each region feature preserves:

```text
region_id
line_ids
line_count
raw_line_character_count_sequence
content_character_count_sequence
total_raw_character_count
total_content_character_count
unknowns
```

Region features are composed only from referenced line features in existing physical order. No semantic regions are reconstructed.

## Raw-text ownership

Raw line text remains owned by `ExternalMaterialStructuralProjection`. The surface-feature projection references the artifact hash, line IDs, and region IDs and preserves only derived feature values.

## Validation boundary

The producer validates only the structural integrity it directly depends on:

- unique line IDs;
- unique region IDs;
- region references point to existing lines;
- region line order is deterministic;
- region `line_count` agrees with referenced line IDs;
- structural line `character_count` matches preserved line text length;
- `has_line_terminator` has a mechanically visible terminator when true.

It does not duplicate upstream artifact-hash, manifest, or source-authority validation.

## Boundary notes

Human and JSON output expose these boundary notes:

```text
Surface features are deterministic measurements of an existing structural projection.
Content-character count excludes only the recorded line terminator.
No case, punctuation, whitespace, or Unicode normalization occurs.
Line-length and region-length arrangements do not establish semantic structure.
A recurring feature arrangement does not establish correspondence or shared responsibility.
This projection does not identify headings, rules, examples, exercises, code, prose, or grammar.
This projection is not runtime Evidence, Fact, candidate verification, or capability evidence.
```

## Selected lesson integration

The supervised grammar campaign now consumes the canonical surface-feature projection for:

```text
selected_lesson_006.txt
```

Identity preserved:

```text
Project Gutenberg eBook #7010
Graded Lessons in English
LESSON 6. ANALYSIS.
SHA-256: 01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963
```

The campaign continues to state:

```text
Seed projected length features.
The campaign author still interpreted headings, rules, examples,
exercises, contrasts, support, and contradiction.
```

## Verified selected-lesson feature sequence

The real selected lesson structural projection produces:

```text
4 projected lines
1 projected nonblank region
content-character sequence: [248, 464, 433, 479]
```

These values are computed from the existing structural projection rather than installed as canonical material facts.

## `AGENTS.md` recurrence probe

The same producer projects the bounded repository `AGENTS.md` structural projection.

Preserved identity:

```text
SHA-256: 60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed
```

Mechanically observed four-line region content-character sequences include:

```text
[47, 152, 56, 61]
[60, 49, 39, 70]
```

## Neutral recurrences observed

Neutral observation only:

```text
both artifacts contain a four-line nonblank region
```

and:

```text
their content-character sequences differ
```

## Semantic correspondences refused

This slice refuses these conclusions:

```text
the regions have the same responsibility
the lesson region corresponds to an instruction block
region length establishes semantic similarity
```

## First remaining manual handoff

The first remaining manual handoff is:

```text
line/region length features
→ bounded structural comparison
```

## Exact next bounded question

The exact next bounded question is:

> Which bounded structural comparison artifact, if any, can compare line-count and length-sequence features across independent artifacts without inferring semantic correspondence?

## CandidateExternalGrammarSet compatibility

`CandidateExternalGrammarSet` is unchanged. No candidate schema, candidate generation, candidate ranking, or candidate verification behavior was modified.

## Testimony-binding compatibility

`ExternalMaterialTestimonyBindingSet` is unchanged. The testimony-binding schema and meanings remain preserved.

## Structural-projection compatibility

`ExternalMaterialStructuralProjection` is compatibility-preserved. This slice consumes it without changing its ownership of raw text, line segmentation, region segmentation, identity validation, human output, or JSON output.

## Read-only guarantees

The new projection preserves:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

The producer and renderers append no events, create no Observations, create no Evidence, create no Facts, modify no projected State, mutate no repository or cluster state, and perform no network access.

## Compatibility answer

Did this slice change any existing compatibility boundary?

```text
No.
```

## Files changed

```text
campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py
external_material_surface_feature_projection_slice_001.md
scripts/seed_local.py
seed_runtime/diagnostic_inventory.py
seed_runtime/diagnostic_shape_audit.py
seed_runtime/external_material_surface_feature_projection.py
tests/test_external_material_surface_feature_projection.py
```

## LOC delta

`git diff --numstat` before commit reported 831 insertions and 1 deletion across 7 files, including the canonical projection implementation, focused tests, supervised-campaign integration, diagnostic registration, CLI surface, and this slice report.

## Tests executed

```text
pytest -q tests/test_external_material_surface_feature_projection.py
pytest -q tests/test_external_material_surface_feature_projection.py tests/test_external_material_structural_projection.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Remaining missing roads

Left unresolved:

```text
line/region length features
→ bounded structural comparison
```

```text
structural comparison
→ recurrence testimony
```

```text
external structure
+
repository structure
→ candidate correspondence
```

```text
candidate correspondence
→ recovered responsibility
```

```text
mechanical region
→ semantic annotation
```

```text
exact material spans
→ autonomous structural candidate generation
```
