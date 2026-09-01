# Answer Support Relationships Investigation

This investigation is observational. It uses existing app surfaces and repository implementation to determine whether Seed already preserves enough implementation evidence to answer: `Where did this answer come from?` It does not implement an answer-support surface, add explanation generation, or infer relationships not already present in implementation.

## Implementation summary

Existing implementation preserves several support relationships for inquiry answers:

1. **Question Family -> answering surface -> CLI flag -> bounded dispatch surface** is preserved by `QuestionSurfaceInventoryRow` plus bounded ask dispatch maps.
2. **Diagnostic surface -> operational shape declaration** is preserved by `DiagnosticInventoryEntry`.
3. **Diagnostic surface -> implementation spec -> module/build/format/json functions -> observed shape fields** is preserved by diagnostic shape audit specs and audit rows.
4. **Answer payload -> immediate evidence fields** is preserved inside individual evaluators such as service ownership authority and knowledge reachability.
5. **Trait -> recurring concern -> exposing inventory surfaces** is preserved by implementation trait characterization.

The repository does **not** currently preserve one normalized, connected chain from a concrete answer payload back through all of those relationships. Existing links are implementation-backed but distributed across independent surfaces.

## Representative inquiry relationship table

| Inquiry surface | Question Family relationship | Dispatch / CLI relationship | Evidence-source relationship | Shape / boundary relationship | Answer-payload support relationship | Implementation-backed gap |
|---|---|---|---|---|---|---|
| `service_ownership_authority` | Question inventory row maps `authority-constrained service ownership` to surface `service_ownership_authority` and flag `--service-ownership-authority`. | Bounded dispatch map maps the same family to dispatch surface `service_ownership_authority`; the row is enriched as `eligible_now`. | Diagnostic inventory declares projected state, repo files, diagnostic facts; implementation spec names `build_observation_inventory` and `build_capability_needs` markers. | Diagnostic inventory and shape audit declare/read `supports_json`, `supports_record=false`, `record_scope=none`, `writes_event_ledger=false`, `mutates_cluster=false`; payload also has a `boundary` object. | Evaluator output preserves desired observation, required observations, required authority, available authority, reachable/blocked observations, blocked details, outcome, strategy, uncertainty, and blocking boundary. | The payload does not point back to its Question Family row, diagnostic inventory row, or shape-audit implementation spec. |
| `operational_pressure` / `ops_brief` | Question inventory row maps `operational pressure` to surface `ops_brief` and flag `--ops-brief`. | Bounded dispatch map maps the same family to dispatch surface `ops_brief`; the row is enriched as `eligible_now`. | Diagnostic inventory declares projected state, repo files, diagnostic facts; implementation spec names repo markers including observation inventory, consumer audit, diagnostic shape audit, and snapshots. | Diagnostic inventory and shape audit preserve non-recording/read-only shape fields. | `OpsBrief` payload preserves composed sections: observations, ownership, capabilities, diagnostics, snapshots, and recommended actions; builder calls existing surfaces for those sections. | The output sections do not carry provenance pointers to the exact component builder calls or inventory rows used to produce each section. |
| `knowledge_reachability` | Question inventory row maps `knowledge reachability` to surface `knowledge_reachability` and flag `--knowledge-reachability-audit`. | Bounded dispatch map maps the family to `knowledge_reachability_audit`; the row is enriched as `eligible_now`. | Diagnostic inventory declares projected state and repo files; implementation scans default seeds, event payloads, projected state, docs, seed runtime files, and source-navigation terms as candidate sources. | Diagnostic inventory and shape audit preserve JSON/non-recording/non-mutating shape fields. | Audit metadata preserves timings, candidate counts, kind counts, source counts, indexes, cache state, scan counts, truncation reason, and rows preserve family/kind/candidate/stage booleans/first loss. | The reachability rows identify staged visibility, but not a normalized link from a rendered answer to the specific Question Family, dispatch row, or diagnostic implementation spec. |
| `implementation_trait_characterization` | There is no Question Surface Inventory row for this diagnostic in the current question-family inventory. | There is no bounded ask dispatch row for this surface; it is exposed as a diagnostic surface. | Diagnostic inventory declares no projected state, repo files, or diagnostic-fact reads; implementation consumes static dataclass fields from diagnostic inventory, projected-state consumers, question-surface inventory, and operational-surface inventory. | Diagnostic inventory and shape audit preserve JSON/non-recording/non-mutating shape fields. | Output maps traits to concerns (`evidence_source`, `operational_boundary`, `dispatchability`, `implementation_capability`) and lists exposing surfaces and implementation meanings. | It exposes recurring support vocabulary, but it is disconnected from concrete inquiry answers and concrete answer rows. |

## Relationships already contributing to inquiry answers

| Relationship | Implementation evidence | Surfaces where observed |
|---|---|---|
| Question Family names the bounded question class. | `QuestionSurfaceInventoryRow.question_family` is a field; rows include `operational pressure`, `knowledge reachability`, and `authority-constrained service ownership`. | `ops_brief`, `knowledge_reachability`, `service_ownership_authority` |
| Question Family maps to answering surface and CLI flag. | Question inventory rows store `surface` and `surface_flag`. | `ops_brief`, `knowledge_reachability`, `service_ownership_authority` |
| Bounded ask dispatch maps eligible families to dispatch attributes. | `BOUNDED_ASK_DISPATCH_SURFACES` maps `operational pressure` to `ops_brief`, `knowledge reachability` to `knowledge_reachability_audit`, and `authority-constrained service ownership` to `service_ownership_authority`. | `ops_brief`, `knowledge_reachability`, `service_ownership_authority` |
| Required surface args are preserved when they exist. | `BOUNDED_ASK_REQUIRED_SURFACE_ARGS` exists and enrichment copies `required_surface_args`; none of the four required representative surfaces require args. | All dispatchable question rows, with explicit empty args for selected surfaces |
| Operational boundary is preserved as inventory metadata. | Question rows have `authority_boundary`; diagnostic inventory has `supports_record`, `record_scope`, `writes_event_ledger`, `mutates_cluster`, and related fields. | All four selected surfaces through diagnostic inventory; three through question inventory |
| Evidence-source declarations are preserved. | Diagnostic inventory declares `uses_projected_state`, `uses_repo_files`, and `reads_diagnostic_facts`. | All four selected surfaces |
| Implementation entry points are preserved for diagnostic surfaces. | Shape audit specs include `module_path`, `build_function`, `format_function`, `json_function`, and CLI flags. | All four selected surfaces |
| Static shape validation links declarations to observed code markers. | Shape audit rows compare declared and observed values for support, record, event ledger, repo, projection, diagnostic-fact, and mutation fields. | All four selected surfaces |
| Answer payload carries domain-specific immediate support. | `ServiceOwnershipAuthoritySlice` carries observations/authority/blockers; `KnowledgeReachabilityAuditResult` carries rows and metadata; `OpsBrief` carries composed sections; implementation trait characterization carries trait concern rows. | All four selected surfaces |

## Recurring support relationships

These relationships recur across multiple inquiry surfaces and are supported by implementation evidence:

| Recurring relationship | Evidence | Recurrence |
|---|---|---|
| Surface is registered with read-only/no-cluster-mutation operational shape. | Diagnostic inventory rows repeatedly declare `writes_event_ledger=false` and `mutates_cluster=false`; shape audit checks the same fields. | All four selected surfaces. |
| Surface has JSON visibility. | Diagnostic inventory `supports_json=true`; shape audit checks `supports_json`; question rows set `json_support=true` for question-family rows. | All four selected surfaces in diagnostic inventory; three selected question-family rows. |
| Surface consumes projected state / repo files / diagnostic facts as declared traits. | Diagnostic inventory and shape audit expose `uses_projected_state`, `uses_repo_files`, and `reads_diagnostic_facts`. | `service_ownership_authority`, `knowledge_reachability`, and `ops_brief` share projected state and repo-file declarations; `implementation_trait_characterization` exposes these as traits rather than consuming them. |
| Question-family dispatchability is explicit. | Question inventory enrichment derives `bounded_status`, `dispatch_surface`, and `implementation_reason` from bounded ask maps. | `operational pressure`, `knowledge reachability`, and `authority-constrained service ownership`. |
| Implementation specs identify source module and entry points. | Diagnostic shape audit `IMPLEMENTATION_SPECS` names module/build/format/json functions. | All four selected surfaces. |
| Domain answers preserve immediate support fields. | Service ownership returns required/reachable/blocked observations and authority; knowledge reachability returns stages and candidate/source metadata; ops brief returns component summaries; trait characterization returns trait concern mappings. | All four selected surfaces, but with different, non-normalized payload shapes. |

## Implementation-backed gaps

| Gap | Evidence-backed reason |
|---|---|
| No single normalized answer-support chain exists. | Question inventory, diagnostic inventory, diagnostic shape audit, and answer payloads each preserve pieces, but no current row or payload connects `question_family -> dispatch_surface -> diagnostic_spec -> implementation inputs -> answer fields`. |
| Diagnostic-only surfaces can be important support surfaces without question-family ownership. | `implementation_trait_characterization` is registered in diagnostic inventory and shape audit but absent from `QuestionSurfaceInventoryRow` rows and bounded dispatch maps. |
| Payload support fields are domain-specific rather than cross-surface provenance. | Service ownership has authority/observation fields, knowledge reachability has candidate/stage metadata, ops brief has aggregate sections, and trait characterization has trait/concern rows. These are evidence, but not a common provenance schema. |
| Implementation specs preserve marker-level evidence, not full dependency chains. | Shape audit specs identify module paths, entry points, repo markers, diagnostic markers, and mutation markers; they do not enumerate every internal builder call as a structured graph tied to output fields. |
| Question Family does not own arbitrary diagnostic support. | The question inventory explicitly includes selected question surfaces and diagnostic-only inventory/audit rows, but not every registered diagnostic surface. |
| Shape audit validates operational shape, not answer derivation. | It checks fields like JSON support, record scope, repo-file use, projected-state use, diagnostic-fact reads, and mutation, but does not prove how a concrete answer value was derived. |

## Currently visible but disconnected relationships

Only implementation-preserved relationships are listed here:

```text
Question Family
  -> QuestionSurfaceInventoryRow.surface
  -> QuestionSurfaceInventoryRow.surface_flag
  -> BOUNDED_ASK_DISPATCH_SURFACES[question_family]
  -> bounded_status / required_surface_args / implementation_reason
```

```text
DiagnosticInventoryEntry.name
  -> cli_flags
  -> uses_projected_state / uses_repo_files / reads_diagnostic_facts
  -> supports_json / supports_record / record_scope
  -> writes_event_ledger / mutates_cluster
```

```text
DiagnosticImplementationSpec.name
  -> module_path
  -> build_function / format_function / json_function / record_function
  -> repo_file_markers / diagnostic_fact_read_markers / mutation_markers
  -> DiagnosticShapeAuditRow(field, declared, observed, status)
```

```text
Concrete answer payload
  -> domain-specific support fields
  -> outcome / rows / sections / trait concern rows
```

These chains are visible separately. Existing implementation does not join them into a single answer-support relation for a concrete answer.

## Required question answers

### 1. What implementation-backed relationships already contribute to answering an inquiry?

The existing relationships are Question Family classification, answering surface metadata, CLI flag metadata, bounded dispatch metadata, diagnostic inventory shape declarations, diagnostic shape-audit implementation specs, evidence-source declarations, operational boundary declarations, and surface-specific answer payload fields. These are implementation-backed because they are dataclass fields, static maps, diagnostic registry rows, implementation specs, audit output, or concrete evaluator output.

### 2. Which support relationships recur across multiple inquiry surfaces?

Recurring relationships include CLI surface registration, JSON support, no-record/default read-only boundary, non-mutating cluster boundary, projected-state/repo-file/diagnostic-fact evidence-source declarations, diagnostic shape audit checks, and implementation entry-point specs. Question Family dispatch metadata recurs across the selected question-family surfaces but not diagnostic-only `implementation_trait_characterization`.

### 3. Can the repository already explain `where this answer came from` using existing implementation relationships alone?

Partially. The repository can already answer where a surface came from and what immediate evidence fields a domain answer used. It cannot already provide a single connected answer-support chain for a concrete answer using existing relationships alone, because the implementation-backed pieces are distributed and disconnected.

### 4. What implementation relationships are currently visible but disconnected?

The visible disconnected chains are: Question Family to dispatch surface; diagnostic name to operational shape; diagnostic name to implementation spec; shape declarations to observed fields; and answer payload to domain-specific support fields. They are preserved, but not joined into `Question Family -> dispatch surface -> projected/repository/diagnostic evidence -> observation/authority/boundary -> concrete answer field`.

### 5. Is there sufficient implementation evidence to expose an answer-support surface?

There is sufficient evidence to expose many existing relationships without inventing new domain knowledge: question-family rows, bounded dispatch maps, diagnostic inventory entries, shape-audit implementation specs, and output payload support fields. Important links are still missing if the intended surface must explain concrete answer derivation end-to-end: normalized payload provenance, per-output-field source attribution, and a structured join across question inventory, diagnostic inventory, shape audit, and evaluator internals.

### 6. If an answer-support surface were implemented, would it primarily expose existing implementation relationships or require introducing new implementation knowledge?

A bounded first version would primarily expose existing implementation relationships. It would become new implementation knowledge if it claimed unpreserved links such as exact per-field derivation, inferred dependencies not in implementation specs, or Question Family ownership for diagnostics absent from the question inventory.

## Conclusion

The repository already contains enough implementation evidence to answer a narrower question: **which registered surface, dispatch path, operational shape, implementation entry points, evidence-source declarations, and immediate payload fields contributed to this inquiry?**

The repository does not yet contain enough connected visibility to answer the full operator question **`Where did this answer come from?`** as a single implementation-backed chain for a concrete answer. Additional visibility would be required first, but a future answer-support surface could primarily expose existing relationships if it stays bounded to relationships already preserved by implementation.

## Commands executed

```bash
pwd && find .. -name AGENTS.md -print && git status --short
cat AGENTS.md && rg -n "service_ownership_authority|operational_pressure|knowledge_reachability|implementation_trait_characterization|diagnostic-inventory|Question Family|question_family" -S .
sed -n '1,280p' seed_runtime/question_surface_inventory.py
sed -n '1,240p' seed_runtime/diagnostic_inventory.py
sed -n '1,260p' seed_runtime/diagnostic_shape_audit.py
sed -n '280,620p' seed_runtime/question_surface_inventory.py
sed -n '240,620p' seed_runtime/diagnostic_inventory.py
sed -n '260,620p' seed_runtime/diagnostic_shape_audit.py
sed -n '1,260p' seed_runtime/service_ownership_authority.py
sed -n '1,220p' seed_runtime/knowledge_reachability.py
sed -n '1,220p' seed_runtime/implementation_trait_characterization.py
sed -n '1,220p' seed_runtime/ops_brief.py
python scripts/seed_local.py --question-surface-inventory --json | python -m json.tool | head -120
python scripts/seed_local.py --diagnostic-inventory --json | python -m json.tool | rg -n '"name": "(service_ownership_authority|knowledge_reachability|implementation_trait_characterization|ops_brief)"' -A16
python scripts/seed_local.py --diagnostic-shape-audit --json | python -m json.tool | rg -n '"diagnostic": "(service_ownership_authority|knowledge_reachability|implementation_trait_characterization|ops_brief)"' -A5 | head -160
python scripts/seed_local.py --service-ownership-authority --json > /tmp/service.json
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr.json
python scripts/seed_local.py --implementation-trait-characterization --json > /tmp/itc.json
python scripts/seed_local.py --ops-brief --json > /tmp/ops.json
python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/implementation_trait_characterization.py`
- `seed_runtime/ops_brief.py`
- Related existing docs returned by repository search under `docs/`.

## Files changed

- `docs/answer_support_relationships_investigation.md`

## LOC changed

- Added 179 lines in `docs/answer_support_relationships_investigation.md`.

## Tests run

- `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`
