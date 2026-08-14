# Knowledge Reachability Slice 004 — Public result metadata assembly

## District consistency gate

- Active district verified: **Knowledge Reachability**.
- Latest relevant completed slice verified: **`knowledge_reachability_slice_003.md`**.
- Latest local district scout verified: **`knowledge_reachability_district_scout_001.md`**.
- Branch and local files did not point to another active district. Unrelated district reports were not used as authority.

## Selected boundary

Public result metadata assembly.

## Implementation evidence

After `_admit_knowledge_reachability_candidates(...)`, `_construct_knowledge_reachability_indexes(...)`, and `_evaluate_knowledge_reachability_candidates(...)`, `build_knowledge_reachability_audit_result(...)` still directly assembled the public `KnowledgeReachabilityMetadata` object from recovered admission artifacts, index timing artifacts, evaluation rows, counters, cache state, truncation state, limit, and max-seconds.

## Before

The result builder directly constructed `KnowledgeReachabilityMetadata`, mixing public metadata value assembly with orchestration of admission, index construction, and evaluation.

## After

`_assemble_knowledge_reachability_metadata(...)` owns construction of the existing `KnowledgeReachabilityMetadata` object. The result builder remains the orchestrator and returns the same `KnowledgeReachabilityAuditResult` shape.

## Recovered producer

`_assemble_knowledge_reachability_metadata(...)`.

## Recovered artifact/helper

The helper returns the existing public `KnowledgeReachabilityMetadata` artifact. No new public artifact or schema was introduced.

## Recovered consumer

`build_knowledge_reachability_audit_result(...)` consumes the helper result before returning `KnowledgeReachabilityAuditResult`.

## Compatibility preserved

No.

Timings, candidate counts, candidate-kind counts, loss-stage counts, algorithmic counters, candidate sources, scan counts, cache state, index timings, truncation/reason, limit, max-seconds, JSON output, table output, read-only metadata, and event-ledger non-mutation are preserved.

## Files changed

- `seed_runtime/knowledge_reachability.py`
- `tests/test_knowledge_reachability.py`
- `knowledge_reachability_slice_004.md`

## LOC changed

Slice 004 implementation/test diff before this report: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py` changed with 148 insertions and 13 deletions.

## Tests executed

- `pytest -q tests/test_knowledge_reachability.py` — passed.

Focused coverage proves direct metadata helper construction, timing rounding, candidate counts, candidate-kind counts, loss-stage counts, algorithmic counters, candidate sources, scan counts, cache state, index timings, truncation/reason, limit, max-seconds, JSON output, table/human output, read-only metadata, and event-ledger non-mutation.

## Remaining compressed responsibilities

After this slice, direct implementation evidence still shows `knowledge_reachability_json(...)` owns JSON payload construction and `format_knowledge_reachability_table(...)` owns human/table formatting. Both require reassessment before recovery because they are sequential medium-confidence candidates.

## Required questions

1. **What responsibility was previously compressed?** Public `KnowledgeReachabilityMetadata` assembly from admission, index, evaluation, counter, cache, timing, truncation, limit, and max-seconds artifacts.
2. **Which implementation-local ownership boundary became directly observable?** Metadata production for the public Knowledge Reachability audit result.
3. **What producer now owns the recovered responsibility?** `_assemble_knowledge_reachability_metadata(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** The helper carries the boundary and returns the existing `KnowledgeReachabilityMetadata` object.
5. **Who consumes it?** `build_knowledge_reachability_audit_result(...)`.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Knowledge Reachability district?** It only assembles Knowledge Reachability audit metadata from existing Knowledge Reachability artifacts.
8. **How is this distinct from Knowledge Reachability Slice 001 candidate admission?** Slice 001 discovers/admitted candidates and source budgets; this slice only consumes the resulting admission artifact for public metadata.
9. **How is this distinct from Knowledge Reachability Slice 002 staged index construction?** Slice 002 builds reachability indexes and index timings; this slice only includes existing index timing values in public metadata.
10. **How is this distinct from Knowledge Reachability Slice 003 row evaluation?** Slice 003 produces rows and evaluation truncation state; this slice only packages completed rows and state into metadata counts and fields.
11. **How is this distinct from prior Operational Graph slices?** It does not compose graph evidence, nodes, edges, confidence tiers, aggregate filtering, examples, or graph summary payloads.
12. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify emitters or build attribution rows/items.
13. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect emitted outputs, derive relationship status, or assemble emitted-item audit rows.
14. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce observation-predicate or diagnostic item families or matched consumer groups.
15. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates, fan out pressure sources, score pressure, or produce pressure evidence payloads.
16. **How does this avoid Source Navigation direct work?** It only carries already computed source-navigation-related index timing/counter values and does not query or format Source Navigation.
17. **How does this avoid Question Surface Inventory and bounded ask work?** It does not touch inventory, dispatch, bounded ask compatibility, or question routing.
18. **How does this preserve Knowledge Reachability JSON and table output?** The existing JSON and table renderers consume the same metadata fields and rows; focused tests exercise both outputs.
19. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No diagnostic surface, registration, shape spec, CLI flag, or recordable output was added or changed.
20. **How does this preserve read-only and event-ledger behavior?** The helper consumes in-memory artifacts only; tests assert ledger event count remains unchanged.
21. **How is this distinct from any earlier slice in this batch?** This is the first slice in this batch.

## District boundary compliance

The slice remains local to Knowledge Reachability public result metadata assembly. It avoids candidate admission, index construction, row evaluation, JSON payload construction, table formatting, diagnostic registration, CLI dispatch, Source Navigation direct work, Question Surface Inventory, bounded ask work, event-ledger mutation, and prior districts.
