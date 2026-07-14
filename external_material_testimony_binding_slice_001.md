# External Material Testimony Binding Slice 001

## Recovered responsibility

This slice recovers one implementation-local responsibility: validate caller-supplied testimony reference IDs against a bounded caller-supplied external-material manifest, then preserve the mechanically valid bindings as one immutable read-only artifact.

The bounded question answered is referential only: Seed can establish that a testimony reference resolves to an existing manifest, source, selected artifact, expected artifact hash, exact bounded span, and optional annotation identity without interpreting material or deciding whether the span supports testimony.

## Campaign evidence supporting recovery

The supervised grammar apprenticeship campaign already preserved Project Gutenberg eBook #7010, `Graded Lessons in English`, `LESSON 6. ANALYSIS.`, as `selected_lesson_006.txt` with SHA-256 `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963` and selected artifact lines 1-4. Existing candidate grammar artifacts preserved testimony references only as opaque strings. This slice binds those strings to caller-supplied material coordinates while leaving candidate meaning unchanged.

## Selected implementation boundary

Canonical code lives in `seed_runtime/external_material_testimony_binding.py`. It is substrate-neutral and uses no Project Gutenberg-specific, English-specific, lesson-specific, corpus, acquisition, interpretation, Evidence, Fact, or State concepts.

## Producer

`validate_external_material_testimony_bindings(...)` is the producer. It consumes an `ExternalMaterialManifest`, binding requests, and set unknowns, then returns an `ExternalMaterialTestimonyBindingSet` or raises a deterministic validation error.

## Manifest input artifact

`ExternalMaterialManifest` preserves:

- `manifest_id`
- `sources`
- `selected_artifacts`
- `annotations`
- `manifest_unknowns`

Source records preserve source identity, kind, hash, location, reported title/creator, provenance, and unknowns. Selected artifact records preserve artifact identity, parent source identity, artifact hash, artifact location, line count, character count, selection bounds, and unknowns. Annotation records preserve annotation identity, artifact identity, line span, optional character span, supplier, kind, and unknowns.

The manifest does not verify remote source identity or source authority.

## Binding-request input artifact

`ExternalMaterialTestimonyBindingRequest` preserves:

- `testimony_reference_id`
- `manifest_id`
- `source_id`
- `artifact_id`
- `expected_artifact_hash`
- `start_line`
- `end_line`
- optional character bounds
- optional annotation ID
- unknowns

The testimony reference ID remains a downstream stable string, not Evidence identity, Fact identity, candidate identity, source identity, annotation identity, or support-verification identity.

## Output artifact

`ExternalMaterialTestimonyBindingSet` preserves `manifest_id`, immutable validated bindings, `set_unknowns`, boundary notes, and read-only guarantees. Each binding uses `binding_status = reference_validated` only.

Unsupported semantic fields such as support, contradiction, authority, correctness, confidence, warrant, admissibility, and grammar verification are not emitted.

## Consumer

The immediate consumers are read-only diagnostics and the noncanonical supervised grammar campaign. Candidate grammar construction remains unchanged and continues to preserve strings without accepting responsibility for manifests, hashes, filesystem access, span validation, annotation validation, or support evaluation.

## Source/artifact/annotation identity rules

- `source_id` must exist in the supplied manifest.
- `artifact_id` must exist in the supplied manifest.
- The selected artifact must name the supplied source as `parent_source_id`.
- Parent source hash and selected artifact hash are distinct fields.
- If supplied, `annotation_id` must exist and belong to the same selected artifact.
- Material identity, work identity, edition identity, and interpretation identity remain distinct.

## Coordinate conventions

Line bounds are one-based and inclusive. Character bounds, when supplied, are also one-based and inclusive. Character bounds are optional and must be supplied as a start/end pair.

## Annotation compatibility rule

This slice chooses exact span equality as the deterministic annotation compatibility rule. If a request supplies an annotation ID, the request line span and optional character span must exactly equal the annotation span. Ambiguous containment or overlap relationships are rejected as `annotation_span_mismatch`.

## Validation outcomes

The validator preserves these deterministic failures when applicable:

- `unknown_manifest`
- `unknown_source`
- `unknown_artifact`
- `source_artifact_mismatch`
- `artifact_hash_mismatch`
- `invalid_line_bounds`
- `line_bounds_out_of_range`
- `invalid_character_bounds`
- `unknown_annotation`
- `annotation_artifact_mismatch`
- `annotation_span_mismatch`
- `duplicate_testimony_reference_id`

## Boundary notes

Human and JSON output expose the following boundaries:

- Validated bindings establish material-reference integrity only.
- A valid span does not establish that the span supports or contradicts any claim.
- A matching artifact hash does not establish source authority or truth.
- Annotation existence does not establish annotation correctness.
- Bindings are not runtime Evidence, Facts, grammar verification, or capability evidence.
- No material interpretation, candidate ranking, or testimony evaluation occurs.

## CandidateExternalGrammarSet compatibility

`CandidateExternalGrammarInput`, `CandidateExternalGrammarInputCandidate`, and `CandidateExternalGrammarSet` were not modified. Validated binding IDs can be supplied unchanged as candidate support or contradiction strings. Candidate grammar artifacts still refuse responsibility for manifests, hashes, filesystems, span validation, annotation validation, support calculation, contradiction calculation, and grammar verification.

## Supervised campaign integration

The campaign now exposes a bounded manifest, testimony-binding requests, and validated binding set over `selected_lesson_006.txt`. It uses the real lesson hash `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963` and exact selected artifact lines 1-4. The selected lesson text was not modified.

## Unknown preservation

Manifest unknowns, record unknowns, request unknowns, and set unknowns are preserved as caller-supplied strings. Unknowns are not promoted to Evidence, Facts, or interpretation.

## Read-only guarantees

The implementation and rendering preserve:

- `read_only = true`
- `writes_event_ledger = false`
- `mutates_cluster = false`

The slice does not fetch URLs, acquire material, modify external material, append events, create Observations, create Evidence, create Facts, alter projected State, mutate repositories or clusters, register tools, or execute operations.

## Compatibility answer

Did this slice change any existing compatibility boundary?

No.

## Files changed

- `seed_runtime/external_material_testimony_binding.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py`
- `tests/test_external_material_testimony_binding.py`
- `external_material_testimony_binding_slice_001.md`

## LOC delta

Pre-commit observed additions were approximately: 212 canonical implementation lines, 104 focused test lines, 39 campaign integration lines, 29 CLI lines, 15 diagnostic inventory lines, 10 diagnostic shape-audit lines, and this report.

## Tests executed

- `pytest -q tests/test_external_material_testimony_binding.py`
- `pytest -q tests/test_external_material_testimony_binding.py tests/test_candidate_external_grammar.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining missing roads

Unresolved by design:

```text
external material
→ automatic structural-region discovery
```

```text
material span
→ candidate annotation
```

```text
multiple spans
→ structural comparison
```

```text
structural comparison
→ candidate grammar generation
```

```text
validated reference
→ testimony support or contradiction evaluation
```

```text
supported grammar candidate
→ translation specification
```
