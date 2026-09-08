# External Material Structural Projection Slice 001

## Recovered responsibility
Mechanically project stable line records and maximal nonblank contiguous line regions from one already bounded, hash-identified external text artifact. Human interpretation remains outside this producer.

## Producer
`seed_runtime.external_material_structural_projection.project_external_material_structure`.

## Input artifact
`ExternalMaterialStructuralProjectionRequest` plus an existing `ExternalMaterialManifest` and selected `ExternalMaterialSelectedArtifactRecord`. The caller supplies `manifest_id`, `source_id`, `artifact_id`, `expected_artifact_hash`, `encoding`, `exact_text`, and `unknowns`.

## Output artifact
`ExternalMaterialStructuralProjection` with immutable selected identity, artifact hash, encoding, projected line records, projected nonblank-region records, projection unknowns, boundary notes, and read-only guarantees.

## Consumer
The read-only `seed --external-material-structure JSON_FILE` surface and the supervised grammar campaign consume the projection. Candidate grammar construction and testimony binding remain compatible and unchanged.

## Exact text identity validation
The producer resolves the selected artifact from the manifest and validates manifest, source, artifact, source-artifact parentage, expected hash, supplied text encodability, SHA-256 over `exact_text.encode(encoding)`, line count, and character count before projecting. Deterministic failures include `unknown_manifest`, `unknown_source`, `unknown_artifact`, `source_artifact_mismatch`, `unsupported_encoding`, `text_encode_failure`, `artifact_hash_mismatch`, `line_count_mismatch`, and `character_count_mismatch`.

## Encoding convention
The supplied deterministic encoding is used directly. The canonical campaign uses UTF-8. No remote resource or local file discovery occurs inside the producer.

## Line-splitting convention
Empty text has zero physical lines. Non-empty text uses Python `splitlines(keepends=True)` and does not add a synthetic final empty line after a trailing terminator.

## Character-coordinate convention
Line numbers are one-based and inclusive. Character offsets are zero-based half-open offsets over the exact Python string. A line's range includes its line terminator when one exists.

## Line identity rule
Line IDs are deterministic SHA-256-derived identifiers over the projection convention, artifact identity, artifact hash, line kind, and coordinates. Content meaning is not used.

## Region identity rule
Region IDs are deterministic SHA-256-derived identifiers over the projection convention, artifact identity, artifact hash, region kind, region coordinates, and projected line IDs.

## Blank/nonblank behavior
Blankness is mechanical: after removing only the line terminator from the line record, `content.strip() == ""` is blank. Blank lines remain line records. Maximal contiguous nonblank lines become regions. Consecutive blank lines do not create empty regions.

## Empty-artifact behavior
An empty exact text is valid when its hash, declared line count, and declared character count match. It projects zero line records and zero nonblank regions.

## Boundary notes
The projection exposes the following notes: lines and regions are mechanical projections; line boundaries are not semantic boundaries; nonblank regions are not paragraphs, sections, headings, rules, examples, or exercises; no prose comprehension, grammar inference, semantic labeling, candidate generation, or normalized similarity occurs; raw case, punctuation, whitespace, and newline distinctions remain unnormalized; and this projection is not runtime Evidence, Fact, or grammar verification.

## Supervised campaign integration
The campaign now records the structural projection for `selected_lesson_006.txt` while explicitly preserving that Seed projected lines and nonblank regions and that the campaign author still identified heading, rule, example, exercise, contrast, support, and contradiction. The selected lesson bytes, candidate schema, testimony binding schema, and annotation meanings were not changed.

## Cross-substrate recurrence probe
Selected repository artifact: `AGENTS.md`.

- SHA-256: `60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed`
- line count: `61`
- nonblank-region count: `22`

The same producer and schema project the repository artifact; no parser specific to Markdown or repository files was added.

## Recurring neutral properties
Both artifacts contain ordered lines. Both artifacts can contain blank-delimited regions. Both use stable coordinate-addressed regions. Both preserve exact source identity and hash.

## Unsupported semantic correspondences
This slice refuses claims that a lesson region is equivalent to a code block, a heading is equivalent to a class, a website section is equivalent to a module, or that the two artifacts share semantic grammar.

## CandidateExternalGrammarSet compatibility
`CandidateExternalGrammarInput` and `CandidateExternalGrammarSet` were not changed and do not require structural projections.

## Testimony-binding compatibility
`ExternalMaterialTestimonyBindingSet` was not changed. Existing testimony references may continue using exact line coordinates.

## Read-only guarantees
The producer and renderers set `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`. They do not append events, create Observations, Evidence, or Facts, mutate projected State, acquire network material, or execute tools.

## Compatibility answer
Did this slice change any existing compatibility boundary?

No.

## Files changed
- `seed_runtime/external_material_structural_projection.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py`
- `tests/test_external_material_structural_projection.py`
- `external_material_structural_projection_slice_001.md`

## LOC delta
Recorded from pre-commit `git diff --stat` and `git diff --numstat` during this slice.

## Tests executed
- `pytest -q tests/test_external_material_structural_projection.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Exact next bounded question
For mechanically projected line and nonblank regions, what raw surface-feature projection can be computed without prose interpretation?

## Remaining missing roads
- mechanical regions → raw surface-feature projection
- surface features → structural comparison
- external structure + repository structure → candidate recurrence or correspondence
- structural recurrence → candidate responsibility recovery
- material region → semantic annotation
- structural comparison → candidate grammar generation

## Real selected lesson result
Project Gutenberg eBook #7010, `selected_lesson_006.txt`, SHA-256 `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`, projects 4 lines and 1 mechanically projected nonblank region.
