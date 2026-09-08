# Source Navigation District Scout 001

## District consistency verification

- Active district verified: **Source Navigation**.
- Handoff source verified: **`knowledge_reachability_outward_scout_003.md`**.
- Completed source district verified: **Knowledge Reachability**.
- Latest completed Knowledge Reachability slice verified: **`knowledge_reachability_slice_006.md`**.
- Latest Knowledge Reachability stopping scout verified: **`knowledge_reachability_district_scout_002.md`**.
- No local report, summary, branch state, or implementation file was found that redirected this scout to another active district.
- Knowledge Reachability reports were used only for handoff and exhaustion context. They were not used as authority for Source Navigation internals.
- Unrelated district reports were ignored as authority; prior district boundaries were used only as re-slice constraints.

Verification commands run before scouting:

```sh
rg -n "Source Navigation|knowledge_reachability_outward_scout_003|knowledge_reachability_slice_006|knowledge_reachability_district_scout_002" -S .
sed -n '1,340p' seed_runtime/source_navigation.py
sed -n '340,560p' seed_runtime/source_navigation.py
sed -n '1,700p' tests/test_source_navigation.py
python scripts/seed_local.py --source-navigation state_summary
```

## Current Source Navigation implementation evidence

Source Navigation is implemented in `seed_runtime/source_navigation.py` as a read-only projection over existing `imports` and `defines` fact supports. The module-level contract explicitly says it does not inspect files, parse source, ingest observations, or infer behavior, reachability, or ownership.

The public builder path is:

1. `build_source_navigation(state, query)` prepares the external query and delegates composition.
2. `_prepare_source_navigation_query(state, query)` strips the query and converts all projected `FactSupport` rows into `SourceNavigationRow` rows.
3. `_compose_source_navigation(prepared_query)` performs match selection, definition/import separation, bounded lookup detection, dependency mention selection, and explanation/view assembly.
4. `format_source_navigation(view)` renders the human view.
5. `source_navigation_json(view)` renders the stable JSON-compatible view.

The current tests show existing coverage for query handoff, composition equivalence, definition explanation JSON/human output, dependency explanation JSON/human output, support explanation JSON/human output, non-claims, short/qualified/module/path lookups, repeated observations, read-only behavior, bounded rendering, support summaries, and deterministic rendering.

The app command `python scripts/seed_local.py --source-navigation state_summary` returned the Source Navigation view with unknown definition/dependency/support status and explicit non-claims, then `No source facts matched.` This was treated as app behavior evidence only, not semantic authority.

## Inspected Source Navigation neighborhoods

### 1. External query preparation

Evidence inspected:

- `_prepare_source_navigation_query(...)` strips the external query and constructs `_PreparedSourceNavigationQuery` with normalized query plus all `SourceNavigationRow` values.
- Tests assert the private handoff carries only prepared input and not definitions, imports, or repository-artifact explanation fields.
- `build_source_navigation(...)` delegates from preparation into composition.

Scout result: **C. Already separated / likely re-slice**.

Reasoning: The query-intake boundary is already a distinct private handoff with focused tests. Recovering it again would re-slice existing External Orientation / Source Navigation Query Intake work and would not produce a new implementation-local ownership boundary.

### 2. Match selection and definition/import separation

Evidence inspected:

- `_matches(...)` owns source predicate filtering plus exact subject/path matching and definition-value/final-segment matching.
- `_dependency_mentions(...)` separately owns import dependency mention matching.
- `_compose_source_navigation(...)` still owns collecting matched rows and splitting them into sorted `definitions` and `imports`.
- Tests cover short symbol lookup, qualified symbol lookup, module lookup, path lookup, and import behavior.

Scout result: **B. Possible but needs caution**.

Reasoning: There is implementation-backed pressure because `_compose_source_navigation(...)` still performs selection and classification before explanation assembly. However, the primitive predicates are already separate helpers, and the behavior is tightly coupled to public `definitions` / `imports` fields and lookup semantics. A future slice could recover a narrow **source-navigation match-set assembly** helper only if it preserves the exact rows, sorting, query semantics, JSON, formatter behavior, read-only behavior, and tests. This candidate is not merely a name because it is supported by concrete code paths and tests, but it needs caution because over-broad extraction would collide with already separated `_matches(...)`, `_dependency_mentions(...)`, or public view assembly.

### 3. Bounded path/module status derivation

Evidence inspected:

- `_compose_source_navigation(...)` computes `bounded` from whether the normalized query matches row subject or path in definitions/imports.
- `_is_path_or_module_lookup(view)` recomputes boundedness for formatting from the completed view.
- `_definition_explanation(...)` and `_dependency_explanation(...)` suppress representative fact/support ids when bounded.
- `format_source_navigation(...)`, `_section_heading(...)`, `_format_rows(...)`, and `_format_support_summary(...)` apply bounded output rules.
- Tests cover bounded path/module rendering, support-summary availability, and exact-symbol visibility.

Scout result: **B. Possible but needs caution**.

Reasoning: Boundedness appears in two phases: composition-time explanation shaping and formatting-time row rendering. A compatibility-preserving slice might recover an implementation-local **bounded source-navigation lookup policy** helper used by both phases. This is implementation-backed, not merely a presentation label, because it changes structured explanation identities as well as human rendering. It is not a re-slice of Knowledge Reachability, Operational Graph, or prior audit districts. However, it is sequential/cautious because it may become clearer after any match-set assembly slice, and it touches public schema-sensitive representative-id behavior.

### 4. Repository artifact explanation assembly

Evidence inspected:

- `_definition_explanation(...)`, `_dependency_explanation(...)`, `_support_explanation(...)`, and `_non_claims_explanation(...)` already exist as separate helpers.
- Dedicated dataclasses and `to_json_dict(...)` methods exist for definition, dependency mention, dependency explanation, support explanation, and non-claims.
- Tests separately assert JSON and human output for each explanation family and guard against behavior, reachability, ownership, truth, call graph, dependency correctness, and semantic-relevance claims.

Scout result: **C. Already separated / likely re-slice**.

Reasoning: The explanation families are already individually separated with direct tests. A future command that merely renames or rewraps definition/dependency/support/non-claim explanation assembly would likely be cosmetic or a re-slice. A targeted slice could be justified only if a concrete failing behavior appears; this scout did not find one.

### 5. Human/table formatting and JSON/public output

Evidence inspected:

- `format_source_navigation(...)` owns operator-facing text composition and delegates to `_format_definition_explanation(...)`, `_format_dependency_explanation(...)`, `_format_support_explanation(...)`, `_format_non_claims_explanation(...)`, `_section_heading(...)`, `_format_rows(...)`, and `_format_support_summary(...)`.
- `source_navigation_json(...)` owns stable JSON payload assembly and delegates row serialization to `_row_json(...)` and dataclass `to_json_dict(...)` methods.
- Tests assert JSON/human parity for each repository-artifact explanation family, deterministic rendering, bounded rendering, and no-match output.

Scout result: **C/D. Already separated / cosmetic only unless a failing compatibility gap appears**.

Reasoning: Formatting and JSON behavior are public compatibility surfaces. They are covered and helperized. Extracting further without a failing surface would mostly move presentation strings or schema keys and risk breaking public output without recovering a true ownership boundary.

### 6. CLI dispatch, Question Surface Inventory, bounded ask, and Inquiry Orientation

Evidence inspected:

- `scripts/seed_local.py` exposes `--source-navigation` as a read-only CLI flag and dispatches to `format_source_navigation(build_source_navigation(...))`.
- `seed_runtime/question_surface_inventory.py` maps the source-navigation question family/surface to `source_navigation` and `--source-navigation`.
- `seed_runtime/inquiry_orientation.py` consumes Source Navigation through `build_source_navigation(...)` to produce related material from lexical token matches.

Scout result: **Outward compatibility evidence only**.

Reasoning: These call sites are compatibility surfaces and consumers, not Source Navigation internals. Direct work there would risk drifting into Question Surface Inventory, bounded ask, or Inquiry Orientation rather than recovering a Source Navigation ownership boundary.

## Recently consumed Knowledge Reachability boundaries respected

The following Knowledge Reachability boundaries are unavailable and were not proposed as Source Navigation slices: candidate discovery and admission, source-budget behavior, global limit behavior, subject bypass behavior, raw/source/scan counts, effective limit, skipped count, truncation state, `_CandidateAdmission` handoff, staged/preserved/projected/read-model/source-navigation/inquiry index construction, timing/counter metadata, candidate evaluation and first-loss row production, public result metadata, JSON payload construction, table/human formatting, and their row/metadata/schema aliases.

Source Navigation match selection and bounded lookup policy were considered only as direct `seed_runtime/source_navigation.py` responsibilities, not as Knowledge Reachability source-navigation-term admission or index construction.

## Prior district boundaries avoided

This scout avoided re-slicing:

- Operational Graph graph composition, node/edge registry, confidence aggregation/filtering, and confidence summary work.
- Emitter Attribution Audit unknown-emitter classification and evidence/row construction work.
- Emitter/Consumer Audit scan-result, relationship-status, unknown-emitter, emitted-item, and final assembly work.
- Consumer Dependency Audit observation-predicate, diagnostic item-family, and matched group construction work.
- Frontier Pressure Admission candidate admission, source fan-out, evidence payload, score production, refusal, and item-set selection work.

No candidate proposed here constructs operational graphs, emitter/consumer relationships, consumer dependency groups, pressure scores, or Knowledge Reachability candidates.

## Stopped and exhausted neighborhoods respected

The stopped/exhausted neighborhoods listed for selection path audit, diagnostic-shape pressure construction, pressure-audit, Consumer Dependency Audit, Emitter/Consumer Audit, Emitter Attribution Audit, Operational Graph, Knowledge Reachability, and Knowledge Reachability-led outward scouting were treated as closed. No candidate proposes work in those neighborhoods.

## Candidate boundaries found

### Candidate 1: Source-navigation match-set assembly

- Rank: **B. Possible but needs caution**.
- Classification: **Independent**.
- Confidence: **Medium**.
- Recoverable candidate? **Yes, cautious**.
- What is compressed: `_compose_source_navigation(...)` still directly collects matched rows, sorts definitions/imports, and selects dependency mentions before explanation/view assembly.
- Implementation evidence: `_compose_source_navigation(...)`, `_matches(...)`, `_dependency_mentions(...)`, `_row_sort_key(...)`, and lookup tests for short symbol, qualified symbol, module, path, and dependency mention behavior.
- Inside Source Navigation? **Yes**.
- Distinct from Knowledge Reachability Slices 001-006? **Yes**; it does not admit Knowledge Reachability candidates or build/evaluate/format Knowledge Reachability output.
- Distinct from prior Operational Graph / Emitter Attribution / Emitter-Consumer / Consumer Dependency / Frontier Pressure Admission slices? **Yes**.
- Compatibility preservation: Must preserve `SourceNavigationView.definitions`, `imports`, dependency mentions, sorting, JSON, formatter output, read-only behavior, and CLI behavior.
- Would it still be valid without the other candidates? **Yes**. It can be recovered without changing bounded policy or formatting if scoped narrowly to a private handoff such as matched definitions/imports/dependency mentions.
- Why it is not a re-slice: Prior consumed work did not recover Source Navigation match-set assembly; the existing query handoff is separate, but composition still owns this match grouping.
- Why it is not merely a name: It corresponds to concrete row-selection and sort operations used by public view fields and covered lookup behavior.

### Candidate 2: Bounded source-navigation lookup policy

- Rank: **B. Possible but needs caution**.
- Classification: **Sequential**.
- Confidence: **Medium-Low**.
- Recoverable candidate? **Possibly, after reassessment**.
- What is compressed: bounded path/module status is computed in composition for explanation representative-id suppression and recomputed in formatting for row truncation/support-summary behavior.
- Implementation evidence: `_compose_source_navigation(...)` bounded calculation, `_is_path_or_module_lookup(...)`, `_definition_explanation(...)`, `_dependency_explanation(...)`, `_section_heading(...)`, `_format_rows(...)`, `_format_support_summary(...)`, and bounded rendering/support tests.
- Inside Source Navigation? **Yes**.
- Distinct from Knowledge Reachability Slices 001-006 and prior districts? **Yes**.
- Compatibility preservation: Must preserve bounded JSON representative-id suppression, human row limits, support summary wording, exact symbol expansion, CLI output, and read-only behavior.
- Would it still be valid without the other candidates? **Possibly**, but reassessment is required. If Candidate 1 lands first, boundedness may have a clearer input structure. If Candidate 1 does not land, boundedness may still be recoverable, but the slice risks mixing composition and formatting concerns.
- Why it is not a re-slice: It is not Knowledge Reachability source-budget/effective-limit/truncation behavior; it is Source Navigation path/module bounded visibility over source facts.
- Why it is not merely a name: It has concrete behavior in both structured explanations and rendered output, with tests proving bounded versus exact lookup differences.

## Rejected candidates

- **External query preparation** — **C. Already separated / likely re-slice**. `_PreparedSourceNavigationQuery` and tests already separate query normalization and source-row preparation.
- **Definition explanation assembly** — **C. Already separated / likely re-slice**. Dedicated dataclass, JSON conversion, formatter helper, and tests already isolate this family.
- **Dependency explanation assembly** — **C. Already separated / likely re-slice**. Dedicated dataclasses/helpers/tests already isolate dependency mentions and boundaries.
- **Support explanation assembly** — **C. Already separated / likely re-slice**. Dedicated helper/dataclass/tests already isolate support counts, representatives, paths, and boundaries.
- **Non-claims explanation assembly** — **C/D. Already separated / cosmetic only**. Current work would likely only move boundary strings.
- **Human formatting** — **C/D. Already separated / cosmetic/public compatibility**. Existing formatter helpers and tests make further extraction risky without a failing behavior.
- **JSON serialization** — **C/D. Already separated / public schema risk**. Current serializer is small and stable; schema-key movement would be compatibility-sensitive.
- **CLI dispatch** — **Outward compatibility only**. It proves the public command path but is not Source Navigation internal ownership.
- **Question Surface Inventory linkage** — **Outward compatibility only**. It belongs to inventory, not Source Navigation internals.
- **Inquiry Orientation consumption** — **Outward compatibility only**. It consumes Source Navigation rows but owns related-material selection outside this district.

## Candidate independence answer

How many recoverable candidates currently exist? **2**.

1. **Source-navigation match-set assembly**
   - Classification: **Independent**.
   - Confidence: **Medium**.
   - Not a re-slice because prior consumed boundaries did not recover Source Navigation row-match grouping; existing query handoff and predicate helpers do not own the full match-set handoff.
   - Not merely a name because it maps to specific selection, sorting, and grouping code that feeds public definitions/imports/dependency behavior.

2. **Bounded source-navigation lookup policy**
   - Classification: **Sequential**.
   - Confidence: **Medium-Low**.
   - Not a re-slice because Source Navigation bounded path/module display and representative-id suppression are separate from Knowledge Reachability truncation/source-budget work.
   - Not merely a name because it changes concrete JSON and human visibility behavior for path/module lookups versus exact symbol lookups.

Fewer than three implementation-backed candidates are supported. A third safe candidate was not found. Explanation assembly, JSON, formatting, query preparation, CLI, Question Surface Inventory, bounded ask, and Inquiry Orientation are either already separated, public compatibility surfaces, outward evidence, or likely re-slices.

## Batch efficiency gate

- Discovered queue: **Protection batch**, not an efficiency batch.
- Recoverable candidates: **2**.
- Recommended batch size: **1 initially**, despite two candidates existing.
- Batch worth it for speed? **No**. Two candidates do not save command count compared to old one-slice prompting.
- Batch worth it for process protection? **Only if the next command is explicitly guarded and reassesses Candidate 2 after Candidate 1**. Because Candidate 2 is sequential and public-shape-sensitive, the safer next move is a single slice for Candidate 1.

## Recommended next command

Recommended next command: perform **one Source Navigation slice** to recover only **source-navigation match-set assembly** from `_compose_source_navigation(...)` into a private implementation-local handoff/helper, preserving all public behavior and tests.

The next move classification is: **single-slice target**, even though the broader queue has two possible candidates, because the second candidate should be reassessed after the first slice and is not safe for an efficiency batch.

Do not run an efficiency batch. Do not recover bounded lookup policy in the same command unless the command is explicitly a protection batch and requires reassessment between slices.

## Risk of re-slicing prior work

Risk is **medium** if the next command stays narrowly inside `seed_runtime/source_navigation.py` and only extracts match-set assembly with unchanged behavior.

Risk is **high** if the next command moves public JSON keys, formatter wording, non-claim vocabulary, CLI dispatch, Question Surface Inventory rows, Knowledge Reachability source-navigation candidate admission/indexes, Inquiry Orientation related-material selection, or any prior exhausted audit/graph/pressure neighborhood.

## Read-only scout statement

This scout was read-only with respect to implementation and tests. No implementation files were changed. No test files were changed. No slice report was created. The only intended repository change is this scout report: `source_navigation_district_scout_001.md`.

## Scout report commit

Commit hash: `e0d4ec28fb5d16245bc54bd751eff39ccadae745`.
