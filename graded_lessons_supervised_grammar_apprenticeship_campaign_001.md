# Graded Lessons Supervised Grammar Apprenticeship Campaign 001

## 1. Bounded question

What can Seed currently do when it encounters attributed English instructional prose, exactly where must a human or campaign author still interpret the material, and what is the smallest missing responsibility that would reduce that manual assistance?

The preserved topology is:

```text
external public-domain material
→ exact attributed material preservation
→ human/campaign-author reading
→ caller-supplied structural testimony
→ CandidateExternalGrammarInput
→ CandidateExternalGrammarSet
→ deterministic Seed presentation
```

Seed did not read, understand, interpret, learn, verify, rank, or promote English grammar in this campaign.

## 2. Source artifact identity

| Field | Value |
|---|---|
| reported_title | Graded Lessons in English |
| reported_creator | Alonzo Reed and Brainerd Kellogg |
| source_url_or_archive_identity | Project Gutenberg eBook #7010 plain text; `https://www.gutenberg.org/ebooks/7010.txt.utf-8` redirected in the web retrieval view to `http://www.gutenberg.org/cache/epub/7010/pg7010.txt` |
| acquisition_method | Operator used the repository environment's web retrieval surface to inspect Project Gutenberg metadata and copied one bounded lesson excerpt without alteration into the campaign artifact. |
| acquired_at | 2026-07-14T00:00:00Z |
| content_type | text/plain selected excerpt from Project Gutenberg plain-text transcription |
| encoding | UTF-8 |
| byte_length | 1628 |
| sha256 | `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963` |
| reported_edition_or_transcription | Project Gutenberg eBook #7010; produced by Karl Hagen, Charles Franks, and the Online Distributed Proofreading Team; release date December 1, 2004; most recently updated December 30, 2020; revised edition, 1896 reported in text. |
| edition_relationship_unknowns | Full parent plain-text artifact was not committed; campaign preserves the selected excerpt hash, not a full-book byte hash. |
| raw_artifact_location | `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt` |

Identity distinctions preserved: historical work != printed edition != digital transcription != downloaded file != selected lesson != campaign annotations != candidate grammar.

## 3. Public-domain/source testimony

The web retrieval of Project Gutenberg metadata reported title, authors, eBook number 7010, language English, credits, release/update dates, and "Copyright Public domain in the USA." The selected artifact is treated only as external public-domain testimony copied from that source relationship.

## 4. Source hash and byte length

The campaign scaffold computes the selected artifact byte length and SHA-256 from the committed selected lesson file and validates them against constants:

```text
byte_length=1628
sha256=01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963
```

## 5. Selected lesson and exact bounds

| Field | Value |
|---|---|
| selected lesson | `LESSON 6. ANALYSIS.` |
| exact committed bounds | `selected_lesson_006.txt` lines 1-4 |
| retrieval-view bounds | Project Gutenberg web-rendered text lines 59-62 in the retrieval view |
| heading context | `LESSON 6. ANALYSIS.` |
| selection method | Campaign author selected the Project Gutenberg rendered plain-text lines corresponding to LESSON 6. |
| selector attribution | campaign author supplied |
| selection unknowns | Full parent-artifact byte offsets were not available in the repository environment; retrieval line numbers are not canonical Project Gutenberg file line numbers. |

## 6. Unaltered material preservation

The selected material is stored verbatim as external public-domain testimony in `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt`. The campaign-local scaffold reads it as bytes, hashes it, decodes it as UTF-8 only for bounded reporting, and does not parse its English.

## 7. Supervision trace

| step_id | material_reference | operation | supplied_by | bounded_output | uncertainty | explicitly_refused_claims |
|---|---|---|---|---|---|---|
| preserve_hash | selected_lesson_006.txt | hash source bytes | observer or import scaffold supplied | selected SHA-256 above | none for selected artifact bytes | Seed interpreted the prose |
| preserve_bounds | selected_lesson_006.txt:L1-L4 | preserve line boundaries | observer or import scaffold supplied | four UTF-8 text lines retained | parent byte offsets Unknown | Seed selected the pedagogically relevant lesson |
| annotate_rule | selected_lesson_006.txt:L2-L3 | this span appears to state a rule | campaign author supplied | `ann_rule_subject`; `ann_rule_predicate_analysis` | human interpretation | Seed verified the rule |
| annotate_examples | selected_lesson_006.txt:L1-L3 | this span appears to be an example | campaign author supplied | `ann_model_intemperance`; `ann_model_stars` | human interpretation | Seed classified examples autonomously |
| render_candidates | CandidateExternalGrammarInput | render caller-supplied structures | Seed supplied | deterministic human and JSON candidate output | strings preserved but not bound by schema | Seed ranked, verified, or promoted a candidate |

## 8. Material annotations

Each annotation is caller-supplied campaign testimony. None establishes grammar truth.

| annotation_id | material_reference | annotation_kind | bounded_annotation | supplied_by | unknowns |
|---|---|---|---|---|---|
| ann_rule_subject | selected_lesson_006.txt:L2:sentences 13-15 | candidate_rule_statement | campaign author reports that the span appears to define Subject. | campaign author supplied | Correctness is not established. |
| ann_rule_predicate_analysis | selected_lesson_006.txt:L3:sentences 1-2 | candidate_rule_statement | campaign author reports that the span appears to define Predicate and Analysis. | campaign author supplied | Correctness is not established. |
| ann_model_intemperance | selected_lesson_006.txt:L1-L2:Model Intemperance degrades exchange | candidate_example | campaign author reports that the span appears to present a labeled model example. | campaign author supplied | Seed does not decide whether the model is grammatically correct. |
| ann_model_stars | selected_lesson_006.txt:L3:Model Stars twinkle explanation | candidate_example | campaign author reports that the span appears to present a second labeled model example. | campaign author supplied | Seed does not compare it autonomously with the first model. |
| ann_exercise_numbered | selected_lesson_006.txt:L2:numbered items 1-12 and L4:numbered items 1-12 | candidate_exercise_instruction | campaign author reports that the numbered sentence lists appear to request analysis by the model. | campaign author supplied | The exercise purpose is human testimony, not Seed inference. |
| ann_label_subject_predicate | selected_lesson_006.txt:L2:terms `_+Subject+_` and `_+Predicate+_` | candidate_label | campaign author reports that the highlighted terms appear to label grammatical categories. | campaign author supplied | Label/category relationship remains Unknown. |
| ann_ambiguous_models | selected_lesson_006.txt:L1-L3:two `+Model+` spans | unknown | campaign author reports uncertainty whether the two model spans are complementary examples or a repeated teaching pattern. | campaign author supplied | Seed preserves the ambiguity without resolving it. |

## 9. Candidate grammar input

A real `CandidateExternalGrammarInput` is constructed by the campaign scaffold using three caller-supplied candidates:

1. `gl001_pair_label_example`: the lesson may pair highlighted category labels with model sentences and explanations.
2. `gl001_repeated_two_part_structure`: the lesson may present sentences as divisible into two named parts before asking for repeated analysis.
3. `gl001_model_then_exercise`: the lesson may use a model-then-exercise pattern.

All candidates cite exact strings of the form:

```text
source:gl001:selected_lesson_006:<line/span>#<annotation_id>
```

## 10. Candidate grammar output

The existing canonical surface assembled a `CandidateExternalGrammarSet` with:

```text
read_only: true
writes_event_ledger: false
mutates_cluster: false
```

Its boundary notes preserve that candidate grammars are caller-supplied hypotheses, supporting and contradicting testimony is preserved rather than evaluated, no candidate is selected or verified, absence of support is not contradiction, absence of contradiction is not verification, and no translator readiness or capability is established.

## 11. Exact testimony-reference topology

```text
Project Gutenberg eBook #7010 metadata and plain-text rendition
→ campaign selected excerpt selected_lesson_006.txt@sha256:01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963
→ line/span material references such as selected_lesson_006.txt:L2
→ campaign annotations such as ann_rule_subject
→ string testimony references in CandidateExternalGrammarInput
→ preserved strings in CandidateExternalGrammarSet human and JSON output
```

## 12. External-source responsibilities

External source supplied: attributed prose, title, authorship, public-domain/source metadata, eBook identity, and lesson text.

## 13. Observer/import responsibilities

Observer or import scaffold supplied: byte hashing, byte-length calculation, selected artifact loading, line-boundary preservation, local record assembly, candidate input construction from fixed campaign testimony, and deterministic output capture.

## 14. Campaign-author responsibilities

Campaign author supplied: lesson selection, span references, all interpretive annotations, structural candidate wording, support/contradiction mapping, Unknowns, and answers to campaign questions.

## 15. Operator responsibilities

Operator supplied: campaign request, source requirement, bounded scope, classification options, strict exclusions, expected diff guardrails, and the repository environment.

## 16. Seed-owned responsibilities

Seed supplied: structural validation of `CandidateExternalGrammarInput`, candidate identity preservation, testimony string preservation, contradiction and Unknown preservation, read-only/non-mutating `CandidateExternalGrammarSet`, deterministic human output, and deterministic JSON output.

## 17. Unknowns

- Full parent-artifact byte offsets are Unknown.
- Full parent plain-text artifact hash is not preserved because the full book was not committed.
- Retrieval-view line numbers are not canonical source-file line numbers.
- Correctness of all grammatical interpretations remains Unknown.
- Whether highlighted terms are category labels or merely presentation emphasis remains Unknown.
- Whether model spans are examples, exercises, or classroom script remains Unknown.

## 18. Current manual handoffs

1. Selecting a bounded lesson from the external source.
2. Identifying span boundaries within the selected lesson.
3. Labeling spans as rule statement, example, contrast, exercise instruction, or category label.
4. Describing candidate structural claims.
5. Mapping supporting and contradicting testimony references.

## 19. Mechanically recoverable responsibilities

- Hashing bytes.
- Recording byte length.
- Preserving line boundaries.
- Detecting repeated typography tokens such as `+Model+`, `+DEFINITION.--`, and numbered list markers.
- Producing stable material span identifiers for detected bounded regions.

## 20. Responsibilities requiring prose competency

- Deciding that a span is a rule statement rather than a quotation or classroom prompt.
- Deciding that examples are intentionally contrasted or complementary.
- Inferring instructional purpose from exercise wording.
- Verifying category-label semantics.
- Generating grammar candidates from prose without caller testimony.

## 21. Evidence for and against current testimony-reference sufficiency

For sufficiency: current string references survive the canonical handoff unchanged; they can contain source identity, selected lesson identity, line/span hints, and annotation ids; contradictions can point to the same style of reference.

Against sufficiency: the references are opaque strings; `CandidateExternalGrammarSet` does not validate that a cited source exists, that a line/span exists, that an annotation id exists, that a hash matches, or that two candidates refer to the same immutable material. This is sufficient for preservation but insufficient for safe binding.

## 22. Next missing road

The evidence selects:

```text
candidate testimony reference
→ exact external material binding
```

This is selected because external material was preserved, annotations could be represented honestly, and candidate testimony survived the handoff, but the binding remained string-only and unvalidated.

## 23. Exact next bounded slice

Recovered responsibility: validate a campaign-local testimony reference against a bounded material artifact manifest.

Producer: observer/import scaffold.

Artifact or handoff: `source_id + selected_artifact_sha256 + line/span + optional annotation_id` reference object.

Consumer: candidate grammar campaign harness before constructing `CandidateExternalGrammarInput`.

Exact bounded question: Can a campaign-local validator prove that every candidate testimony reference resolves to an existing selected external material span and, when supplied, an existing campaign annotation id, without interpreting the prose?

Explicit exclusions: no English parsing, no semantic interpretation, no grammar induction, no candidate ranking, no canonical `CandidateExternalGrammarSet` schema change, no permanent book corpus, no Project Gutenberg-specific architecture.

## 24. Implementation-warrant decision

One bounded implementation slice is warranted.

## 25. Files changed

- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py`
- `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/selected_lesson_006.txt`
- `tests/test_graded_lessons_campaign_001.py`
- `graded_lessons_supervised_grammar_apprenticeship_campaign_001.md`

## 26. Tests and commands executed

- `pytest -q tests/test_graded_lessons_campaign_001.py` — passed.
- `python - <<'PY' ... candidate output capture ... PY` — passed.
- `git diff --stat` — executed before commit.
- `git diff --numstat` — executed before commit.
- `git diff --check` — executed before commit.
- `git status --short` — executed before commit.

## 27. Confidence statement

Confidence is high that the campaign preserved a real bounded public-domain lesson excerpt, preserved caller-supplied annotations and testimony strings, and demonstrated deterministic non-mutating candidate grammar handoff. Confidence is lower for full parent-artifact provenance because the full Project Gutenberg artifact was not committed or hashed; this limitation is explicitly recorded as an Unknown rather than converted into a Seed capability claim.

## Campaign questions answered

1. Seed can preserve the selected real lesson bytes without interpreting them; full parent artifact preservation was intentionally not committed.
2. Exact material spans can be referenced as strings from candidate testimony.
3. Current string testimony references are sufficient for preservation, but not sufficient for safe binding.
4. Rule, example, exercise, label, ambiguity, and candidate-claim annotations required human reading.
5. Repeated `+Model+`, `+DEFINITION.--`, highlighted terms, and numbered-list regions could be mechanically detected as layout/typography regions.
6. Seed cannot compare two examples structurally today without campaign-author description.
7. Seed cannot autonomously distinguish rule statement, example, exercise, and category label.
8. Seed can preserve competing interpretations of one passage as unresolved alternatives or contradicting testimony strings.
9. Contradiction or ambiguity can be tied to exact source spans as strings, but not schema-validated bindings.
10. `CandidateExternalGrammarSet` contains enough provenance strings to walk back manually, but not enough typed provenance to prove the walk-back safely.
11. Seed contributed validation, preservation, refusal boundaries, non-mutation flags, and deterministic rendering.
12. The campaign author contributed source selection, annotations, candidates, reference strings, and interpretation.
13. Before “Seed read this lesson” became truthful, implementation would need autonomous material-region identification, structural comparison, prose-role classification, and candidate generation with verifiable evidence boundaries.
14. The first manual handoff to reduce is string testimony reference binding to exact external material.
15. The smallest next bounded implementation slice is a campaign-local reference resolver/validator for selected material spans and annotation ids.

## Campaign classification

A. A real grammar lesson completed the supervised candidate-preservation path end to end.

One bounded implementation slice is warranted.

- recovered responsibility: validate campaign-local testimony references against a bounded external material manifest
- producer: observer/import scaffold
- artifact or handoff: selected-material reference object with source id, selected artifact hash, exact line/span, and optional annotation id
- consumer: campaign harness before `CandidateExternalGrammarInput`
- exact bounded question: Can every candidate testimony reference resolve to an existing selected external material span and optional campaign annotation id without interpreting the prose?
- explicit exclusions: no English parsing; no semantic interpretation; no grammar induction; no ranking; no canonical `CandidateExternalGrammarSet` schema change; no permanent corpus; no Project Gutenberg-specific architecture.
