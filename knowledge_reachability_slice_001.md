# Knowledge Reachability Slice 001 — Candidate discovery and source-budget admission

## District consistency gate

- Active district verified: **Knowledge Reachability**.
- Handoff source verified: **`operational_graph_outward_scout_005.md`**.
- Completed source district verified: **Operational Graph**.
- Latest completed Operational Graph slice verified: **`operational_graph_slice_008.md`**.
- No local branch/report mismatch was found before implementation; repository authority came from `seed_runtime/knowledge_reachability.py`.

## Selected boundary

Knowledge Reachability candidate discovery and source-budget admission.

## Implementation evidence

`build_knowledge_reachability_audit_result(...)` compressed candidate discovery, source-budget admission, subject bypass, family/kind filtering, global limit handling, raw-seen accounting, source counts, scan counts, truncation state, and discovery phase metadata before index construction and row evaluation.

## Before

The result builder directly called `_discover_candidates(...)`, rewrote subject/family/kind filters inline, sorted and capped candidates inline, and carried source/scan/truncation values into public metadata.

## After

`_admit_knowledge_reachability_candidates(...)` now owns that admission boundary and returns `_CandidateAdmission`, while `build_knowledge_reachability_audit_result(...)` remains the compatibility assembler and consumes the unchanged values.

## Recovered producer

`_admit_knowledge_reachability_candidates(...)`.

## Recovered artifact/helper

`_CandidateAdmission` carries the discovered candidates, sorted candidate list, source counts, scan counts, effective limit, discovered count, skipped count, truncation flag, and reason.

## Recovered consumer

`build_knowledge_reachability_audit_result(...)` consumes `_CandidateAdmission` during the existing `discover_candidates` phase.

## Compatibility preserved

No.

Public runtime behavior, CLI behavior, JSON output, table/human output, schema, candidate counts, source counts, scan counts, limit behavior, truncation behavior, read-only behavior, event-ledger behavior, and mutation flags are preserved.

## Files changed

- `seed_runtime/knowledge_reachability.py`
- `tests/test_knowledge_reachability.py`
- `knowledge_reachability_slice_001.md`

## LOC changed

Part of the batch diff: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py` changed with 352 insertions and 55 deletions before reports.

## Tests executed

- `pytest -q tests/test_knowledge_reachability.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed.

Focused coverage includes default seed, event-payload, projected-state, source-navigation-term, docs, and `seed_runtime/` candidate admission; source budget/global limit behavior; subject bypass; raw-seen/source/scan counts; truncation state; public JSON/table output; read-only ledger preservation.

## Remaining compressed responsibilities

After this slice, staged index construction and candidate row evaluation remained visible as separate adjacent responsibilities.

## Required questions

1. **What responsibility was previously compressed?** Candidate discovery and source-budget admission across default seeds, event payloads, projected state, source-navigation terms, docs, and seed runtime sources.
2. **Which implementation-local ownership boundary became directly observable?** Admission of candidates into the audit candidate set before staged index construction.
3. **What producer now owns the recovered responsibility?** `_admit_knowledge_reachability_candidates(...)`.
4. **What artifact or helper carries the recovered boundary, if any?** `_CandidateAdmission`.
5. **Who consumes it?** `build_knowledge_reachability_audit_result(...)`.
6. **Did any compatibility boundary change?** No.
7. **How does this stay inside the Knowledge Reachability district?** It only admits candidates for the Knowledge Reachability audit and does not alter other diagnostics.
8. **How is this distinct from prior Operational Graph slices?** It does not create graph nodes/edges, merge edges, filter confidence edges, select examples, or build graph confidence summaries.
9. **How is this distinct from prior Emitter Attribution Audit slices?** It does not classify or construct emitter-attribution rows/items.
10. **How is this distinct from prior Emitter/Consumer Audit slices?** It does not collect emitted outputs, derive relationship status, or construct emitter/consumer rows.
11. **How is this distinct from prior Consumer Dependency Audit slices?** It does not produce dependency audit item families or matched consumer groups.
12. **How is this distinct from prior Frontier Pressure Admission slices?** It does not admit pressure candidates or produce pressure evidence/score/item sets.
13. **How does this avoid Source Navigation direct work?** It consumes existing fact-support-derived terms only as candidate source material; it does not compose or dispatch Source Navigation queries.
14. **How does this avoid Question Surface Inventory and bounded ask work?** It does not modify inventory, dispatch, bounded ask routing, or question surfaces.
15. **How does this preserve Knowledge Reachability JSON and table output?** Public rows and metadata values are passed through the same result builder and existing renderers.
16. **How does this preserve diagnostic inventory and diagnostic-shape visibility?** No diagnostic surface registration or shape-audit specification changed; existing diagnostic tests pass.
17. **How does this preserve read-only and event-ledger behavior?** The helper only reads events/state/repo files and tests assert the ledger event count is unchanged.
18. **How is this distinct from any earlier slice in this batch?** This is the first slice in the batch.

## District boundary compliance

The slice remains local to `seed_runtime/knowledge_reachability.py` and focused tests. It avoids Operational Graph, Source Navigation direct query composition, Question Surface Inventory, bounded ask dispatch, diagnostic registration, CLI dispatch, JSON serialization internals, table formatting internals, and public result packaging.
