# External Material Structural Feature Comparison Topology Audit 001

## 1. Bounded question

What deterministic comparison can Seed perform between caller-selected external-material line or region feature records while reporting only exact agreements, exact differences, and Unknowns, without selecting correspondences, computing semantic similarity, identifying recurrence, or recovering responsibility?

## 2. Starting evidence

The completed road is implementation-backed: `project_external_material_structure` validates manifest/source/artifact identity, expected hash, exact text hash, line count, and character count before producing an `ExternalMaterialStructuralProjection` (`seed_runtime/external_material_structural_projection.py:118-148`). The structural artifact is read-only, records convention and coordinate fields, and exposes lines plus nonblank regions (`seed_runtime/external_material_structural_projection.py:79-115`).

The next road is also implementation-backed: `project_external_material_surface_features(structural_projection)` validates the structural projection and emits an `ExternalMaterialSurfaceFeatureProjection` (`seed_runtime/external_material_surface_feature_projection.py:111-126`). The line feature record preserves `line_id`, `line_number`, raw/content/terminator character counts, blank status, terminator status, and unknowns (`seed_runtime/external_material_surface_feature_projection.py:39-51`). The region feature record preserves `region_id`, `line_ids`, `line_count`, raw/content sequences, totals, and unknowns (`seed_runtime/external_material_surface_feature_projection.py:54-71`).

Feature conventions are explicit: counts use Python string characters, content count excludes only the recorded line terminator, other whitespace remains counted, region sequences preserve physical line order, and no normalization or interpretation occurs (`seed_runtime/external_material_surface_feature_projection.py:14-23`). Boundary notes already refuse semantic structure, correspondence, shared responsibility, headings, rules, examples, exercises, code, prose, and grammar (`seed_runtime/external_material_surface_feature_projection.py:24-31`).

The existing focused test verifies the selected lesson feature sequence `[248, 464, 433, 479]` and verifies that `AGENTS.md` produces at least one four-line feature region while refusing correspondence and semantic similarity claims (`tests/test_external_material_surface_feature_projection.py:94-114`). A read-only probe during this audit found two caller-eligible `AGENTS.md` four-line region sequences: `[47, 152, 56, 61]` and `[60, 49, 39, 70]`.

Current implementation truthfully preserves `same line count` and `different content-character sequences`, but no typed comparison request/result artifact exists in the inspected external-material modules.

## 3. Governing distinctions

This audit preserves all requested distinctions: comparison is not selection; a comparison subject is not correspondence; equal line count is not similar structure; unequal sequence values are not structural dissimilarity; numeric difference is not significance; exact agreement is not shared meaning; positional comparison is not aligned semantic roles; caller-selected alignment is not Seed-discovered correspondence; comparison result is not recurrence; recurrence is not recovered responsibility; distance is not similarity; comparison observation is not judgment.

## 4. Constitutional comparison boundary

The lawful boundary is: caller-selected subjects and basis -> validated comparison request -> deterministic operation -> typed comparison result. The caller must own the left subject, right subject, comparison level, feature name, operation, positional alignment instruction, and requested scope. Seed must not choose artifacts, regions, lines, features, importance, similarity, recurrence, or responsibility.

## 5. Composition-depth discipline

The audit stopped at implementation evidence affecting determinism, identity, alignment, failure behavior, provenance, Unknown preservation, and current sufficiency. It did not inspect or propose statistics, clustering, embeddings, edit distance, dynamic alignment, semantic matching, machine learning, grammar induction, language parsing, Markdown parsing, or source parsing.

## 6. Methodology

I ran the three required focused searches, inspected the implementation bodies and tests around external-material structural projection, surface-feature projection, testimony binding, candidate grammar preservation, documentation structure recurrence/membership, source navigation, selection path audit, diagnostic inventory/shape audit, audit snapshot comparison, observation agreement, and self-model alignment. I then used a read-only Python snippet to compute the two primary sequence probes from existing projection producers and literal caller-selected sequences.

## 7. Inspected neighborhoods

Inspected neighborhoods included:

- `seed_runtime/external_material_structural_projection.py`
- `seed_runtime/external_material_surface_feature_projection.py`
- `seed_runtime/external_material_testimony_binding.py`
- `seed_runtime/candidate_external_grammar.py`
- `seed_runtime/structure_observation.py`
- `seed_runtime/documentation_structure.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/audit_snapshots.py`
- `seed_runtime/knowledge/observation_agreement.py`
- `seed_runtime/knowledge/self_model_alignment.py`
- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/`
- focused tests matching comparison, discrepancy, conflict, reconciliation, recurrence, shape-audit, external-material, and audit-snapshot terms.

## 8. Primary probe identities

External lesson subject:

- Source: Project Gutenberg eBook #7010, *Graded Lessons in English*.
- Artifact: `selected_lesson_006.txt`.
- SHA-256: `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`.
- Feature: region `content_character_count_sequence`.
- Values: `[248, 464, 433, 479]`.
- Existing test evidence: `tests/test_external_material_surface_feature_projection.py:94-100`.

Repository artifact subjects:

- Artifact: `AGENTS.md`.
- SHA-256: `60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed`.
- Feature: caller-selected four-line region `content_character_count_sequence`.
- Values observed during the read-only probe: `[47, 152, 56, 61]` and `[60, 49, 39, 70]`.
- Existing test evidence verifies the hash and that four-line regions are present without semantic correspondence claims (`tests/test_external_material_surface_feature_projection.py:105-114`).

## 9. Existing comparison-owner inventory

| Owner | Left input | Right input | Operation | Output | Semantic/authority assumptions | Reuse classification |
| --- | --- | --- | --- | --- | --- | --- |
| External structural projection validation | Manifest selected artifact and request exact text/hash/counts | Caller request metadata, encoded text hash, line/character counts | Exact equality checks; mismatch errors | `ExternalMaterialStructuralProjection` or deterministic error | Authority limited to material-reference integrity; not semantic truth (`seed_runtime/external_material_structural_projection.py:118-148`) | reusable constitutional precedent |
| External surface feature validation | Structural projection lines/regions | Region line IDs and physical line positions | Duplicate/membership/order/count validation | `ExternalMaterialSurfaceFeatureProjection` or deterministic error | Mechanical order only; no semantic structure (`seed_runtime/external_material_surface_feature_projection.py:200-226`) | reusable constitutional precedent |
| Audit snapshot comparison | Previous snapshot JSON | Latest snapshot JSON | Set added/removed; field changed from/to | Dict diff for supported snapshot kinds (`seed_runtime/audit_snapshots.py:130-205`) | Substrate-specific to observation inventory and ownership discrepancy snapshots | substrate-specific comparison |
| Diagnostic shape audit | Declared diagnostic inventory/spec | Observed implementation markers | Declared vs observed status | `DiagnosticShapeAuditRow` with consistent/warning/mismatch/unknown (`seed_runtime/diagnostic_shape_audit.py:55-82`) | Operational diagnostic authority over registered surfaces | diagnostic-only comparison |
| Observation agreement | Supplied evidence text from independent streams | Supplied evidence text from other streams | Trimmed exact string equality and stream count | Candidate agreement record (`seed_runtime/knowledge/observation_agreement.py:65-99`) | Refuses semantic interpretation and truth promotion | reusable constitutional precedent |
| Candidate external grammar validation | Caller-supplied candidate IDs | Seen candidate IDs | Duplicate ID equality | Candidate set or duplicate error (`seed_runtime/candidate_external_grammar.py:98-115`) | Caller-supplied hypotheses preserved, not evaluated | authority-bearing gate |
| Testimony binding validation | Binding request span/hash/source | Manifest source/artifact/annotation facts | Referential equality/range checks | Binding set or deterministic error; valid span not support/contradiction (`seed_runtime/external_material_testimony_binding.py:7-15`) | Integrity only, not source authority or truth | authority-bearing gate |
| Documentation structure recurrence | Corpus structural observations | Counters and thresholds | Count equal labels/depths/keys/languages; min-count filters | Recurrence report (`seed_runtime/documentation_structure.py:961-1030`) | Corpus-level recurrence over repository docs; not external feature comparison | substrate-specific comparison |
| Documentation structure membership | Target label | Observed section labels | Exact inclusion | Membership report; no similarity/classification (`seed_runtime/documentation_structure.py:40-45`) | Repository docs only | substrate-specific comparison |
| Source navigation matching | Caller query | Preserved source fact subject/path/value | Syntactic exact/short-symbol/path matching | Navigation view (`seed_runtime/source_navigation.py:177-259`) | Navigation only; no behavior/reachability/ownership | substrate-specific comparison |
| Selection path audit | Target focus/category | Pressure/story candidates | Selection explanation and non-selected preservation | Selection path audit (`seed_runtime/selection_path_audit.py:126-153`) | Explains implemented selection, not comparison | insufficient evidence |
| Self-model alignment | Supplied documentation claim | Supplied artifact facts | Rule-specific matching and support/conflict classification | `AlignmentRecord` | Imports semantic/authority assumptions through claim families and supported/conflict outcomes | semantic comparison |
| Test assertions | Expected values | Actual values | Python equality | Test pass/fail | Test-only verification | incidental equality check |

## 10. Comparison-subject identity analysis

Minimum stable subject identity should be no weaker than the projection’s existing provenance fields: `manifest_id`, `source_id`, `artifact_id`, `artifact_hash`, `structural_projection_identity`, `feature_convention`, record ID (`line_id` or `region_id`), and `feature_name`. The surface-feature projection already carries the artifact identifiers and feature convention (`seed_runtime/external_material_surface_feature_projection.py:74-108`). Line and region records already carry stable IDs generated from artifact identity and coordinates upstream, and tests verify stable IDs for repeated identical projections and changed IDs across changed artifact identity/hash (`tests/test_external_material_structural_projection.py:51-70`).

Possible subjects and current status:

- Line feature record: stable enough when identified by projection identity + feature convention + `line_id` + feature name.
- Region feature record: stable enough when identified by projection identity + feature convention + `region_id` + feature name.
- Entire feature projection: identifiable, but comparing entire projections would aggregate too much and invite feature/basis selection by Seed.
- Selected feature sequence: stable when derived from a named region feature and named sequence field.
- Single scalar feature: stable when derived from a named line/region feature and named scalar field.

## 11. Comparison-level analysis

| Level | Classification | Rationale |
| --- | --- | --- |
| Scalar-to-scalar | safe but absent | Exact equality/inequality and numeric differences over caller-selected numeric fields are deterministic and interpretation-free. |
| Line-to-line | safe but absent | Safe only as a container for caller-selected scalar feature comparisons; whole-line comparison would otherwise imply basis selection. |
| Region-to-region | safe but absent | Safe only as selected scalar/sequence feature comparisons; whole-region comparison is premature aggregation. |
| Sequence-to-sequence | safe but absent | Equal-length caller-aligned positional comparison is deterministic if output refuses role/correspondence claims. |
| Projection-to-projection | premature aggregation | It would require selecting comparable records/features and risks becoming correspondence discovery. |

## 12. Operation classification

| Operation | Scalar | Sequence | Interpretation-free | Alignment required | Warranted now? |
| --- | ---: | ---: | ---: | ---: | ---: |
| exact equality | yes | yes | yes | no for whole sequence equality | yes |
| inequality | yes | yes | yes | no | yes, as negation of exact equality |
| numeric difference | yes | per-position only | yes | yes for sequences | yes |
| absolute numeric difference | yes | per-position only | yes | yes for sequences | yes |
| sequence length equality | no | yes | yes | no | yes |
| exact sequence equality | no | yes | yes | no | yes |
| positional equality mask | no | yes | yes | yes | yes for equal-length or explicit matched prefix with unmatched positions |
| positional difference sequence | no | yes | yes | yes | yes for matched positions only |
| total equality | no | yes numeric sequences | yes | no | yes when feature is numeric sequence and total is explicitly requested or pre-existing |
| total numeric difference | no | yes numeric sequences | yes | no | yes when total basis is explicit |

Excluded: distance, similarity, confidence, thresholds, closeness, relevance, importance, correspondence strength, significance, recurrence, and responsibility.

## 13. Alignment analysis

Two sequences may be compared positionally only when the caller selected both sequences and requested positional comparison. Equal lengths are not conceptually required for every bounded sequence comparison: unequal lengths can produce length facts, matched-prefix position facts, and explicit left-only/right-only positions. However, the narrowest first implementation boundary should start with equal-length caller-aligned sequence comparison because it avoids deciding how to represent unmatched positions.

Position one on the left does not imply the same structural role as position one on the right. It means only: the caller asked Seed to compare ordinal position 1 with ordinal position 1 under the named operation. A result must state that positional pairing is caller-selected, not discovered by Seed.

## 14. Difference-representation analysis

Scalar observations can preserve: `left_value`, `right_value`, `equal`, `signed_difference` for numeric fields, and `absolute_difference` for numeric fields. Sequence observations can preserve: `left_length`, `right_length`, `lengths_equal`, `exact_sequence_equal`, per-position `left_value`, `right_value`, `equal`, `signed_difference`, `absolute_difference`, and, when unequal-length comparison is eventually owned, explicit `left_only_positions` and `right_only_positions`.

The result must not add percentage similarity, normalized distance, thresholded match, closeness, confidence, relevance, importance, or correspondence strength.

## 15. Unknown and failure behavior

A future boundary should preserve distinct statuses for: unknown left artifact, unknown right artifact, unknown line/region, artifact hash mismatch, feature convention mismatch, unsupported feature, feature unavailable on left, feature unavailable on right, comparison-level mismatch, sequence-length mismatch, invalid positional request, duplicate comparison request ID, and no comparable values.

`unavailable` must not collapse into `unequal`. `sequence-length mismatch` must not collapse into semantic dissimilarity. Current external-material producers already use deterministic error codes for unknown artifact/hash/count/order failures rather than semantic judgments (`seed_runtime/external_material_structural_projection.py:118-148`; `seed_runtime/external_material_surface_feature_projection.py:200-226`).

## 16. Feature-convention compatibility

Current feature artifacts expose `feature_convention` and convention notes, while the structural projection exposes projection, coordinate, and line-splitting conventions (`seed_runtime/external_material_surface_feature_projection.py:14-23`; `seed_runtime/external_material_structural_projection.py:93-95`). Comparisons should require exact feature-convention compatibility for canonical results. Cross-convention comparison should fail or remain Unknown unless a future caller-authorized conversion boundary exists. This audit does not warrant conversion.

## 17. Comparison-request ownership

A future producer should consume a typed request preserving: comparison request ID, left subject reference, right subject reference, comparison level, feature name, operation, alignment instruction, and request unknowns. Free-form comparison expressions are too broad because they could smuggle feature selection, correspondence selection, semantic role claims, or recurrence questions into the comparison boundary.

## 18. Comparison-artifact analysis

One bounded immutable artifact is warranted as the smallest future shape, not multiple broad artifacts: a tagged comparison result that can carry scalar or equal-length sequence result variants. It should preserve request identity/basis, left/right subject references, feature name, operation, alignment basis, result facts, Unknowns/failures, boundary notes, and read-only/no-ledger/no-cluster flags. Entire projection comparison is not warranted.

## 19. Selected lesson versus `AGENTS.md` comparison probe

Caller-selected sequence A: `[248, 464, 433, 479]`.

Caller-selected sequence B: `[47, 152, 56, 61]`.

Read-only mechanical observations:

- Left length: 4.
- Right length: 4.
- Lengths equal: true.
- Exact sequence equal: false.
- Positional equality mask: `[false, false, false, false]`.
- Positional signed differences using left minus right: `[201, 312, 377, 418]`.
- Positional absolute differences: `[201, 312, 377, 418]`.
- Left total: 1624.
- Right total: 316.
- Total signed difference using left minus right: 1308.

Second caller-selected `AGENTS.md` sequence, only as a repeated probe not candidate search: `[60, 49, 39, 70]`.

- Left length: 4.
- Right length: 4.
- Lengths equal: true.
- Exact sequence equal: false.
- Positional equality mask: `[false, false, false, false]`.
- Positional signed differences using left minus right: `[188, 415, 394, 409]`.
- Positional absolute differences: `[188, 415, 394, 409]`.
- Left total: 1624.
- Right total: 218.
- Total signed difference using left minus right: 1406.

No probe result labels the records similar, dissimilar, close, far, analogous, corresponding, meaningful, recurrent, or responsibility-bearing.

## 20. Structuring-probe implications

Deterministic exact comparison would improve structuring probes by replacing manual arithmetic and equality checks with typed observations. It enables better questions such as: which additional raw feature distinguishes equal-length regions, whether the same exact positional arrangement is observed under an independently selected basis, whether repeated exact differences align with independently known boundaries, and whether another substrate exposes the same sequence under a different producer. It does not establish correspondence.

## 21. Recurrence-boundary analysis

After deterministic comparison, the first missing responsibility before recurrence is candidate pair/request selection for repetition counting. Deterministic comparison can say two caller-selected records agree/differ exactly; it cannot decide what set of comparisons should be counted, which bases define recurrence identity, what counterexamples matter, or whether recurrence sufficiency is met.

## 22. Manual-handoff inventory

Current operator steps include: manually checking whether two line counts are equal, manually checking whether sequences are exactly equal, manually subtracting positional length values, manually summing totals or noticing total differences, and manually recording unmatched positions. Non-reducible operator steps include deciding correspondence, deciding recurrence meaning, selecting the feature basis, and recovering responsibility.

## 23. First reducible manual responsibility

The first reducible manual responsibility is: human checks whether two caller-selected feature sequences have equal length and are exactly equal. The next nearby reducible arithmetic step is per-position subtraction for caller-aligned equal-length numeric sequences.

## 24. Reverse trace

| Stage | Current producer | Current artifact | Current consumer | Manual or Seed-owned | Missing boundary |
| --- | --- | --- | --- | --- | --- |
| structural projection | `project_external_material_structure` | `ExternalMaterialStructuralProjection` | surface-feature projection and CLI/tests | Seed-owned | none for current road |
| surface-feature projection | `project_external_material_surface_features` | `ExternalMaterialSurfaceFeatureProjection` | CLI/tests/campaign record | Seed-owned | no comparison consumer |
| comparison-subject selection | absent | absent | absent | manual/caller | typed subject reference |
| comparison-basis selection | absent | absent | absent | manual/caller | typed feature/level/operation request |
| exact comparison | absent for external structural features | absent | absent | manual | deterministic comparison producer |
| difference preservation | absent for external structural features | absent | absent | manual | typed result with Unknowns |
| recurrence identification | documentation-structure recurrence exists for repository docs only | `DocumentationStructureRecurrenceReport` | docs diagnostic | Seed-owned only in that substrate | external feature recurrence identity/selection/counting absent |
| correspondence testimony | absent | absent | absent | manual/caller | correspondence boundary intentionally absent |
| responsibility recovery | absent | absent | absent | manual/not owned | responsibility recovery absent |

## 25. Reusable owners

No existing owner is a reusable structural feature comparison owner. Closest precedents are:

1. Observation agreement: exact equality over supplied records, candidate-only output, provenance preservation, and explicit refusal to promote truth (`seed_runtime/knowledge/observation_agreement.py:65-99`).
2. External structural/surface validation: deterministic identity/feature production with typed failures and explicit semantic refusals (`seed_runtime/external_material_structural_projection.py:118-148`; `seed_runtime/external_material_surface_feature_projection.py:111-126`).
3. Audit snapshot comparison: mechanical added/removed/from-to diff, but substrate-specific (`seed_runtime/audit_snapshots.py:177-205`).

## 26. Missing owners

Missing owners are: typed comparison request, stable subject reference resolver, deterministic scalar comparison result, deterministic caller-aligned sequence comparison result, Unknown/failure taxonomy for comparison, and boundary notes refusing selection/correspondence/similarity/recurrence/responsibility.

## 27. Missing roads

Missing road: `ExternalMaterialSurfaceFeatureProjection` -> caller-selected `ExternalMaterialStructuralFeatureComparisonRequest` -> immutable exact comparison result.

Absent roads must remain absent: comparison -> correspondence testimony; comparison -> recurrence implementation; comparison -> responsibility recovery; comparison -> similarity/distance score.

## 28. Strongest supporting evidence

Strongest support for one bounded comparison slice:

- Feature projection already provides stable artifact identity, structural projection identity, feature convention, line/region IDs, scalar features, sequences, totals, read-only status, and non-mutation flags (`seed_runtime/external_material_surface_feature_projection.py:74-108`).
- Existing tests verify the exact external lesson sequence and the repository four-line-region compatibility without semantic correspondence (`tests/test_external_material_surface_feature_projection.py:94-114`).
- Observation agreement demonstrates a constitutional precedent for exact comparison over supplied records that preserves candidate output and refuses truth promotion (`seed_runtime/knowledge/observation_agreement.py:65-99`).

## 29. Strongest counterevidence

Strongest counterevidence:

- Ordinary equality checks are trivial and currently handled in tests or caller scripts; a canonical artifact risks over-formalizing arithmetic.
- Diagnostic shape audit already compares declared versus observed diagnostic shapes, so a generic comparison artifact could duplicate diagnostic-only comparison if scoped too broadly (`seed_runtime/diagnostic_shape_audit.py:55-82`).
- Audit snapshot comparison already has set/field diffs, but it is explicitly snapshot-kind-specific and not a reusable external-feature artifact (`seed_runtime/audit_snapshots.py:130-205`).
- Positional difference can be misread as correspondence unless the request and result loudly preserve caller-selected alignment.
- Feature convention mismatch is a real blocker for safe cross-artifact comparison unless conventions match exactly.
- Recurrence, not comparison, may be the larger missing owner; comparison alone does not select candidate pairs or count repetition.

## 30. Supported conclusions

1. Seed does not currently own a reusable exact structural feature comparison artifact.
2. Scalar feature values can be compared safely when both subjects and feature names are caller-selected and conventions match.
3. Equal-length sequences can be compared positionally when the caller explicitly requests ordinal alignment.
4. Unequal-length sequences can be compared without implied alignment only by preserving length facts and explicit unmatched positions; this is warranted conceptually but not the narrowest first slice.
5. Signed and absolute numeric differences are lawful mechanical facts for numeric features.
6. Distance and similarity scores are not lawful at this boundary.
7. Line and region records from different artifacts can be compared if both records are caller-selected, stable IDs/provenance are preserved, and feature conventions match exactly.
8. Entire projection comparison is not warranted.
9. Deterministic comparison improves structuring probes but does not warrant recurrence implementation next.
10. One bounded implementation slice is warranted.

## 31. Unsupported conclusions

Unsupported conclusions include: Seed has discovered correspondence; equal line counts show similar structure; unequal sequence values show dissimilarity; numeric differences are significant; recurring arrangements establish shared responsibility; entire projections should be compared; feature-convention conversion should be implemented; recurrence testimony is ready immediately after comparison.

## 32. Primary classification

C. Surface-feature projection exists, but deterministic structural feature comparison is a genuinely missing responsibility.

## 33. Comparison-scope classification

2. Scalar and caller-aligned equal-length sequence comparison are warranted.

## 34. Recurrence-readiness classification

II. Deterministic comparison will improve recurrence questions, but another boundary remains before recurrence implementation.

## 35. Exact next bounded boundary

Recovered responsibility: replace manual exact arithmetic/equality checks over caller-selected external-material feature records.

Producer: a future external-material structural feature comparison producer.

Input artifacts: two `ExternalMaterialSurfaceFeatureProjection` records or two subject references resolvable within such projections, plus a typed comparison request.

Output artifact: one immutable tagged scalar/equal-length-sequence comparison result.

Consumer: operator/campaign/probe code that currently performs manual exact checks.

Exact bounded question: for these two caller-selected feature subjects and this caller-selected feature/operation, what exact agreements, differences, and Unknowns are mechanically observable?

Lawful operations: scalar exact equality/inequality, scalar signed/absolute numeric difference, sequence length equality, exact sequence equality, positional equality mask for equal-length caller-aligned numeric sequences, positional signed/absolute difference for equal-length caller-aligned numeric sequences, total equality, and total numeric difference.

Explicit exclusions: subject discovery, correspondence discovery, semantic alignment, unequal-length unmatched-position artifact in the first slice, whole-projection comparison, similarity/distance scores, recurrence, and responsibility recovery.

## 36. Implementation-warrant decision

One bounded implementation slice is warranted.

## 37. Files changed

- `external_material_structural_feature_comparison_topology_audit_001.md` only.

## 38. Probes executed

- `rg -n "compare|comparison|equal|difference|mismatch|discrepancy|expected|actual|left|right" seed_runtime campaigns tests`
- `rg -n "sequence|alignment|position|correspond|similar|distance|recurrence|repeated" seed_runtime campaigns tests`
- `rg -n "ExternalMaterialSurfaceFeatureProjection|content_character_count_sequence|total_content_character_count|region_features" seed_runtime campaigns tests *.md`
- `sed`/`nl -ba` inspections of relevant implementation and test files.
- Read-only Python probe computing the selected lesson and `AGENTS.md` feature sequences and deterministic comparison facts.

## 39. Confidence statement

Confidence is high that external-material structural and surface-feature projection are implemented and that no reusable typed structural feature comparison artifact exists. Confidence is medium-high on the implementation-warrant decision because exact comparison is mechanically small and constitutionally bounded, but the strongest counterevidence is real: if the future slice expands beyond caller-selected scalar/equal-length sequence operations, it would duplicate diagnostics or drift into correspondence/recurrence responsibilities.

## Required questions answered

1. No.
2. Observation agreement is the closest constitutional precedent.
3. Self-model alignment, graph validation, service/ownership authority gates, documentation recurrence/outlier signals, and source navigation matching import substrate-specific semantic or authority assumptions to varying degrees.
4. Yes, with caller-selected subjects/features and matching conventions.
5. Yes, if caller-aligned and output refuses correspondence.
6. Yes conceptually, with explicit unmatched positions and no implied alignment; not first-slice warranted.
7. It means caller-requested ordinal pairing only.
8. It should be a valid comparison result for length operations and a bounded non-result/Unknown for operations requiring equal-length positional pairs unless unmatched positions are explicitly supported.
9. Exact equality/inequality, numeric signed/absolute difference, sequence length equality, exact sequence equality, positional equality mask, positional signed/absolute differences, total equality, total numeric difference.
10. Yes.
11. Yes.
12. No.
13. Yes, for canonical comparison.
14. Yes, if caller-selected and conventions match.
15. Yes, if caller-selected and conventions match.
16. No.
17. Yes.
18. Request ID, left/right subject references, level, feature, operation, alignment instruction, convention/provenance expectations, and unknowns.
19. Similarity, correspondence, recurrence, significance, importance, semantic roles, responsibility, and subject/feature discovery.
20. One immutable tagged scalar/equal-length sequence comparison artifact.
21. Human checks equal length and exact sequence equality.
22. Yes.
23. No.
24. Candidate pair/request selection for repetition counting.
25. Yes: one bounded implementation slice is warranted.
