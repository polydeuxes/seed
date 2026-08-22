# External Material Surface Feature Projection Topology Audit 001

## 1. Bounded questions

This read-only audit asks what raw, evidence-preserving surface features Seed can lawfully project from mechanically bounded lines and nonblank regions without interpreting prose, and whether recurrence across `selected_lesson_006.txt` and `AGENTS.md` is useful enough to guide one next bounded implementation slice. It does not implement projection, recurrence comparison, or responsibility inference.

## 2. Starting evidence

The completed road exists: `project_external_material_structure` validates a manifest-selected, hash-identified, caller-supplied exact text, projects stable line records, and projects maximal contiguous nonblank regions. The projection validates manifest/source/artifact identity, artifact hash, encoding, line count, and character count before splitting lines. Its line records include `line_id`, one-based `line_number`, zero-based half-open character offsets, `character_count`, `is_blank`, `has_line_terminator`, and raw `text`. Region records include `region_id`, inclusive start/end lines, referenced line IDs, and `line_count`.

The repository also preserves the prior recurrence probes. The campaign test verifies `selected_lesson_006.txt` has 4 lines and 1 nonblank region. The same test projects `AGENTS.md` with the same canonical producer and schema and asserts the JSON does not assert equivalence, correspondence, or semantic grammar. The prior structural report records `AGENTS.md` SHA-256 `60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed`, 61 lines, and 22 nonblank regions.

The first remaining manual handoff remains: mechanically projected region -> human describes visible surface properties.

## 3. Governing distinctions

The audit preserves these distinctions: raw character property is not a language token; uppercase characters are not a heading; a terminal question mark is not a question; repeated prefix is not shared meaning; short line followed by long lines is not title followed by body; surface recurrence is not semantic recurrence; structural correspondence candidate is not recovered responsibility; feature projection is not feature interpretation; exact equality is not normalized similarity; cross-substrate recurrence is not shared substrate grammar.

## 4. Composition-depth discipline

The audit descends only to deterministic properties computable from exact text and structural line/region coordinates. It avoids linguistic tokenization, POS tagging, sentence parsing, Unicode algorithm internals beyond Python character predicates used only as precedents, compression, parser internals, statistical language modeling, and embeddings.

## 5. Methodology

I inspected implementation bodies and direct consumers for external-material projection, testimony binding, structure observation, documentation structure, source navigation, the graded-lessons campaign, and focused tests. I ran the required focused `rg` searches, then used a read-only Python script to calculate candidate features for exactly the two primary probes.

## 6. Inspected neighborhoods

Inspected neighborhoods included `seed_runtime/external_material_structural_projection.py`, `seed_runtime/external_material_testimony_binding.py`, `seed_runtime/structure_observation.py`, `seed_runtime/documentation_structure.py`, `seed_runtime/source_navigation.py`, `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/`, `tests/test_external_material_structural_projection.py`, `tests/test_external_material_testimony_binding.py`, `tests/test_graded_lessons_campaign_001.py`, `external_material_structural_projection_slice_001.md`, and focused diagnostic registry references surfaced by search.

## 7. Primary artifact identities

| Artifact | Existing identity evidence |
| --- | --- |
| `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt` | Manifest artifact `gl001_selected_lesson_006`; source `gl001_source_pg7010`; manifest `gl001_lesson006_manifest`; SHA-256 `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`; 4 lines; 1 nonblank region; 1628 characters. |
| `AGENTS.md` | Prior probe manifest `repo_probe_manifest`; source `repo_source`; artifact `repo_agents_md`; SHA-256 `60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed`; 61 lines; 22 nonblank regions; 2253 characters. |

## 8. Existing surface-feature owner inventory

| Owner | Input | Output | Features | Normalization | Substrate assumptions | Reuse classification |
| ----- | ----- | ------ | -------- | ------------- | --------------------- | -------------------- |
| `ExternalMaterialStructuralProjection` | Manifest + exact text request | External-material projection | line count validation, character count validation, line offsets, line `character_count`, blank/nonblank, line terminator presence, raw line text, region line count | removes/separates only line terminator for blankness; otherwise raw distinctions are retained | bounded text only; no English/Markdown/source grammar | reusable owner for current structure; reusable implementation precedent for feature projection, but no canonical surface-feature artifact yet |
| `ExternalMaterialManifest` / selected artifact | Manifest JSON/dicts | selected artifact record | artifact `line_count`, `character_count`, hash | none beyond caller-supplied counts | selected external material metadata | reusable implementation precedent |
| `ExternalMaterialTestimonyBindingSet` | Manifest + coordinate requests | validated reference bindings | line/character bounds validation | none; coordinate validation only | selected artifact coordinates | incidental utility; not a feature owner |
| `DocumentationStructureRecord` | top-level `docs/*.md` files | documentation-structure report | line count, byte count, blank/nonblank line counts, trailing newline, headings, sections, duplicate heading text, links, code fences, recurrence distributions | UTF-8 decode; `splitlines()` without terminators; Markdown-ish heading/code/link parsing | Markdown docs under `docs/` | substrate-specific owner and semantic/presentation owner for headings/sections |
| Documentation recurrence reports | documentation-structure records | recurrence/drilldown/membership reports | repeated section labels, heading depths, skeleton signatures, link target classes, code fence languages | Markdown-derived label extraction and counters | docs corpus and Markdown conventions | substrate-specific owner |
| `StructureObservationBoundary` | none / adapter boundary | boundary constants | read-only structural ownership flags | none | substrate-independent boundary only | reusable implementation precedent, not feature computation |
| `SourceNavigation` | projected State fact/support rows + query | navigation view | query stripping, syntactic match rows, support counts, path values | `query.strip()` | repository source facts (`defines`, `imports`) | substrate-specific owner / diagnostic navigation owner |
| Campaign material preservation | selected lesson bytes/text | campaign record, manifest, annotations | bytes hash, exact selected line bounds, line count through manifest/projection | UTF-8 decode for bounded reporting | one campaign material selection | substrate-specific owner for campaign, reusable evidence precedent |

## 9. Raw feature classification

| Candidate feature | Line | Region | Raw-preserving | Normalization required | Interpretation risk | Classification |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| character count | yes | composable | yes | no | low | already implemented at line/artifact; region derivable from line text/counts if boundary defined |
| content character count excluding terminator | derivable | composable | yes | raw-preserving terminator separation | low | safe but absent |
| leading whitespace count | safe | composable as sequence/sum | yes | no if exact whitespace counted | low | safe but absent |
| trailing whitespace count | safe | composable as sequence/sum | yes | no if exact whitespace counted | low | safe but absent |
| whitespace character count | safe | composable | yes | category definition must be explicit | medium for Unicode category | safe but absent / unsupported for unsupported category policy |
| uppercase character count | safe | composable | yes | category definition must be explicit | medium: not heading/title | safe but absent |
| lowercase character count | safe | composable | yes | category definition must be explicit | medium: not language | safe but absent |
| digit count | safe | composable | yes | category definition must be explicit | low-medium | safe but absent |
| punctuation character count | safe | composable | yes | punctuation inventory definition must be explicit | medium: not grammar | safe but absent |
| punctuation inventory | safe | composable | yes | inventory definition explicit | medium | safe but absent |
| first character | safe for nonempty content | region has first line/content char | yes | no | low | safe but absent; Unknown for empty line/region |
| final content character | safe for nonempty content | region has final line/content char | yes | raw-preserving terminator separation | low | safe but absent; Unknown for empty content |
| exact prefix | safe if length is caller-selected | region sequence possible | yes | no | medium: prefix not shared meaning | requires explicit bounded parameter |
| exact suffix | safe if length is caller-selected | region sequence possible | yes | no | medium | requires explicit bounded parameter |
| exact text equality | safe | safe with referenced lines | yes | no | low if exact only | derivable from current owner because raw line text exists |
| repeated exact line | safe | safe as line-ID/text references | yes | no | low | derivable from current owner |
| line-length sequence | safe | natural for region | yes | no | low | derivable from current owner |
| blank/nonblank sequence | safe | projection already uses it | yes | blankness uses `strip()` after terminator separation | low | already implemented as `is_blank` plus regions |

## 10. Raw evidence boundary

Features can be recomputed from the current structural projection because line records retain raw `text`, character offsets, terminator presence, blankness, and region line IDs. The current projection retains enough line text to recompute line-level and region-composed raw features without reopening caller-supplied text. It does not retain separate raw region text, but region text can be reconstructed by concatenating referenced line texts in order.

Storing raw line or region text again in a future feature artifact would duplicate the structural projection and the caller-supplied exact text. An independently verifiable feature artifact can avoid embedding full text if it carries manifest/source/artifact IDs, artifact hash, projection convention, feature convention, referenced line IDs/region IDs, counts/inventories, unavailable/Unknown markers, and enough line/region coordinate provenance to recompute from the structural projection.

## 11. Normalization analysis

| Normalization | Lawful classification | Notes |
| --- | --- | --- |
| newline removal for line-content metrics | raw-preserving mechanical separation | Lawful only as recorded terminator separation, not source rewrite. |
| line terminator separation | raw-preserving mechanical separation | Already precedent: `has_line_terminator` and content extraction for blankness. |
| case folding | explicit caller-selected normalization / otherwise unsupported | Destroys raw case distinctions if silent. |
| whitespace collapsing | evidence-destroying unless explicitly caller-selected outside canonical raw projection | Collapses raw distinctions needed for evidence. |
| leading/trailing whitespace removal | evidence-destroying for feature projection, except non-mutating counts of leading/trailing whitespace | `strip()` is already used for blankness only; trimmed text should not replace raw text. |
| punctuation removal | evidence-destroying / unsupported | Would remove visible evidence. |
| Unicode normalization | unsupported / explicit caller-selected normalization | No implementation evidence warrants it here. |
| digit replacement | evidence-destroying / unsupported | Replaces raw evidence. |

## 12. Line-versus-region ownership analysis

The first feature artifact should be both line-level and region-level through one bounded projection over an existing structural projection. Evidence favors lines as the primitive owner: current canonical projection owns lines, region records only refer to line IDs and counts, and region features are deterministically composable from ordered line features. Evidence also favors region output because the current manual handoff begins at a mechanically projected region and asks a human to describe visible surface properties. A combined line+region feature projection would not compress two existing feature owners because no canonical feature owner exists yet; it would preserve the current structural owner and add a derived feature owner.

## 13. Selected lesson feature probe

The selected lesson has 4 physical lines, all nonblank, one region spanning lines 1-4, 1628 characters, SHA-256 `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`. Line content lengths excluding terminators are `[248, 464, 433, 479]`; all lines have zero leading and trailing whitespace; uppercase counts are `[23, 31, 29, 18]`; lowercase counts are `[167, 297, 298, 325]`; digit counts are `[1, 15, 0, 15]`; final content character is `.` on all four lines. Punctuation inventories by line are `+,-.?_`, `+-.?_`, `+,-.;_`, and `"+,-.;_`.

## 14. `AGENTS.md` feature probe

`AGENTS.md` has 61 physical lines, 22 nonblank regions, 2253 characters, SHA-256 `60d0a3b1eb5692ef0acc49058b303eb3fcca77e271b827c5c7d03589abc3afed`. Region line-count sequence is `[1,1,1,1,1,7,1,1,1,1,4,1,1,1,7,1,1,1,1,1,4,1]`. Blank/nonblank alternation is frequent: blank single-line separators occur after most single-line regions. Content lengths include many short one-line regions and longer bullet regions. All observed lines have zero leading and trailing whitespace in this file. Several nonblank lines begin with `#` or `-`; several final content characters are `.`, `:`, or ordinary letters.

## 15. Cross-substrate recurrence analysis

| Artifact | Region/line reference | Raw features observed | Recurrence candidates | Meaning remaining Unknown |
| -------- | --------------------- | --------------------- | --------------------- | ------------------------- |
| selected lesson | region 1, lines 1-4 | one 4-line nonblank region; line content lengths `[248,464,433,479]`; final `.` on all lines; punctuation contains `+`, `_`, `.`, and `-`; zero indentation | 4-line region recurs as a region length in `AGENTS.md`; zero leading/trailing whitespace recurs; final period recurs on many AGENTS lines; punctuation inventory overlaps partially | Whether lines are examples, rules, exercises, or prose units remains Unknown. |
| `AGENTS.md` | regions 11 and 21 | two 4-line regions, at lines 27-30 and 56-59; line content lengths `[47,152,56,61]` and `[60,49,39,70]`; bullet prefix `-` on all lines in these regions; zero indentation | 4-line region length recurs with lesson; short/long sequence inside region 11 includes one much longer line; final period recurs | Whether regions are lists, obligations, or sections remains Unknown for this audit. |
| both | all lines | zero leading/trailing whitespace in observed primary probes | exact whitespace-edge recurrence | Whether this reflects authoring convention, accident, or substrate rules remains Unknown. |
| both | punctuation inventories | shared visible punctuation characters include `.`, `-`, `_`; selected lesson also has `+`, `?`, `;`, comma, quote; `AGENTS.md` has `#`, backticks, slash, colon, angle brackets, equals | punctuation overlap can guide inventory design | Punctuation has no grammatical meaning here. |

Strongest observed mechanical recurrence: both primary artifacts expose a mechanically bounded 4-line nonblank region under the same producer, but with different visible prefixes and line-length distributions. Strongest counterexample: selected lesson has a single 4-line region with no blank separators and no repeated bullet prefix; `AGENTS.md` has 22 regions, many one-line regions, blank separators, and repeated `-` prefixes in multi-line regions. Therefore region length alone does not establish a shared responsibility or semantic structure.

## 16. Structuring-probe implications

Recurrence can lawfully improve probe questions without assigning semantics. It can ask whether a 4-line region recurs under unrelated substrates, whether stable blank-delimited boundaries coincide with repeated prefixes, whether short single-line regions adjacent to longer regions recur, and whether punctuation inventories provide bounded comparison handles. It cannot establish that a lesson region and a repository instruction region have the same responsibility.

## 17. Candidate responsibility-recovery implications

Before recurrence could support recovering a repository responsibility, Seed would need additional evidence: repetition across more independent substrates, stable producer/artifact/consumer roles, independent navigation or catalog testimony, replaceability, distinct failure behavior, downstream consumer pressure, and possibly manually known semantics used only as validation testimony. Surface recurrence alone is only question-generating testimony.

## 18. Failure and Unknown behavior

A future feature projection should preserve typed failures/Unknowns for missing structural projection, missing exact text, hash mismatch, unsupported encoding, empty line, empty region set, unsupported character category, unavailable feature, normalization not selected, no recurrence found, and recurrence inconclusive. Absence of a recurrence must not become structural dissimilarity unless the compared feature was available for both artifacts under the same feature convention.

## 19. Manual-handoff inventory

| Current human step | Mechanical? | Existing owner | Missing owner | Reducible now? |
| ------------------ | ----------: | -------------- | ------------- | -------------: |
| Human counts characters in a line | yes | structural line has `character_count`; manifest has artifact count | content-length excluding terminator convention for feature artifact | yes |
| Human notices one line is shorter/longer | yes | structural line count text length data | line-length sequence projection | yes |
| Human notices capitalization differs | yes if raw character category is explicit | none canonical for external material | uppercase/lowercase count owner | yes, with category caveat |
| Human notices punctuation recurs | yes if punctuation inventory is explicit | none canonical for external material | punctuation inventory/count owner | yes, with category caveat |
| Human notices region line-count patterns | yes | structural region has `line_count` | sequence/comparison owner | yes |
| Human labels heading/rule/example/exercise | no | campaign author testimony / documentation Markdown owner for docs only | semantic owner intentionally absent | no |

## 20. First reducible manual responsibility

The first reducible manual responsibility is: for each mechanically projected line and region, report raw line length/content-length and region line-length sequence so a human no longer manually counts or notices that one bounded region has four long lines while another has four shorter or varied lines.

## 21. Reusable owners

Closest lawful owner: `ExternalMaterialStructuralProjection`, because it is substrate-neutral, validates exact text identity, preserves raw line text, line IDs, character counts, blankness, and region line IDs, and refuses semantic correspondence. `StructureObservationBoundary` is a useful boundary precedent but does not compute features.

## 22. Missing owners

Missing owners are: canonical external-material raw surface-feature projection; typed feature-availability/Unknown behavior; cross-substrate mechanical recurrence testimony over feature artifacts; explicit punctuation/category convention owner; explicit parameterized prefix/suffix convention owner.

## 23. Missing roads

Missing road: `ExternalMaterialStructuralProjection` -> `ExternalMaterialSurfaceFeatureProjection` -> non-canonical, read-only recurrence testimony. Current road stops at lines and nonblank regions.

## 24. Strongest supporting evidence

Supporting evidence for a new bounded feature projection is that the current projection already preserves raw line text and mechanical boundaries, prior tests prove the same producer can project unrelated `AGENTS.md` without semantic correspondence, and the campaign boundary explicitly says the campaign author still identifies higher-level visible/semantic properties after mechanical projection.

## 25. Strongest counterevidence

The strongest counterevidence is that line `character_count`, `is_blank`, `has_line_terminator`, line raw text, region `line_count`, and region `line_ids` already make many features derivable, so a separate artifact risks duplicating current projection. Documentation structure also already computes line/byte/blank/heading/section metrics, but it is Markdown/docs-specific and would import substrate grammar. Character counting may be trivial enough to compute ad hoc, but repeated manual campaign handoffs and provenance requirements argue for canonical ownership if used by consumers.

## 26. Supported conclusions

Supported conclusions: the structural projection exists and retains raw line text; raw features can be recomputed from it without reopening caller text; no reusable canonical raw surface-feature projection exists; documentation/source-navigation feature implementations are too substrate-specific for this boundary; line features should be primitive and region features composed; recurrence improves questions but does not establish responsibilities.

## 27. Unsupported conclusions

Unsupported conclusions: a repeated 4-line region means the same structural responsibility; uppercase or `#` means heading; terminal `.` or `?` means a sentence/question; punctuation inventory has grammatical meaning; Markdown documentation structure should be reused for external material; normalization such as case folding or whitespace collapsing is lawful by default; semantic annotation is implemented or recoverable from these surfaces.

## 28. Primary classification

C. Mechanical line/region projection exists, but raw surface-feature projection is a genuinely missing responsibility.

## 29. Recurrence classification

2. Cross-substrate recurrence improves probe questions but does not yet warrant comparison implementation.

## 30. Exact next bounded boundary

Recovered responsibility: project raw, evidence-preserving line features and deterministically composed region feature summaries from an existing `ExternalMaterialStructuralProjection`.

Producer: a future external-material surface-feature projection producer, not implemented here.

Input artifact: existing `ExternalMaterialStructuralProjection`.

Output artifact: `ExternalMaterialSurfaceFeatureProjection` carrying projection identity, artifact identity/hash, line feature records, region feature summaries by referenced line IDs, feature convention, and Unknowns.

Consumer: campaign-author structural probe/reporting surfaces that currently require manual visible-feature descriptions.

Exact bounded question: for each projected line and nonblank region, what exact raw counts/inventories/sequences are visible without interpreting prose?

Explicit exclusions: semantic labels, normalized similarity, Markdown headings/sections, language tokens, parser output, recurrence comparison implementation, responsibility inference, text-store creation.

## 31. Implementation-warrant decision

One bounded implementation slice is warranted.

## 32. Files changed

This audit changes only `external_material_surface_feature_projection_topology_audit_001.md`.

## 33. Probes executed

- `rg -n "character_count|byte_count|line_count|whitespace|indent|uppercase|lowercase|punctuation|prefix|suffix|token|normalize" seed_runtime campaigns tests`
- `rg -n "ExternalMaterialStructuralProjection|ExternalMaterialStructuralLine|ExternalMaterialStructuralRegion|selected_lesson_006|AGENTS.md" seed_runtime campaigns tests *.md`
- `rg -n "DocumentationStructure|heading|section|blank_line|nonblank|surface|shape|recurrence|similar" seed_runtime campaigns tests`
- `sed` inspections of implementation and tests listed in this report.
- Read-only Python feature probe over exactly `selected_lesson_006.txt` and `AGENTS.md`.

## 34. Confidence statement

Confidence is high for the primary classification because the canonical structural owner retains raw text and mechanical regions but no searched/inspected implementation exposes a canonical external-material surface-feature projection. Confidence is medium for recurrence value because the two primary probes show lawful mechanical recurrences, but counterevidence shows the recurrences are too weak to implement comparison or infer responsibility now.
