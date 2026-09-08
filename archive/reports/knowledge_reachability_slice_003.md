# Knowledge Reachability Slice 003 — Candidate stage evaluation and first-loss row production

## District consistency gate

- Active district verified: **Knowledge Reachability**.
- Handoff source verified: **`operational_graph_outward_scout_005.md`**.
- Completed source district verified: **Operational Graph**.
- Latest completed Operational Graph slice verified: **`operational_graph_slice_008.md`**.
- After Slices 001 and 002, `build_knowledge_reachability_audit_result(...)` was reassessed and candidate evaluation remained a narrow implementation-local boundary distinct from admission, index construction, metadata assembly, rendering, diagnostic registration, Source Navigation query composition, and bounded ask work.

## Selected boundary

Knowledge Reachability candidate stage evaluation and first-loss row production.

## Implementation evidence

After candidate admission produced `sorted_candidates` and staged index construction produced `_AuditIndexes`, the result builder still contained a local loop that enforced deadline/progress behavior, evaluated per-candidate flags, classified candidate kind, calculated first-loss, and constructed `KnowledgeReachabilityRow` values.

## Before

The evaluate phase directly contained deadline checks, progress messages, `_candidate_flags_from_indexes(...)`, `_candidate_kind(...)`, `_first_loss(...)`, and row construction.

## After

`_evaluate_knowledge_reachability_candidates(...)` owns per-candidate evaluation and returns `_EvaluationResult`; `build_knowledge_reachability_audit_result(...)` remains responsible for public metadata/result assembly.

## Recovered producer

`_evaluate_knowledge_reachability_candidates(...)`.

## Recovered artifact/helper

`_EvaluationResult` carries produced rows plus skipped/truncated/reason state.

## Recovered consumer

`build_knowledge_reachability_audit_result(...)` consumes `_EvaluationResult` before building existing metadata.

## Compatibility preserved

No.

Candidate flags, candidate kind classification, first-loss classification, row fields, row order, progress handling, deadline handling, truncation behavior, metadata counts, public JSON/table output, read-only behavior, event-ledger behavior, and diagnostic visibility are preserved.

## Files changed

- `seed_runtime/knowledge_reachability.py`
- `tests/test_knowledge_reachability.py`
- `knowledge_reachability_slice_003.md`

## LOC changed

Part of the batch diff: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py` changed with 352 insertions and 55 deletions before reports.

## Tests executed

- `pytest -q tests/test_knowledge_reachability.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.

Focused coverage includes candidate flag evaluation from indexes, candidate kind classification, first-loss classification, `KnowledgeReachabilityRow` construction, row order/fields, progress handling, deadline/truncation behavior, metadata counts, public JSON/table output, read-only ledger preservation.

## Remaining compressed responsibilities

Broad result metadata assembly, JSON rendering, table formatting, diagnostic registration, question-surface inventory, bounded ask compatibility, and CLI dispatch remain intentionally unrecovered by this batch.

## Required questions

1. **What responsibility was previously compressed?** Per-candidate stage evaluation and first-loss row production.
2. **Which implementation-local ownership boundary became directly observable?** Evaluation of admitted candidates against completed indexes into `KnowledgeReachabilityRow` values.
3. **What producer now owns the recovered responsibility?** `_evaluate_knowledge_reachability_candidates(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_EvaluationResult`.
5. **Who consumes it?** `build_knowledge_reachability_audit_result(...)`.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Knowledge Reachability district?** It evaluates Knowledge Reachability candidates against Knowledge Reachability indexes only.
8. **How is this distinct from prior Operational Graph slices?** It does not compose graph audit evidence, nodes, edges, confidence tiers, aggregate filtering, examples, or summary payloads.
9. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify emitters or build attribution rows/items.
10. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect emitted outputs or derive emitter/consumer audit rows.
11. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce consumer dependency item families or matched groups.
12. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates or score fragile/orphaned predicate pressure.
13. **How does this avoid Source Navigation direct work?** It evaluates against an existing index artifact and does not compose/direct Source Navigation queries.
14. **How does this avoid Question Surface Inventory and bounded ask work?** It does not touch inventory, dispatch, bounded ask matching, or public question routes.
15. **How does this preserve Knowledge Reachability JSON and table output?** Rows have identical fields/order and still flow through unchanged renderers.
16. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No diagnostic registration/spec changes were made; diagnostic tests pass.
17. **How does this preserve read-only and event-ledger behavior?** Evaluation reads in-memory candidates/indexes only and tests assert no ledger mutation.
18. **How is this distinct from any earlier slice in this batch?** Slice 001 owns candidate admission; Slice 002 owns index construction; this slice owns row production from both artifacts.

## District boundary compliance

The slice remains local to Knowledge Reachability row evaluation. It avoids broad result assembly, JSON rendering, table formatting, diagnostic registration, CLI dispatch, Source Navigation direct work, Question Surface Inventory, bounded ask work, and prior districts.
