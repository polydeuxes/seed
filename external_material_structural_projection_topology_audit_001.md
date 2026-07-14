# External Material Structural Projection Topology Audit 001

## 1. Bounded question

What substrate-neutral structural features can Seed project from bounded external text without reading its prose, assigning semantic labels, or inferring grammar?

Primary boundary audited:

```text
bounded external material
→ mechanical structural projection
→ structurally addressable regions and relationships
```

This audit is read-only with respect to runtime behavior. It does not implement structural projection.

## 2. Starting evidence

The repository contains the completed preservation road:

```text
real external material
→ ExternalMaterialManifest
→ ExternalMaterialTestimonyBindingSet
→ stable testimony_reference_id
→ CandidateExternalGrammarSet
```

Evidence:

- `ExternalMaterialManifest` stores source records, selected artifact records, annotations, and manifest unknowns.
- `ExternalMaterialSelectedArtifactRecord` stores identity, hash, location, line count, character count, bounds text, and unknowns; it does not store selected text bytes.
- `validate_external_material_testimony_bindings` validates manifest id, source id, artifact id, source/artifact relationship, expected artifact hash, line bounds, optional character bounds, optional annotation existence, artifact match, and exact span equality.
- Binding boundary notes explicitly say bindings establish material-reference integrity only, do not establish support or contradiction, do not evaluate interpretation, and are not runtime Evidence or Facts.
- `CandidateExternalGrammarInputCandidate.supporting_testimony` and `contradicting_testimony` are tuples of strings.
- `CandidateExternalGrammarSet` preserves caller-supplied candidates and testimony strings; it does not validate support semantics or bind offsets.
- The supervised campaign reads `selected_lesson_006.txt`, verifies the exact SHA-256 `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`, decodes UTF-8 for reporting, and constructs the manifest, testimony bindings, and candidate grammar output.
- The current first manual handoff remains: exact material span → human reports what kind of visible or meaningful structure it appears to contain.

## 3. Governing distinctions

The audit preserves these distinctions:

- text decoding != prose comprehension
- line or region boundary != semantic unit
- capitalization pattern != heading
- repeated shape != repeated meaning
- punctuation pattern != sentence role
- indentation != grammatical dependency
- structural similarity != semantic similarity
- structural projection != grammar candidate generation
- mechanical region != human annotation

Semantic labels such as heading, title, lesson, rule, definition, example, exercise, instruction, contrast, subject, predicate, noun, verb, sentence, clause, and English grammar are treated as caller testimony unless an implementation owner gives them a narrower mechanical meaning.

## 4. Composition-depth rule

The audit descended only to implementation boundaries that affect identity, text access, decoding, bounds, determinism, provenance, failure behavior, replaceability, or current inquiry sufficiency. It did not inspect parser internals, Unicode algorithm internals, compression, filesystem internals, Python runtime internals, or hardware mechanics.

## 5. Methodology

Commands/probes executed are listed in section 31. The audit used focused `rg` searches, direct implementation inspection, test-neighborhood inspection, and one read-only byte inspection of the selected lesson. Classifications are based on implementation bodies and consumers, not search matches alone.

## 6. Inspected neighborhoods

Inspected implementation and nearby tests/docs:

- `seed_runtime/structure_observation.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/external_material_testimony_binding.py`
- `seed_runtime/candidate_external_grammar.py`
- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py`
- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt`
- `graded_lessons_supervised_grammar_apprenticeship_campaign_001.md`
- `project_gutenberg_external_orientation_campaign_001.md`
- `seed_runtime/documentation_structure.py`
- `tests/test_external_material_testimony_binding.py`
- `tests/test_candidate_external_grammar.py`
- focused structure/search tests surfaced by the required `rg` commands, especially documentation-structure and diagnostic-inventory line-set neighborhoods.

## 7. Selected lesson identity

Primary probe:

| Field | Value |
| --- | --- |
| Source | Project Gutenberg eBook #7010 |
| Reported title | Graded Lessons in English |
| Selected artifact | `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt` |
| Campaign artifact id | `gl001_selected_lesson_006` |
| Campaign source id | `gl001_source_pg7010` |
| Expected SHA-256 | `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963` |
| Observed SHA-256 | `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963` |
| Expected byte length | `1628` |
| Observed byte length | `1628` |
| Manifest line count | `4` |
| Observed byte-level splitlines count | `4` |
| Manifest character count source | `len(selected_lesson_bytes().decode("utf-8"))` |
| Encoding represented by campaign identity | `UTF-8` |
| Selected artifact bounds | `selected_lesson_006.txt lines 1-4` |

Read-only primary-probe surface facts from bytes:

- The artifact has four newline-terminated byte lines under `splitlines(keepends=True)`.
- Byte line lengths are 249, 465, 434, and 480 bytes, including line endings.
- All four lines are nonblank under simple whitespace stripping.
- The visible line order is fixed by file order.
- Punctuation and capitalization characters are present, but no existing external-material owner projects their patterns.

## 8. Exact material-access topology

| Question | Answer |
| --- | --- |
| Is text stored inside the manifest? | No. The manifest stores selected artifact identity, hash, artifact location, line count, character count, selection bounds, and unknowns. It does not store raw bytes or decoded text. |
| Does the manifest store only identity and location? | Mostly identity/location plus counts and human-readable bounds; it also stores annotations and unknowns. |
| Who reads the local artifact? | The campaign-local function `selected_lesson_bytes()` reads `SELECTED_LESSON.read_bytes()`. |
| Who verifies its hash? | `validate_source_identity()` hashes bytes from `selected_lesson_bytes()` and compares to `EXPECTED_SHA256`; it also checks byte length. Binding validation compares caller-supplied expected hash to the manifest artifact hash but does not read bytes. |
| Who owns decoding? | The campaign scaffold decodes via `selected_lesson_bytes().decode("utf-8")` in `lesson_selection()` and for manifest character count. There is no reusable external-material decoding owner. |
| Is encoding known or caller-supplied? | The campaign identity records `encoding="UTF-8"`; the reusable manifest schema has no encoding field on the selected artifact. |
| Can structural projection operate from caller-supplied text without filesystem access? | A future boundary could, and the repository-observation adapter demonstrates caller-supplied-text operation for Python source. No current external-material projection does so. |
| Would canonical projection need direct file access? | Not necessarily. Canonical projection could consume a verified bounded text artifact or caller-supplied decoded text plus provenance. Current canonical exact text access, however, is campaign-local file access. |

## 9. Existing structure-owner analysis

### `StructureObservationBoundary`

`StructureObservationBoundary` is an architectural ownership boundary. It declares read-only structural extraction, evidence preservation, non-interpretation, no substrate parsing, no grammar, no responsibility recovery, no lexicon ownership, and no event-ledger/repository/cluster mutation. Its documentation compatibility method explicitly says it does not infer shapes.

Findings:

- Input consumed: none; it is a dataclass boundary declaration.
- Output produced: boundary flags/text only.
- Substrate-neutral: yes as a responsibility statement.
- Requires parser: no.
- Preserves exact source locations: no records are produced.
- Infers interpretation: no.
- Operates on plain text: no operation is implemented.
- Reusable here: reusable as policy/orientation, not as a projection implementation.
- Architectural testimony vs owner: it is owner testimony, not a current external-material structural artifact producer.

### Repository artifact observation adapter

`RepositoryArtifactObservationAdapter.extract(source_path, text)` consumes caller-provided Python source text, parses with Python `ast`, and emits `RepositoryArtifactFact` records for modules, classes, functions, methods, and imports. It does not read files and falls back to a parse-failed module fact on `SyntaxError`.

Findings:

- Substrate-specific: Python source.
- Requires parser: yes, Python AST.
- Source locations: emitted facts carry path and symbol, not exact source spans.
- Interpretation: implementation says it does not infer architecture/ownership, but emitted facts are Python artifact facts.
- Plain text: consumes text but expects Python grammar.
- Reusable here: only as precedent that caller-supplied text can feed a structural adapter; reusing it for external prose would distort responsibility.

### Documentation structure owner

`documentation_structure.py` computes byte count, line count, blank/nonblank line counts, trailing newline, headings, sections, links, code fences, architectural relations, and outliers for documentation files. It reads documentation bytes, decodes UTF-8, and parses Markdown-like/documentation-specific structures.

Findings:

- It already implements line and blank-line metrics for documentation.
- It is substrate-specific to documentation/Markdown membership and includes semantic-ish documentation concepts such as headings, sections, links, code blocks, and architectural relations.
- Reusing its records for external-material regions would import documentation semantics into bounded external material.
- Its metrics are useful counterevidence that line segmentation is easy and already present elsewhere, but not as a lawful external-material owner.

### Diagnostic line-set owners

Diagnostic inventory has `_DiagnosticSurfaceDefinitionLineSet`, `_DiagnosticSurfaceExplanationLineSet`, and `_DiagnosticSurfaceEvidenceSourceLine`. These are operational diagnostic visibility artifacts. Their scope is diagnostic inventory/shape audit, not external material. Reusing them would distort the external-material responsibility and violate the distinction between diagnostics and cluster/material testimony.

## 10. Line and region artifact inventory

| Artifact/owner | Owns | Can represent external-material regions lawfully? | Reason |
| --- | --- | --- | --- |
| `ExternalMaterialSelectedArtifactRecord` | artifact identity, hash, location, line count, character count, selection bounds | Partially | Represents bounded artifact metadata, not per-line/region records or text fragments. |
| `ExternalMaterialAnnotationRecord` | caller-supplied annotation id, artifact id, line/optional character bounds, kind, supplied_by, unknowns | Partially but semantic/manual | Can hold coordinates but annotation kind is caller testimony; not mechanical projection. |
| `ExternalMaterialValidatedTestimonyBinding` | validated testimony reference and coordinate bounds | Partially | Stable references to spans, but no generated region identity or features. |
| `CandidateExternalGrammarInputCandidate` | caller-supplied structural claim and string testimony refs | No for projection | Preserves hypotheses, not regions/features. |
| `DocumentationStructureRecord` | documentation byte/line/blank metrics, headings, sections, links, code fences | No as canonical external owner | Documentation-specific surface and semantics. |
| Diagnostic line-set records | diagnostic definitions/explanations/evidence source lines | No | Diagnostic-specific operational visibility. |
| Repository artifact facts | Python module/class/function/import facts | No | Python-source substrate and no exact regions. |

No existing artifact composes external selected material into stable mechanical line/region identities with surface features and relationships.

## 11. Mechanical feature classification

| Feature | Classification | Existing owner | Evidence | Interpretation risk |
| --- | --- | --- | --- | --- |
| byte bounds | Derivable from existing implementation | Campaign local byte reader/hash; documentation metrics for docs | Selected artifact bytes and byte length are read/verified; no external region byte-offset records exist. | Low if preserved as coordinates; medium if inferred from decoded text without newline policy. |
| character bounds | Already explicitly implemented for validation; not projected | External material binding | Optional character bounds validate against artifact `character_count`. | Low for coordinates; medium because character-count unit/newline policy is not formalized. |
| line bounds | Already explicitly implemented for validation; not projected | External material binding | Start/end line validation against artifact line count. | Low if stated as one-based inclusive coordinates; high if treated as semantic unit. |
| blank-line regions | Derivable elsewhere, safe but absent for external material | Documentation structure | Documentation metrics count blank lines; selected lesson has none. | Low mechanically; medium if region means paragraph/section. |
| indentation | Safe but currently absent for external material | None found | Search found indentation parsing in YAML/inventory-like code, not external material. | Medium if mapped to hierarchy/dependency. |
| line length | Derivable from current byte/text access; absent as external artifact | Campaign local selected bytes/text | Read-only probe computed line byte lengths; manifest stores total character count. | Low mechanically. |
| capitalization shape | Safe but currently absent | None found | No external-material capitalization projector found. | Medium/high if called heading/title/emphasis. |
| digit shape | Safe but currently absent | None found | No external-material digit-shape projector found. | Medium if treated as list/exercise numbering. |
| punctuation shape | Safe but currently absent | None found | No external-material punctuation projector found. | Medium/high if treated as sentence role. |
| whitespace-token shape | Safe but currently absent | Inquiry tokenization exists for lexical matching, not structural external material | Tokenization appears in inquiry/source-navigation matching, not this boundary. | Medium because token-like splitting can look semantic. |
| exact repeated region | Safe but currently absent | None found for external material | Equality is Python-string/bytes derivable but no owner records repeated external regions. | Low for exact equality; medium if recurrence gets meaning. |
| normalized repeated shape | Unsupported or Unknown | None found for this boundary | No canonical normalization policy for external material. | High unless normalization is explicit and evidence-preserving. |
| adjacency | Derivable from validated coordinate bounds; absent as relation | External material line coordinates | One-based inclusive spans can be ordered; no relation artifact exists. | Low if coordinate-derived; medium if adjacency implies cohesion. |
| containment | Derivable from validated coordinate bounds; absent as relation | External material line/optional char coordinates | Span containment can be computed; not currently emitted. | Low mechanically; medium if semantic grouping inferred. |
| ordering | Derivable from validated coordinate bounds and file order; absent as relation | External material binding coordinates | Line numbers encode order; no structural relationship owner emits it. | Low mechanically. |

## 12. Region identity analysis

A stable structural region identity would likely need some combination of:

- manifest id;
- source id;
- artifact id;
- artifact hash;
- coordinate convention;
- start line and end line;
- optional start/end character or byte offsets;
- possibly a deterministic region id derived from those values;
- optional surface-feature summary that is not part of identity unless intentionally content-addressed.

Current evidence supports coordinate-addressed identity better than content-addressed identity because existing bindings already validate line/optional-character coordinates against manifest artifact metadata. Content-addressed region identity would require canonical text access and normalization/newline policy not currently owned. Caller-assigned identity is already used for annotations and testimony references but does not reduce manual handoff. Deterministically derived identity is plausible but not implemented. Final schema remains unresolved.

## 13. Relationship analysis

Mechanically assertable from coordinates alone, but not currently emitted:

- `precedes`
- `follows`
- `adjacent_to`
- `contains`
- `contained_by`
- `ordering`

Mechanically assertable only with exact text access and explicit raw-form preservation, but not currently emitted:

- `same_exact_text_as`

Unsafe or unsupported without a normalization/surface-shape policy:

- `same_surface_shape_as`
- `different_surface_shape_from`
- `shares_prefix_with`
- `shares_punctuation_pattern_with`

For a first slice, coordinate-derived line identity and nonblank contiguous regions are better supported than universal relationship taxonomy.

## 14. Normalization analysis

| Candidate normalization | Current lawful status | Notes |
| --- | --- | --- |
| Newline style | Preserved exactly by bytes; normalized mechanically only if caller selects and raw bytes remain preserved | Current selected file bytes are the evidence; no external-material newline normalizer exists. |
| Trailing whitespace | Preserved exactly by bytes; unsupported as normalization | Silent trimming would destroy evidence. |
| Repeated whitespace | Preserved exactly; unsupported as normalization | Collapsing whitespace risks erasing visible structure. |
| Case | Preserved exactly; unsupported as normalization | Case-folding would erase capitalization evidence. |
| Punctuation | Preserved exactly; unsupported as normalization | Removing or mapping punctuation would erase structural evidence. |
| Unicode normalization | Unsupported/caller-selected only with explicit raw preservation | Campaign decodes UTF-8 but does not declare Unicode normalization policy. |

Normalization must be explicit, caller-selected or owner-declared, and evidence-preserving. For this audit, exact raw form is the only fully lawful baseline.

## 15. Failure and Unknown behavior

Future projection should preserve distinct failures/unknowns rather than returning an empty projection:

| Condition | Current evidence | Required preservation behavior for future boundary |
| --- | --- | --- |
| Missing artifact | Campaign file read would fail; no reusable external failure artifact | Report missing artifact separately. |
| Hash mismatch | `validate_source_identity()` raises `AssertionError`; binding validation raises `artifact_hash_mismatch` only for manifest/request mismatch | Preserve hash mismatch as identity failure, not no regions. |
| Unknown encoding | Campaign records UTF-8; manifest lacks encoding | Preserve unknown encoding before decoding. |
| Decode failure | Campaign decode would raise; no reusable projection failure | Preserve decode failure separately. |
| Empty artifact | Documentation metrics represent empty docs; no external owner | Empty artifact is valid distinct state, not failed projection. |
| Invalid bounds | Binding validation has `invalid_line_bounds`, `line_bounds_out_of_range`, and invalid character bounds | Preserve coordinate failure. |
| Unsupported character structure | No boundary | Preserve Unknown rather than forcing character features. |
| No projected regions | No boundary | Distinguish no regions from failed access/decode. |
| Ambiguous normalization | No policy | Preserve raw and declare normalization unsupported/unknown. |

## 16. Selected lesson reverse trace

| Stage | Current producer | Current artifact | Current consumer | Manual or Seed-owned | Missing boundary |
| --- | --- | --- | --- | --- | --- |
| source identity | Campaign scaffold/operator | `SourceArtifactIdentity`; `ExternalMaterialSourceRecord` | campaign record; manifest | Mixed: operator/campaign supplied, Seed formats/validates selected bytes | Full parent source byte identity absent. |
| selected artifact identity | Campaign scaffold | `ExternalMaterialSelectedArtifactRecord` | manifest; binding validation | Seed-owned construction from campaign-local file plus operator-selected artifact | Canonical reusable external artifact store absent. |
| exact text access | Campaign-local `selected_lesson_bytes()` and UTF-8 decode | bytes/text local to campaign functions; `LessonSelection.selected_text` | campaign record | Seed-owned campaign-local, not reusable canonical | Reusable exact-text artifact boundary absent. |
| line segmentation | Campaign author/scaffold reports `line_count=4`; Python/text splitting possible | manifest line count; selected text lines | binding validation | Mixed; count is scaffold-supplied, not projected region artifact | Stable line identity/projection absent. |
| region segmentation | Human annotations and binding requests | `ExternalMaterialAnnotationRecord`; testimony refs | binding validation; candidates | Manual/caller-supplied | Mechanical region segmentation absent. |
| surface feature projection | Absent | Absent | Absent | Absent | Surface feature owner absent. |
| structural comparison | Absent except manual candidate wording | Caller strings in candidate claims | Candidate grammar output | Manual/caller-supplied | Mechanical comparison owner absent. |
| semantic annotation | Campaign author | `MaterialAnnotation`; `ExternalMaterialAnnotationRecord.annotation_kind`; candidate claims | candidate input; binding set | Manual/caller-supplied | Seed semantic reader absent intentionally. |
| candidate grammar input | Campaign author | `CandidateExternalGrammarInput` | `assemble_candidate_external_grammar_set` | Caller/manual input, Seed preservation | Schema-bound support semantics absent intentionally. |
| testimony binding | Campaign scaffold plus validation | `ExternalMaterialTestimonyBindingSet` | campaign record; candidate testimony refs remain strings | Seed-owned referential integrity | Region-feature binding absent. |

## 17. Manual-handoff inventory

| Current campaign-author step | Classification |
| --- | --- |
| Lesson selection | Requires external testimony and semantic/pragmatic judgment about relevant source excerpt. |
| Exact span selection | Mixed: line coordinates are mechanical once selected; choosing the bounded lesson requires external testimony/semantic judgment. |
| Identifying a line as visibly distinct | Mechanical and potentially recoverable if based only on surface features such as capitalization/punctuation/length; currently manual. |
| Identifying a heading | Requires semantic interpretation unless rephrased as capitalization/punctuation/position pattern. |
| Identifying an example | Requires semantic interpretation and English competency. |
| Identifying a rule | Requires semantic interpretation and English competency. |
| Identifying an exercise | Requires semantic interpretation and English competency. |
| Identifying contrast | Requires semantic interpretation unless reduced to mechanical differences between bounded shapes. |
| Creating structural candidate wording | Requires semantic interpretation, structural comparison, and caller testimony. |
| Binding support and contradiction | Binding references are mechanically validated; support/contradiction roles remain caller-supplied strings and require interpretation/testimony. |

## 18. First reducible manual responsibility

The earliest current manual responsibility Seed could take over without prose comprehension is mechanical line/region segmentation over the already selected and hash-verified bounded artifact: emit stable line records and a nonblank contiguous region record for the selected artifact, preserving provenance and Unknowns.

This is smaller than heading/example/rule/exercise recognition. It consumes existing bounded artifact identity, reduces the current handoff from “human reports what visible structure it appears to contain” to “Seed reports mechanically addressable lines/nonblank regions; human interprets them,” and gives a direct read-only consumer: future annotation/testimony binding can point at stable region ids instead of only caller-assigned annotation ids or free-form testimony strings.

## 19. Reusable owners

Strongest reusable owners:

1. `ExternalMaterialManifest`/`ExternalMaterialSelectedArtifactRecord` for artifact identity, hash, location, line count, and character count.
2. `validate_external_material_testimony_bindings` for referential-integrity validation of manifest/source/artifact/hash/span/annotation relationships.
3. `StructureObservationBoundary` for policy: read-only, non-interpretive, evidence-preserving structural extraction with substrate parsing owned by adapters.
4. Campaign-local `selected_lesson_bytes()`/`validate_source_identity()` for the selected lesson’s concrete byte access and hash proof.
5. Documentation-structure metrics as a noncanonical precedent that byte/line/blank-line metrics can be computed deterministically.

## 20. Missing owners

Missing owners:

- Reusable external-material exact-text/decoded-text artifact boundary.
- External-material line identity projection.
- External-material nonblank/blank-line-delimited region projection.
- External-material raw surface feature projection.
- External-material structural relationship projection.
- External-material normalization policy for comparison.
- Schema-bound connection from projected region ids to candidate grammar testimony strings/annotations.

## 21. Missing roads

Absent roads should not be filled by speculation:

```text
ExternalMaterialSelectedArtifactRecord
→ canonical decoded text artifact
```

```text
ExternalMaterialSelectedArtifactRecord
→ stable mechanical line records
```

```text
mechanical line records
→ nonblank contiguous regions / blank-line regions
```

```text
mechanical regions
→ surface feature summaries
```

```text
surface feature summaries
→ structural relationships
```

```text
projected region ids
→ current annotation/testimony reference schema
```

## 22. Strongest supporting evidence

- External-material manifests and binding validation already represent artifact identity, hash, line count, character count, line bounds, optional character bounds, and annotation span equality.
- Binding boundary notes explicitly prevent semantic overclaiming.
- Candidate grammar artifacts preserve caller-supplied structural hypotheses and testimony strings without ranking or verification.
- The campaign uses the real selected lesson file, exact expected hash, byte length, and UTF-8 decoding.
- `StructureObservationBoundary` declares a read-only, non-interpretive, substrate-adapter model that fits the desired responsibility at a policy level.
- Documentation structure proves deterministic byte/line/blank-line metrics are straightforward in the codebase, though not reusable as an external-material owner.

## 23. Strongest counterevidence

- Plain-text structural projection as a reusable external-material artifact was not found.
- `StructureObservationBoundary` intentionally excludes substrate parsing and is not an implementation.
- Line segmentation may be too trivial to warrant a canonical artifact; documentation metrics already count lines and blank lines for another domain.
- Existing spans and testimony bindings may be sufficient for the current campaign because the candidate grammar path accepts caller-supplied testimony strings and the campaign is explicitly supervised.
- Documentation/source-navigation/diagnostic line-set artifacts are existing region-like owners, so a new artifact risks duplication if scoped poorly.
- Capitalization, punctuation, digit, and whitespace features can encode English/document conventions if named carelessly.
- Normalized comparison can destroy evidence by erasing case, punctuation, whitespace, or newline distinctions.
- The first missing step could be argued to be semantic because lesson selection, examples, rules, exercises, and support/contradiction are all human testimony. The audit rejects that only for the smaller handoff of mechanical line/region visibility after selection.

## 24. Supported conclusions

1. Seed can currently access and verify the selected lesson text only through campaign-local functions, not through a reusable canonical external-material text artifact.
2. Seed validates external-material references by manifest/source/artifact/hash/span integrity only.
3. Seed preserves candidate grammar testimony references as strings.
4. Seed does not currently project external-material lines, regions, feature summaries, or structural relationships as typed immutable artifacts.
5. Mechanical line segmentation, nonblank contiguous region projection, exact coordinate ordering, and raw length/whitespace/punctuation/capitalization observations are safe in principle if they remain nonsemantic and evidence-preserving.
6. Normalized shape comparison is not currently supported and would need explicit raw-form preservation and caller/owner-selected normalization.
7. Repository/documentation/diagnostic structure owners provide useful precedents and counterevidence but are substrate-specific or visibility-specific.

## 25. Unsupported conclusions

Unsupported by current repository evidence:

- Seed has read or understood the lesson prose.
- Seed has identified a heading, rule, example, exercise, subject, predicate, sentence, clause, or English grammar concept in the selected lesson.
- Candidate grammar claims are true, ranked, or verified.
- Existing testimony references are schema-bound to projected region ids.
- Existing source-navigation or diagnostic line-set records can be reused directly for external-material regions without distortion.
- A canonical normalization policy exists for external-material structural comparison.

## 26. Primary classification

C. Seed has exact material identity and span binding, but mechanical structural-region projection is a genuinely missing responsibility.

## 27. Manual-handoff classification

2. Line or region segmentation remains the first manual boundary.

## 28. Exact next bounded boundary

Recovered responsibility: mechanical line and nonblank-region projection for one already bounded selected external text artifact.

Producer: a future external-material structural projection adapter under the existing Structure Observation policy.

Input artifact: `ExternalMaterialSelectedArtifactRecord` plus verified/caller-supplied exact text for the selected artifact.

Output artifact: immutable external-material structural projection containing stable line ids, raw line coordinates, raw text-presence metadata, nonblank contiguous region ids, provenance, and Unknown/failure fields.

Consumer: external-material annotations/testimony binding and campaign reporting as a read-only provenance surface.

Exact bounded question: “For this verified bounded artifact, what one-based lines and nonblank contiguous line regions exist mechanically?”

Explicit exclusions: no heading/title/lesson/rule/example/exercise detection; no grammar inference; no semantic labels; no candidate generation; no normalized similarity; no event-ledger writes; no cluster mutation; no selected-material mutation; no full-book acquisition.

## 29. Implementation-warrant decision

One bounded implementation slice is warranted.

## 30. Files changed

- `external_material_structural_projection_topology_audit_001.md` — new audit report only.

## 31. Probes executed

Required searches:

```bash
rg -n "StructureObservation|Structural|Region|LineSet|SourceLine|SourceSpan|start_line|end_line|character_count|line_count" seed_runtime campaigns tests
```

```bash
rg -n "selected_lesson_006|ExternalMaterialManifest|ExternalMaterialTestimonyBinding|CandidateExternalGrammar" seed_runtime campaigns tests *.md
```

```bash
rg -n "indent|capital|punctuation|whitespace|normalize|token|prefix|suffix|adjacent|contain" seed_runtime campaigns tests
```

Implementation/body inspection:

```bash
sed -n '1,260p' seed_runtime/external_material_testimony_binding.py
sed -n '1,220p' seed_runtime/candidate_external_grammar.py
cat seed_runtime/structure_observation.py
sed -n '1,220p' seed_runtime/knowledge/repository_observation.py
sed -n '1,280p' campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py
sed -n '120,220p' seed_runtime/documentation_structure.py
sed -n '630,670p' seed_runtime/documentation_structure.py
```

Selected lesson byte probe:

```bash
python - <<'PY'
from pathlib import Path
from hashlib import sha256
p = Path('campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt')
b = p.read_bytes()
print(len(b))
print(sha256(b).hexdigest())
print(repr(b[:200]))
for i, line in enumerate(b.splitlines(keepends=True), 1):
    print(i, len(line), repr(line[:120]))
PY
```

Diff guardrail before commit:

```bash
git diff --stat
git diff --numstat
git diff --check
git status --short
```

## 32. Confidence statement

Confidence is high for the classification that external-material identity/span binding exists and mechanical structural-region projection is missing. Confidence is medium for the exact first reducible boundary because the repository could reasonably decide that trivial line segmentation does not warrant a canonical artifact, but the current supervised campaign handoff and absence of stable projected region ids make one bounded line/nonblank-region slice warranted.
